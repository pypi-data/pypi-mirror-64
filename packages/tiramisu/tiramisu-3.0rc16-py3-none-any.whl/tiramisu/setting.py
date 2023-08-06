# -*- coding: utf-8 -*-
"sets the options of the configuration objects Config object itself"
# Copyright (C) 2012-2020 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ____________________________________________________________
from itertools import chain
from .error import PropertiesOptionError, ConstError, ConfigError, LeadershipError, display_list
from .i18n import _
from .asyncinit import asyncinit


"""If cache and expire is enable, time before cache is expired.
This delay start first time value/setting is set in cache, even if
user access several time to value/setting
"""
EXPIRATION_TIME = 5
"""List of default properties (you can add new one if needed).

For common properties and personalise properties, if a propery is set for
an Option and for the Config together, Setting raise a PropertiesOptionError

* Common properties:

hidden
    option with this property can only get value in read only mode. This
    option is not available in read write mode.

disabled
    option with this property cannot be set/get

frozen
    cannot set value for option with this properties if 'frozen' is set in
    config

* Special property:

permissive
    option with 'permissive' cannot raise PropertiesOptionError for properties
    set in permissive
    config with 'permissive', whole option in this config cannot raise
    PropertiesOptionError for properties set in permissive

mandatory
    should set value for option with this properties if 'mandatory' is set in
    config
    example: 'a', ['a'], [None] are valid
             None, [] are not valid

empty
    raise mandatory PropertiesOptionError if multi or leader have empty value
    example: ['a'] is valid
             [None] is not valid

unique
    raise ValueError if a value is set twice or more in a multi Option

* Special Config properties:

cache
    if set, enable cache settings and values

expire
    if set, settings and values in cache expire after ``expiration_time``

everything_frozen
    whole option in config are frozen (even if option have not frozen
    property)

validator
    launch validator set by user in option (this property has no effect
    for internal validator)

warnings
    display warnings during validation

demoting_error_warning
    all value errors are convert to warning (ValueErrorWarning)
"""
DEFAULT_PROPERTIES = frozenset(['cache', 'validator', 'warnings'])
SPECIAL_PROPERTIES = {'frozen', 'mandatory', 'empty', 'force_store_value'}

"""Config can be in two defaut mode:

read_only
    you can get all variables not disabled but you cannot set any variables
    if a value has a callback without any value, callback is launch and value
    of this variable can change
    you cannot access to mandatory variable without values

read_write
    you can get all variables not disabled and not hidden
    you can set all variables not frozen
"""
RO_APPEND = frozenset(['frozen', 'disabled', 'validator', 'everything_frozen',
                       'mandatory', 'empty', 'force_store_value'])
RO_REMOVE = frozenset(['permissive', 'hidden'])
RW_APPEND = frozenset(['frozen', 'disabled', 'validator', 'hidden',
                      'force_store_value'])
RW_REMOVE = frozenset(['permissive', 'everything_frozen', 'mandatory',
                       'empty'])


FORBIDDEN_SET_PROPERTIES = frozenset(['force_store_value'])
FORBIDDEN_SET_PERMISSIVES = frozenset(['force_default_on_freeze',
                                       'force_metaconfig_on_freeze',
                                       'force_store_value'])
ALLOWED_LEADER_PROPERTIES = frozenset(['empty',
                                       'unique',
                                       'force_store_value',
                                       'mandatory',
                                       'force_default_on_freeze',
                                       'force_metaconfig_on_freeze',
                                       'frozen'])

static_set = frozenset()


class OptionBag:
    __slots__ = ('option',  # current option
                 'path',
                 'index',
                 'config_bag',
                 'ori_option',  # original option (for example useful for symlinkoption)
                 'properties',  # properties of current option
                 'properties_setted',
                 'apply_requires',  # apply requires or not for this option
                 )

    def __init__(self):
        self.option = None

    def set_option(self,
                   option,
                   index,
                   config_bag):
        if config_bag is undefined:
            self.path = None
        else:
            self.path = option.impl_getpath()
        self.index = index
        self.option = option
        self.config_bag = config_bag

    def __getattr__(self, key):
        if key == 'ori_option':
            return self.option
        elif key == 'apply_requires':
            return True
        elif key == 'properties_setted':
            return False
        raise KeyError('unknown key "{}" for OptionBag'.format(key))  # pragma: no cover

    def __setattr__(self, key, val):
        super().__setattr__(key, val)
        if key == 'properties':
            self.properties_setted = True

    def __delattr__(self, key):
        if key in ['properties', 'permissives']:
            try:
                super().__delattr__(key)
            except AttributeError:
                pass
            return
        raise KeyError(_('cannot delete key "{}" for OptionBag').format(key))  # pragma: no cover

    def copy(self):
        option_bag = OptionBag()
        for key in self.__slots__:
            if key == 'properties' and self.config_bag is undefined:
                continue
            if hasattr(self, key):
                setattr(option_bag, key, getattr(self, key))
        return option_bag


class ConfigBag:
    __slots__ = ('context',  # link to the current context
                 'properties',  # properties for current context
                 'true_properties',  # properties for current context
                 'is_unrestraint',
                 'permissives',  # permissives for current context
                 'expiration_time',  # EXPIRATION_TIME
                 'connection',
                 )

    def __init__(self,
                 context,
                 properties: set,
                 permissives: frozenset,
                 **kwargs):
        self.context = context
        self.properties = properties
        self.permissives = permissives
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, key):
        if key == 'true_properties':
            return self.properties
        if key == 'expiration_time':
            self.expiration_time = EXPIRATION_TIME
            return self.expiration_time
        if key == 'is_unrestraint':
            return False
        raise KeyError('unknown key "{}" for ConfigBag'.format(key))  # pragma: no cover

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def remove_warnings(self):
        self.properties = frozenset(self.properties - {'warnings'})

    def remove_validation(self):
        self.properties = frozenset(self.properties - {'validator'})

    def unrestraint(self):
        self.is_unrestraint = True
        self.true_properties = self.properties
        self.properties = frozenset(['cache'])

    def set_permissive(self):
        self.properties = frozenset(self.properties | {'permissive'})

    def copy(self):
        kwargs = {}
        for key in self.__slots__:
            try:
                kwargs[key] = getattr(self, key)
            except KeyError:
                pass
        return ConfigBag(**kwargs)


# ____________________________________________________________
class _NameSpace(object):
    """convenient class that emulates a module
    and builds constants (that is, unique names)
    when attribute is added, we cannot delete it
    """

    def __setattr__(self,
                    name,
                    value):
        if name in self.__dict__:
            raise ConstError(_("can't rebind {0}").format(name))
        self.__dict__[name] = value

    def __delattr__(self,
                    name):
        raise ConstError(_("can't unbind {0}").format(name))


class GroupModule(_NameSpace):
    "emulates a module to manage unique group (OptionDescription) names"
    class GroupType(str):
        """allowed normal group (OptionDescription) names
        *normal* means : groups that are not leader
        """
        pass

    class DefaultGroupType(GroupType):
        """groups that are default (typically 'default')"""
        pass

    class LeadershipGroupType(GroupType):
        """allowed normal group (OptionDescription) names
        *leadership* means : groups that have the 'leadership' attribute set
        """
        pass

    class RootGroupType(GroupType):
        """root means this is the root optiondescription of whole config
        """
        pass

    def addgroup(self, name):
        setattr(groups, name, groups.GroupType(name))


class OwnerModule(_NameSpace):
    """emulates a module to manage unique owner names.

    owners are living in `Config._cfgimpl_value_owners`
    """
    class Owner(str):
        """allowed owner names
        """
        pass

    class DefaultOwner(Owner):
        """groups that are default (typically 'default')"""
        pass

    def addowner(self, name):
        """
        :param name: the name of the new owner
        """
        setattr(owners, name, owners.Owner(name))


# ____________________________________________________________
# populate groups
groups = GroupModule()
"""groups.default
        default group set when creating a new optiondescription"""
groups.default = groups.DefaultGroupType('default')

"""groups.leadership
        leadership group is a special optiondescription, all suboptions should
        be multi option and all values should have same length, to find
        leader's option, the optiondescription's name should be same than de
        leader's option"""
groups.leadership = groups.LeadershipGroupType('leadership')

"""    groups.root
        this group is the root optiondescription of whole config"""
groups.root = groups.RootGroupType('root')


# ____________________________________________________________
# populate owners with default attributes
owners = OwnerModule()
"""default
        is the config owner after init time"""
owners.default = owners.DefaultOwner('default')
"""user
        is the generic is the generic owner"""
owners.user = owners.Owner('user')
"""forced
        special owner when value is forced"""
owners.forced = owners.Owner('forced')


forbidden_owners = (owners.default, owners.forced)


# ____________________________________________________________
class Undefined(object):
    def __str__(self):  # pragma: no cover
        return 'Undefined'

    __repr__ = __str__


undefined = Undefined()


# ____________________________________________________________
class Settings(object):
    "``config.Config()``'s configuration options settings"
    __slots__ = ('_p_',
                 '_pp_',
                 '__weakref__',
                 'ro_append',
                 'ro_remove',
                 'rw_append',
                 'rw_remove',
                 'default_properties')

    def __init__(self,
                 properties,
                 permissives):
        """
        initializer

        :param context: the root config
        :param storage: the storage type
        """
        # generic owner
        self._p_ = properties
        self._pp_ = permissives
        self.default_properties = DEFAULT_PROPERTIES
        self.ro_append = RO_APPEND
        self.ro_remove = RO_REMOVE
        self.rw_append = RW_APPEND
        self.rw_remove = RW_REMOVE

    # ____________________________________________________________
    # get properties and permissive methods

    async def get_context_properties(self,
                                     connection,
                                     cache):
        is_cached, props, validated = cache.getcache(None,
                                                     None,
                                                     None,
                                                     {},
                                                     {},
                                                     'context_props')
        if not is_cached:
            props = await self._p_.getproperties(connection,
                                                 None,
                                                 None,
                                                 self.default_properties)
            cache.setcache(None,
                           None,
                           props,
                           {},
                           props,
                           True)
        return props

    async def getproperties(self,
                            option_bag,
                            apply_requires=True,
                            uncalculated=False,
                            help_property=False):
        """
        """
        option = option_bag.option
        config_bag = option_bag.config_bag
        if option.impl_is_symlinkoption():
            option = option.impl_getopt()
        path = option.impl_getpath()
        index = option_bag.index
        if apply_requires and not uncalculated and not help_property:
            cache = config_bag.context._impl_properties_cache
            is_cached, props, validated = cache.getcache(path,
                                                         config_bag.expiration_time,
                                                         index,
                                                         config_bag.properties,
                                                         {},
                                                         'self_props')
        else:
            is_cached = False
        if not is_cached:
            props = set()
            # if index, get option's properties (without index) too
            p_props = await self._p_.getproperties(config_bag.connection,
                                                   path,
                                                   None,
                                                   option.impl_getproperties())
            if index is not None:
                p_props = chain(p_props,
                                await self._p_.getproperties(config_bag.connection,
                                                             path,
                                                             index,
                                                             option.impl_getproperties()))
            for prop in p_props:
                if uncalculated or isinstance(prop, str):
                    if not help_property:
                        props.add(prop)
                    else:
                        props.add((prop, prop))
                elif apply_requires:
                    if not help_property:
                        new_prop = await prop.execute(option_bag,
                                                      leadership_must_have_index=True)
                    else:
                        new_prop = await prop.help(option_bag,
                                                   leadership_must_have_index=True)
                        if isinstance(new_prop, str):
                            new_prop = (new_prop, new_prop)
                    if new_prop is None:
                        continue
                    elif (not help_property and not isinstance(new_prop, str)) or \
                            (help_property and not isinstance(new_prop, tuple)):
                        raise ValueError(_('invalid property type {} for {} with {} function').format(type(new_prop),
                                                                                                      option_bag.option.impl_getname(),
                                                                                                      prop.function.__name__))
                    if not option.impl_is_optiondescription() and \
                            option.impl_is_leader() and \
                            new_prop not in ALLOWED_LEADER_PROPERTIES:
                        raise LeadershipError(_('leader cannot have "{}" property').format(new_prop))
                    props.add(new_prop)
            props -= await self.getpermissives(option_bag)
            if not uncalculated and apply_requires and not config_bag.is_unrestraint and not help_property:
                cache.setcache(path,
                               index,
                               props,
                               props,
                               config_bag.properties,
                               True)
        return props

    async def has_properties_index(self,
                                   option_bag):
        option = option_bag.option
        if option.impl_is_symlinkoption():
            option = option.impl_getopt()
        path = option.impl_getpath()
        p_props = await self._p_.getproperties(option_bag.config_bag.connection,
                                               path,
                                               None,
                                               option.impl_getproperties())
        if option_bag.index is not None:
            p_props = chain(p_props,
                            await self._p_.getproperties(option_bag.config_bag.connection,
                                                         path,
                                                         option_bag.index,
                                                         option.impl_getproperties()))
        for prop in p_props:
            if not isinstance(prop, str) and prop.has_index(option_bag.option):
                return True
        return False

    async def get_context_permissives(self,
                                      connection):
        return await self.getpermissives(None,
                                         connection=connection)

    async def getpermissives(self,
                             option_bag,
                             connection=None):
        if option_bag is None:
            path = None
            index = None
        else:
            opt = option_bag.option
            if opt.impl_is_symlinkoption():
                opt = opt.impl_getopt()
                path = opt.impl_getpath()
            else:
                path = option_bag.path
            index = option_bag.index
            connection = option_bag.config_bag.connection
        permissives = await self._pp_.getpermissives(connection,
                                                     path,
                                                     None)
        if index is not None:
            option_permissives = await self._pp_.getpermissives(connection,
                                                                path,
                                                                index)
            permissives = frozenset(option_permissives | permissives)
        return permissives

    #____________________________________________________________
    # set methods
    async def set_context_properties(self,
                                     connection,
                                     properties,
                                     context):
        await self._p_.setproperties(connection,
                                     None,
                                     None,
                                     properties)
        await context.cfgimpl_reset_cache(None)

    async def setproperties(self,
                            path,
                            properties,
                            option_bag,
                            context):
        """save properties for specified path
        (never save properties if same has option properties)
        """
        opt = option_bag.option
        if opt.impl_is_symlinkoption():
            raise TypeError(_("can't assign property to the symlinkoption \"{}\""
                              "").format(opt.impl_get_display_name()))
        if not opt.impl_is_optiondescription() and opt.impl_is_leader():
            not_allowed_properties = properties - ALLOWED_LEADER_PROPERTIES
            if not_allowed_properties:
                if len(not_allowed_properties) == 1:
                    raise LeadershipError(_('leader cannot have "{}" property').format(list(not_allowed_properties)[0]))
                else:
                    raise LeadershipError(_('leader cannot have {} properties').format(display_list(list(not_allowed_properties), add_quote=True)))
            if ('force_default_on_freeze' in properties or 'force_metaconfig_on_freeze' in properties) and \
                    'frozen' not in properties:
                raise LeadershipError(_('a leader ({0}) cannot have '
                                        '"force_default_on_freeze" or "force_metaconfig_on_freeze" property without "frozen"'
                                        '').format(opt.impl_get_display_name()))
        await self._p_.setproperties(option_bag.config_bag.connection,
                                     path,
                                     option_bag.index,
                                     properties)
        # values too because of follower values could have a PropertiesOptionError has value
        await context.cfgimpl_reset_cache(option_bag)
        option_bag.properties = properties

    async def set_context_permissives(self,
                                      connection,
                                      permissives):
        await self.setpermissives(None,
                                  permissives,
                                  connection=connection)

    async def setpermissives(self,
                             option_bag,
                             permissives,
                             connection=None):
        """
        enables us to put the permissives in the storage

        :param path: the option's path
        :param type: str
        :param opt: if an option object is set, the path is extracted.
                    it is better (faster) to set the path parameter
                    instead of passing a :class:`tiramisu.option.Option()` object.
        """
        if not isinstance(permissives, frozenset):
            raise TypeError(_('permissive must be a frozenset'))
        if option_bag is not None:
            opt = option_bag.option
            if opt and opt.impl_is_symlinkoption():
                raise TypeError(_("can't assign permissive to the symlinkoption \"{}\""
                                  "").format(opt.impl_get_display_name()))
            path = option_bag.path
            index = option_bag.index
            connection = option_bag.config_bag.connection
        else:
            path = None
            index = None
        forbidden_permissives = FORBIDDEN_SET_PERMISSIVES & permissives
        if forbidden_permissives:
            raise ConfigError(_('cannot add those permissives: {0}').format(
                ' '.join(forbidden_permissives)))
        await self._pp_.setpermissives(connection,
                                       path,
                                       index,
                                       permissives)
        if option_bag is not None:
            await option_bag.config_bag.context.cfgimpl_reset_cache(option_bag)

    #____________________________________________________________
    # reset methods

    async def reset(self,
                    option_bag,
                    config_bag):
        if option_bag is None:
            opt = None
            path = None
            index = None
        else:
            opt = option_bag.option
            assert not opt.impl_is_symlinkoption(), _("can't reset properties to "
                                                      "the symlinkoption \"{}\""
                                                      "").format(opt.impl_get_display_name())
            path = option_bag.path
            index = option_bag.index
        await self._p_.delproperties(config_bag.connection,
                                     path,
                                     index)
        await config_bag.context.cfgimpl_reset_cache(option_bag)

    async def reset_permissives(self,
                                option_bag,
                                config_bag):
        if option_bag is None:
            opt = None
            path = None
            index = None
        else:
            opt = option_bag.option
            assert not opt.impl_is_symlinkoption(), _("can't reset permissives to "
                                                      "the symlinkoption \"{}\""
                                                      "").format(opt.impl_get_display_name())
            index = option_bag.index
            path = option_bag.path
        await self._pp_.delpermissive(config_bag.connection,
                                      path,
                                      index)
        await config_bag.context.cfgimpl_reset_cache(option_bag)

    #____________________________________________________________
    # validate properties
    async def calc_raises_properties(self,
                                     option_bag,
                                     apply_requires=True,
                                     uncalculated=False):
        if not uncalculated and apply_requires and option_bag.properties_setted:
            option_properties = option_bag.properties
        else:
            option_properties = await self.getproperties(option_bag,
                                                         apply_requires=apply_requires,
                                                         uncalculated=uncalculated)
        return self._calc_raises_properties(option_bag.config_bag.properties,
                                            option_bag.config_bag.permissives,
                                            option_properties)

    def _calc_raises_properties(self,
                                context_properties,
                                context_permissives,
                                option_properties):
        raises_properties = context_properties - SPECIAL_PROPERTIES
        # remove global permissive properties
        if raises_properties and 'permissive' in raises_properties:
            raises_properties -= context_permissives
        properties = option_properties & raises_properties
        # at this point it should not remain any property for the option
        return properties

    async def validate_properties(self,
                                  option_bag,
                                  need_help=True):
        config_properties = option_bag.config_bag.properties
        if not config_properties or config_properties == frozenset(['cache']):
            # if no global property
            return
        properties = await self.calc_raises_properties(option_bag)
        if properties != frozenset():
            if need_help:
                help_properties = dict(await self.getproperties(option_bag,
                                                                help_property=True))
                calc_properties = []
                for property_ in self._calc_raises_properties(option_bag.config_bag.properties,
                                                              option_bag.config_bag.permissives,
                                                              set(help_properties.keys())):
                    calc_properties.append(help_properties[property_])
                calc_properties = frozenset(calc_properties)
            else:
                calc_properties = properties
            raise PropertiesOptionError(option_bag,
                                        properties,
                                        self,
                                        help_properties=calc_properties)

    def validate_mandatory(self,
                           value,
                           option_bag):
        if 'mandatory' in option_bag.config_bag.properties:
            values = option_bag.config_bag.context.cfgimpl_get_values()
            if option_bag.option.impl_is_follower():
                force_allow_empty_list = True
            else:
                force_allow_empty_list = False
            if not ('permissive' in option_bag.config_bag.properties and
                    'mandatory' in option_bag.config_bag.permissives) and \
                    'mandatory' in option_bag.properties and values.isempty(option_bag.option,
                                                                                 value,
                                                                                 force_allow_empty_list=force_allow_empty_list,
                                                                                 index=option_bag.index):
                raise PropertiesOptionError(option_bag,
                                            ['mandatory'],
                                            self)
            if 'empty' in option_bag.properties and values.isempty(option_bag.option,
                                                                   value,
                                                                   force_allow_empty_list=True,
                                                                   index=option_bag.index):
                raise PropertiesOptionError(option_bag,
                                            ['empty'],
                                            self)

    def validate_frozen(self,
                        option_bag):
        if option_bag.config_bag.properties and \
                ('everything_frozen' in option_bag.config_bag.properties or
                 ('frozen' in option_bag.config_bag.properties and 'frozen' in option_bag.properties)) and \
                not (('permissive' in option_bag.config_bag.properties) and
                     'frozen' in option_bag.config_bag.permissives):
            raise PropertiesOptionError(option_bag,
                                        ['frozen'],
                                        self)
        return False
    #____________________________________________________________
    # read only/read write

    async def _read(self,
                    remove,
                    append,
                    config_bag):
        props = await self._p_.getproperties(config_bag.connection,
                                             None,
                                             None,
                                             self.default_properties)
        modified = False
        if remove & props:
            props = props - remove
            modified = True
        if append & props != append:
            props = props | append
            modified = True
        if modified:
            await self.set_context_properties(config_bag.connection,
                                              frozenset(props),
                                              config_bag.context)

    async def read_only(self,
                        config_bag):
        "convenience method to freeze, hide and disable"
        await self._read(self.ro_remove,
                         self.ro_append,
                         config_bag)

    async def read_write(self,
                         config_bag):
        "convenience method to freeze, hide and disable"
        await self._read(self.rw_remove,
                         self.rw_append,
                         config_bag)
