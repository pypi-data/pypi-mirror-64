# -*- coding: utf-8 -*-
# Copyright (C) 2017-2020 Team tiramisu (see AUTHORS for all contributors)
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
from inspect import ismethod, getdoc, signature
from time import time
from typing import List, Set, Any, Optional, Callable, Union, Dict
from warnings import catch_warnings, simplefilter
from functools import wraps


from .error import APIError, ConfigError, LeadershipError, PropertiesOptionError, ValueErrorWarning
from .i18n import _
from .setting import ConfigBag, OptionBag, owners, groups, Undefined, undefined, \
                     FORBIDDEN_SET_PROPERTIES, SPECIAL_PROPERTIES, EXPIRATION_TIME
from .storage import default_storage
from .config import KernelConfig, SubConfig, KernelGroupConfig, KernelMetaConfig, KernelMixConfig
from .option import RegexpOption, OptionDescription
from .todict import TiramisuDict
from .asyncinit import asyncinit


TIRAMISU_VERSION = 3


class TiramisuHelp:
    _tmpl_help = '    {0}\t{1}'

    def help(self,
             _display: bool=True) -> List[str]:
        def display(doc=''):
            if _display: # pragma: no cover
                print(doc)
        options = []
        all_modules = dir(self)
        modules = []
        max_len = 0
        force = False
        for module_name in all_modules:
            if module_name in ['forcepermissive', 'unrestraint']:
                force = True
                max_len = max(max_len, len('forcepermissive'))
            elif module_name is not 'help' and not module_name.startswith('_'):
                modules.append(module_name)
                max_len = max(max_len, len(module_name))
        modules.sort()

        display(_(getdoc(self)))
        display()
        if force:
            display(_('Settings:'))
            display(self._tmpl_help.format('forcepermissive', _('Access to option without verifying permissive properties')).expandtabs(max_len + 10))
            display(self._tmpl_help.format('unrestraint', _('Access to option without property restriction')).expandtabs(max_len + 10))
            display()
        if isinstance(self, TiramisuDispatcherOption):
            doc = _(getdoc(self.__call__))
            display(_('Call: {}').format(doc))
            display()
        display(_('Commands:'))
        for module_name in modules:
            module = getattr(self, module_name)
            doc = _(getdoc(module))
            display(self._tmpl_help.format(module_name, doc).expandtabs(max_len + 10))
        display()

    def __dir__(self):
        if '_registers' in super().__dir__():
            return list(self._registers.keys())
        return super().__dir__()


class CommonTiramisu(TiramisuHelp):
    _allow_optiondescription = True
    _validate_properties = True

    async def _get_option(self,
                          connection) -> Any:
        if not self._subconfig:
            config_bag = self._option_bag.config_bag
            try:
                subconfig, name = await config_bag.context.cfgimpl_get_home_by_path(self._option_bag.path,
                                                                                    config_bag,
                                                                                    validate_properties=self._validate_properties)
            except AssertionError as err:
                raise APIError(str(err))
            except Exception as err:
                raise err
            self._subconfig = subconfig
            self._name = name
        option = self._option_bag.option
        if option is None:
            option = await self._subconfig.cfgimpl_get_description().get_child(name,
                                                                               config_bag,
                                                                               self._subconfig.cfgimpl_get_path())
            self._option_bag.option = option
            self._option_bag.config_bag.connection = connection
            # Calculate option's properties

            settings = config_bag.context.cfgimpl_get_settings()
            self._option_bag.properties = await settings.getproperties(self._option_bag)
            if self._validate_properties:
                await settings.validate_properties(self._option_bag)
            index = self._option_bag.index
            if index is not None:
                if option.impl_is_optiondescription() or not option.impl_is_follower():
                    self._option_bag.option = None
                    raise APIError('index must be set only with a follower option')
                self._length = await self._subconfig.cfgimpl_get_length_leadership(self._option_bag)
                if index >= self._length:
                    self._option_bag.option = None
                    raise LeadershipError(_('index "{}" is greater than the leadership length "{}" '
                                            'for option "{}"').format(index,
                                                                      self._length,
                                                                      option.impl_get_display_name()))
        if not self._allow_optiondescription and option.impl_is_optiondescription():
            self._option_bag.option = None
            raise APIError(_('option must not be an optiondescription'))
        return option


class CommonTiramisuOption(CommonTiramisu):
    _allow_optiondescription = False
    _follower_need_index = True
    _validate_properties = False

    def __init__(self,
                 option_bag: OptionBag) -> None:
        self._option_bag = option_bag
        self._subconfig = None

    def __getattr__(self, name):
        raise APIError(_('unknown method "{}" in "{}"').format(name, self.__class__.__name__))


def option_and_connection(func):
    async def wrapped(self, *args, **kwargs):
        config_bag = self._option_bag.config_bag
        async with config_bag.context.getconnection() as connection:
            config_bag.connection = connection
            option = await self._get_option(connection)
            ret = await func(self, *args, **kwargs)
            del config_bag.connection
            return ret
    return wrapped


class _TiramisuOptionOptionDescription(CommonTiramisuOption):
    """Manage option"""
    _allow_optiondescription = True
    _follower_need_index = False
    _validate_properties = False

    def __init__(self,
                 option_bag: OptionBag):
        super().__init__(option_bag)
        self._config = option_bag.config_bag.context

    @option_and_connection
    async def get(self):
        """Get Tiramisu option"""
        return self._option_bag.option

    @option_and_connection
    async def type(self):
        return self._option_bag.option.impl_get_group_type()

    @option_and_connection
    async def isleadership(self):
        """Test if option is a leader or a follower"""
        return self._option_bag.option.impl_is_leadership()

    @option_and_connection
    async def doc(self):
        """Get option document"""
        return self._option_bag.option.impl_get_display_name()

    @option_and_connection
    async def description(self):
        """Get option description"""
        return self._option_bag.option.impl_get_information('doc', None)

    @option_and_connection
    async def name(self,
             follow_symlink: bool=False) -> str:
        """Get option name"""
        if not follow_symlink or \
                self._option_bag.option.impl_is_optiondescription() or \
                not self._option_bag.option.impl_is_symlinkoption():
            return self._option_bag.option.impl_getname()
        else:
            return self._option_bag.option.impl_getopt().impl_getname()

    @option_and_connection
    async def path(self) -> str:
        """Get option path"""
        return self._option_bag.path

    @option_and_connection
    async def has_dependency(self, self_is_dep=True):
        """Test if option has dependency"""
        return self._option_bag.option.impl_has_dependency(self_is_dep)

    @option_and_connection
    async def isoptiondescription(self):
        """Test if option is an optiondescription"""
        return self._option_bag.option.impl_is_optiondescription()

    @option_and_connection
    async def properties(self,
                         only_raises=False,
                         uncalculated=False):
        """Get properties for an option"""
        settings = self._option_bag.config_bag.context.cfgimpl_get_settings()
        if uncalculated:
            return await settings.getproperties(self._option_bag,
                                                uncalculated=True)
        if not only_raises:
            return await settings.getproperties(self._option_bag,
                                                apply_requires=False)
        # do not check cache properties/permissives which are not save (unrestraint, ...)
        return await settings.calc_raises_properties(self._option_bag,
                                                     apply_requires=False,
                                                     uncalculated=uncalculated)

    def __call__(self,
                 name: str,
                 index: Optional[int]=None) -> 'TiramisuOption':
        """Select an option by path"""
        path = self._option_bag.path + '.' + name
        return TiramisuOption(path,
                              index,
                              self._option_bag.config_bag)


class TiramisuOptionOption(_TiramisuOptionOptionDescription):
    """Manage option"""
    @option_and_connection
    async def ismulti(self):
        """Test if option could have multi value"""
        return self._option_bag.option.impl_is_multi()

    @option_and_connection
    async def issubmulti(self):
        """Test if option could have submulti value"""
        return self._option_bag.option.impl_is_submulti()

    @option_and_connection
    async def isleader(self):
        """Test if option is a leader"""
        return self._option_bag.option.impl_is_leader()

    @option_and_connection
    async def isfollower(self):
        """Test if option is a follower"""
        return self._option_bag.option.impl_is_follower()

    @option_and_connection
    async def issymlinkoption(self) -> bool:
        return self._option_bag.option.impl_is_symlinkoption()

    @option_and_connection
    async def default(self):
        """Get default value for an option (not for optiondescription)"""
        return self._option_bag.option.impl_getdefault()

    @option_and_connection
    async def defaultmulti(self):
        """Get default value when added a value for a multi option (not for optiondescription)"""
        option = self._option_bag.option
        ret = option.impl_getdefault_multi()
        if ret is None and option.impl_is_multi() and option.impl_has_callback() and not self.isfollower():
            callback, callback_params = option.impl_get_callback()
            values = self._option_bag.config_bag.context.cfgimpl_get_values()
            value = await values.carry_out_calculation(self._option_bag,
                                                       callback,
                                                       callback_params)
            if not isinstance(value, list):
                ret = value
        return ret

    @option_and_connection
    async def callbacks(self):
        """Get callbacks for an option (not for optiondescription)"""
        return self._option_bag.option.impl_get_callback()

    @option_and_connection
    async def validator(self):
        """Get validator for an option (not for optiondescription)"""
        return self._option_bag.option.impl_get_validator()

    @option_and_connection
    async def type(self):
        return self._option_bag.option.get_type()

    @option_and_connection
    async def pattern(self) -> str:
        option = self._option_bag.option
        type = option.get_type()
        if isinstance(option, RegexpOption):
            return option._regexp.pattern
        if type == 'integer':
            # FIXME negative too!
            return r'^[0-9]+$'
        if type == 'domainname':
            return option.impl_get_extra('_domain_re').pattern
        if type in ['ip', 'network', 'netmask']:
            #FIXME only from 0.0.0.0 to 255.255.255.255
            return r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'


class TiramisuOptionOwner(CommonTiramisuOption):
    #FIXME optiondescription must not have Owner!
    """Manage option's owner"""

    def __init__(self,
                 option_bag: OptionBag) -> None:

        super().__init__(option_bag)
        if option_bag is not None:
            # for help()
            self._values = self._option_bag.config_bag.context.cfgimpl_get_values()

    @option_and_connection
    async def get(self):
        """Get owner for a specified option"""
        return await self._values.getowner(self._option_bag)

    @option_and_connection
    async def isdefault(self):
        """Is option has defaut value"""
        return await self._values.is_default_owner(self._option_bag)

    @option_and_connection
    async def set(self, owner):
        """Get owner for a specified option"""
        try:
            obj_owner = getattr(owners, owner)
        except AttributeError:
            owners.addowner(owner)
            obj_owner = getattr(owners, owner)
        await self._values.setowner(obj_owner,
                                    self._option_bag)


class TiramisuOptionProperty(CommonTiramisuOption):
    """Manage option's property"""
    _allow_optiondescription = True
    _follower_need_index = False
    _validate_properties = False

    def __init__(self,
                 option_bag: OptionBag) -> None:
        super().__init__(option_bag)
        if option_bag and option_bag.config_bag:
            self._settings = option_bag.config_bag.context.cfgimpl_get_settings()

    @option_and_connection
    async def get(self,
                  only_raises=False,
                  uncalculated=False):
        """Get properties for an option"""
        if not only_raises:
            return self._option_bag.properties
        # do not check cache properties/permissives which are not save (unrestraint, ...)
        ret = await self._settings.calc_raises_properties(self._option_bag,
                                                          uncalculated=uncalculated)
        return ret

    @option_and_connection
    async def add(self, prop):
        """Add new property for an option"""
        if prop in FORBIDDEN_SET_PROPERTIES:
            raise ConfigError(_('cannot add this property: "{0}"').format(
                ' '.join(prop)))
        props = await self._settings._p_.getproperties(self._option_bag.config_bag.connection,
                                                       self._option_bag.path,
                                                       self._option_bag.index,
                                                       self._option_bag.option.impl_getproperties())
        await self._settings.setproperties(self._option_bag.path,
                                           props | {prop},
                                           self._option_bag,
                                           self._option_bag.config_bag.context)

    @option_and_connection
    async def pop(self, prop):
        """Remove new property for an option"""
        props = await self._settings._p_.getproperties(self._option_bag.config_bag.connection,
                                                       self._option_bag.path,
                                                       self._option_bag.index,
                                                       self._option_bag.option.impl_getproperties())
        await self._settings.setproperties(self._option_bag.path,
                                           props - {prop},
                                           self._option_bag,
                                           self._option_bag.config_bag.context)

    @option_and_connection
    async def reset(self):
        """Reset all personalised properties"""
        await self._settings.reset(self._option_bag,
                                   self._option_bag.config_bag)


class TiramisuOptionPermissive(CommonTiramisuOption):
    """Manage option's permissive"""
    _allow_optiondescription = True
    _follower_need_index = False

    def __init__(self,
                 option_bag: OptionBag) -> None:
        super().__init__(option_bag)
        if option_bag and option_bag.config_bag:
            self._settings = option_bag.config_bag.context.cfgimpl_get_settings()

    @option_and_connection
    async def get(self):
        """Get permissives value"""
        return await self._settings.getpermissives(self._option_bag)

    @option_and_connection
    async def set(self, permissives):
        """Set permissives value"""
        await self._settings.setpermissives(self._option_bag,
                                            permissives=permissives)

    @option_and_connection
    async def reset(self):
        """Reset all personalised permissive"""
        await self._settings.reset_permissives(self._option_bag,
                                               self._option_bag.config_bag)


class TiramisuOptionInformation(CommonTiramisuOption):
    """Manage option's informations"""
    _allow_optiondescription = True
    _follower_need_index = False

    def __init__(self,
                 option_bag: OptionBag) -> None:
        super().__init__(option_bag)

    @option_and_connection
    async def get(self, key, default=undefined):
        """Get information"""
        path = self._option_bag.path
        values = self._option_bag.config_bag.context.cfgimpl_get_values()
        try:
            return await values.get_information(self._option_bag.config_bag.connection,
                                                key,
                                                path=path)
        except ValueError:
            return self._option_bag.option.impl_get_information(key, default)

    @option_and_connection
    async def set(self, key, value):
        """Set information"""
        path = self._option_bag.path
        values = self._option_bag.config_bag.context.cfgimpl_get_values()
        await values.set_information(self._option_bag.config_bag.connection,
                                     key,
                                     value,
                                     path=path)

    @option_and_connection
    async def reset(self,
              key):
        """Remove information"""
        path = self._option_bag.path
        values = self._option_bag.config_bag.context.cfgimpl_get_values()
        await values.del_information(self._option_bag.config_bag.connection,
                                     key,
                                     path=path)

    @option_and_connection
    async def list(self):
        """List information's keys"""
        path = self._option_bag.path
        values = self._option_bag.config_bag.context.cfgimpl_get_values()
        return await values.list_information(self._option_bag.config_bag.connection,
                                             path)
#
#    async def len(self):
#        """Length of leadership"""
#        option = await self._get_option()
#        # for example if index is None
#        if '_length' not in vars(self):
#            self._length = self._subconfig.cfgimpl_get_length()
#        return self._length


def option_type(typ):
    if not isinstance(typ, list):
        types = [typ]
    else:
        types = typ

    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            config_bag = args[0]._option_bag.config_bag
            async with config_bag.context.getconnection() as connection:
                for typ in types:
                    if typ == 'group':
                        if args[0]._option_bag.config_bag.context.impl_type == 'group':
                            config_bag.connection = connection
                            ret = await func(*args, **kwargs, is_group=True)
                            del config_bag.connection
                            return ret
                    else:
                        config_bag.connection = connection
                        option = await args[0]._get_option(connection)
                        if typ == 'option':
                            if option.impl_is_optiondescription():
                                del config_bag.connection
                                raise APIError(_('please specify a valid sub function ({})').format(func.__name__))
                        elif typ == 'optiondescription':
                            if not option.impl_is_optiondescription():
                                del config_bag.connection
                                raise APIError(_('please specify a valid sub function ({})').format(func.__name__))
                        elif typ == 'leader':
                            if not option.impl_is_leader():
                                del config_bag.connection
                                raise APIError(_('please specify a valid sub function ({})').format(func.__name__))
                        elif typ == 'follower':
                            if not option.impl_is_follower() and not option.impl_is_leader():
                                del config_bag.connection
                                raise APIError(_('please specify a valid sub function ({})').format(func.__name__))
                        elif typ == 'choice':
                            if not option.get_type() == 'choice':
                                del config_bag.connection
                                raise APIError(_('please specify a valid sub function ({})').format(func.__name__))
                        ret = await func(*args, **kwargs)
                        del config_bag.connection
                        return ret
        return wrapped
    return wrapper


class TiramisuOptionValue(CommonTiramisuOption):
    """Manage option's value"""
    _allow_optiondescription = True
    _follower_need_index = True
    _validate_properties = True

    @option_type('optiondescription')
    async def dict(self,
                   flatten=False,
                   withwarning: bool=False,
                   fullpath=False,
                   leader_to_list=False):
        """Dict with path as key and value"""
        name = self._option_bag.option.impl_getname()
        subconfig = await self._subconfig.get_subconfig(self._option_bag)
        config_bag = self._option_bag.config_bag
        if not withwarning and config_bag.properties and 'warnings' in config_bag.properties:
            config_bag = config_bag.copy()
            config_bag.remove_warnings()
        return await subconfig.make_dict(config_bag=config_bag,
                                         flatten=flatten,
                                         fullpath=fullpath,
                                         leader_to_list=leader_to_list)

    @option_type('option')
    async def get(self):
        """Get option's value"""
        if self._option_bag.option.impl_is_follower() and self._option_bag.index is None:
            raise APIError('index must be set with a follower option')
        return await self._subconfig.getattr(self._name,
                                             self._option_bag)

    @option_type('option')
    async def set(self, value):
        """Change option's value"""
        if self._option_bag.option.impl_is_follower() and \
                self._option_bag.index is None:
            raise APIError('index must be set with a follower option')
        values = self._option_bag.config_bag.context.cfgimpl_get_values()
        if isinstance(value, list):
            while undefined in value:
                idx = value.index(undefined)
                soption_bag = self._option_bag.copy()
                soption_bag.index = idx
                value[idx] = await values.getdefaultvalue(soption_bag)
        elif value == undefined:
            value = await values.getdefaultvalue(self._option_bag)
        await self._subconfig.setattr(value,
                                      self._option_bag)

    @option_type(['group', 'option'])
    async def reset(self,
                    is_group: bool=False):
        """Reset value for an option"""
        if is_group:
            await self._option_bag.config_bag.context.reset(self._option_bag.config_bag.connection,
                                                            self._option_bag.path)
        else:
            if self._option_bag.option.impl_is_follower() and self._option_bag.index is None:
                raise APIError('index must be set with a follower option')
            await self._subconfig.delattr(self._option_bag)

    @option_type('option')
    async def default(self):
        """Get default value (default of option or calculated value)"""
        option = self._option_bag.option
        values = self._option_bag.config_bag.context.cfgimpl_get_values()
        if option.impl_is_follower() and self._option_bag.index is None:
            value = []
            length = await self._subconfig.cfgimpl_get_length_leadership(self._option_bag)
            settings = self._option_bag.config_bag.context.cfgimpl_get_settings()
            for idx in range(length):
                soption_bag = OptionBag()
                soption_bag.set_option(option,
                                       idx,
                                       self._option_bag.config_bag)
                soption_bag.properties = await settings.getproperties(soption_bag)
                value.append(await values.getdefaultvalue(soption_bag))
            return value
        else:
            return await values.getdefaultvalue(self._option_bag)

    @option_type('option')
    async def valid(self):
        try:
            with catch_warnings(record=True) as warns:
                simplefilter("always", ValueErrorWarning)
                await self.get()
                for warn in warns:
                    if isinstance(warns.message, ValueErrorWarning):
                        return False
        except ValueError:
            return False
        return True

    @option_type('choice')
    async def list(self):
        """All values available for a ChoiceOption"""
        return await self._option_bag.option.impl_get_values(self._option_bag)

    @option_type('leader')
    async def pop(self, index):
        """Pop a value"""
        if self._option_bag.option.impl_is_follower() and self._option_bag.index is None:
            raise APIError('index must be set with a follower option')
        option_bag = self._option_bag
        assert not option_bag.option.impl_is_symlinkoption(), _("can't delete a SymLinkOption")
        await option_bag.config_bag.context.cfgimpl_get_values().reset_leadership(index,
                                                                                  option_bag,
                                                                                  self._subconfig)

    @option_type('follower')
    async def len(self):
        """Length of follower option"""
        # for example if index is None
        if '_length' not in vars(self):
            self._length = await self._subconfig.cfgimpl_get_length_leadership(self._option_bag)
        return self._length


def _registers(_registers: Dict[str, type],
               prefix: str,
               extra_type: Optional[type]=None):
    for module_name in globals().keys():
        if module_name != prefix and module_name.startswith(prefix):  #  and \
            module = globals()[module_name]
            func_name = module_name[len(prefix):].lower()
            _registers[func_name] = module
#__________________________________________________________________________________________________
#


class TiramisuConfig(TiramisuHelp):
    def __init__(self,
            config_bag: ConfigBag,
            orig_config_bags: Optional[List[OptionBag]]) -> None:
        self._config_bag = config_bag
        self._orig_config_bags = orig_config_bags

    async def _return_config(self,
                             config,
                             storage):
        if isinstance(config, KernelConfig):
            return await Config(config,
                                storage=storage)
        if isinstance(config, KernelMetaConfig):
            return await MetaConfig(config,
                                    storage=storage)
        if isinstance(config, KernelMixConfig):
            return await MixConfig([],
                                   config,
                                   storage=storage)
        if isinstance(config, KernelGroupConfig):
            return await GroupConfig(config)
        raise Exception(_('unknown config type {}').format(type(config)))

    async def _reset_config_properties(self,
                                       connection):
        config = self._config_bag.context
        settings = config.cfgimpl_get_settings()
        properties = await settings.get_context_properties(connection,
                                                           config._impl_properties_cache)
        permissives = await settings.get_context_permissives(connection)
        self._config_bag.properties = properties
        self._config_bag.permissives = permissives
        if self._orig_config_bags:
            for config_bag in self._orig_config_bags:
                config_bag.properties = properties
                config_bag.permissives = permissives


class TiramisuOption(CommonTiramisu, TiramisuConfig):
    """Manage selected option"""
    _validate_properties = False
    _registers = {}
    def __init__(self,
                 path: Optional[str]=None,
                 index: Optional[int]=None,
                 config_bag: Optional[ConfigBag]=None) -> None:
        self._option_bag = OptionBag()
        self._option_bag.config_bag = config_bag
        self._option_bag.path = path
        self._option_bag.index = index
        self._subconfig = None
        self._tiramisu_dict = None
        if not self._registers:
            _registers(self._registers, 'TiramisuOption')

    def __getattr__(self, subfunc: str) -> Any:
        if subfunc in self._registers:
            return self._registers[subfunc](self._option_bag)
        raise APIError(_('please specify a valid sub function ({})').format(subfunc))  # pragma: no cover

    @option_type('optiondescription')
    async def find(self,
                   name: str,
                   value=undefined,
                   type=None,
                   first: bool=False):
        """find an option by name (only for optiondescription)"""
        if not first:
            ret = []
        option = self._option_bag.option
        config_bag = self._option_bag.config_bag
        oname = option.impl_getname()
        path = self._subconfig._get_subpath(oname)
        option_bag = OptionBag()
        option_bag.set_option(option,
                              None,
                              config_bag)
        subconfig = await self._subconfig.get_subconfig(option_bag)
        async for path in subconfig.find(byname=name,
                                         byvalue=value,
                                         bytype=type,
                                         _subpath=option_bag.path,
                                         config_bag=config_bag):
            t_option = TiramisuOption(path,
                                      None,  # index for a follower ?
                                      config_bag)
            if first:
                return t_option
            ret.append(t_option)
        return ret

    @option_type('optiondescription')
    async def group_type(self):
        """Get type for an optiondescription (only for optiondescription)"""
        return self._option_bag.option.impl_get_group_type()

    async def _filter(self,
                      opt,
                      subconfig,
                      config_bag):
        settings = config_bag.context.cfgimpl_get_settings()
        option_bag = OptionBag()
        option_bag.set_option(opt,
                              None,
                              config_bag)
        option_bag.properties = await settings.getproperties(option_bag)
        if opt.impl_is_optiondescription():
            await settings.validate_properties(option_bag)
            return await subconfig.get_subconfig(option_bag)
        await subconfig.getattr(opt.impl_getname(),
                                option_bag)

    @option_type('optiondescription')
    async def list(self,
                   type='option',
                   group_type=None):
        """List options (by default list only option)"""
        assert type in ('all', 'option', 'optiondescription'), _('unknown list type {}').format(type)
        assert group_type is None or isinstance(group_type, groups.GroupType), \
                _("unknown group_type: {0}").format(group_type)
        config_bag = self._option_bag.config_bag
        if config_bag.properties and 'warnings' in config_bag.properties:
            config_bag = config_bag.copy()
            config_bag.remove_warnings()
        option = self._option_bag.option
        option_bag = OptionBag()
        option_bag.set_option(option,
                              None,
                              config_bag)
        subconfig = await self._subconfig.get_subconfig(option_bag)
        options = []
        for opt in await option.get_children(config_bag):
            try:
                await self._filter(opt,
                                   subconfig,
                                   config_bag)
            except PropertiesOptionError:
                continue
            if opt.impl_is_optiondescription():
                if type == 'option' or (type == 'optiondescription' and \
                        group_type and opt.impl_get_group_type() != group_type):
                    continue
            elif type == 'optiondescription':
                continue
            options.append(TiramisuOption(opt.impl_getpath(),
                                          None,
                                          self._option_bag.config_bag))
        return options

    async def _load_dict(self,
                         clearable: str="all",
                         remotable: str="minimum"):
        root = self._option_bag.option.impl_getpath()
        config = self._option_bag.config_bag.context
        self._tiramisu_dict = TiramisuDict(await self._return_config(config,
                                                                     config._storage),
                                           root=root,
                                           clearable=clearable,
                                           remotable=remotable)

    @option_type('optiondescription')
    async def dict(self,
             clearable: str="all",
             remotable: str="minimum",
             form: List=[],
             force: bool=False) -> Dict:
        """convert config and option to tiramisu format"""
        if force or self._tiramisu_dict is None:
            await self._load_dict(clearable, remotable)
        return await self._tiramisu_dict.todict(form)

    @option_type('optiondescription')
    async def updates(self,
                      body: List) -> Dict:
        """updates value with tiramisu format"""
        if self._tiramisu_dict is None:
            await self._load_dict()
        return await self._tiramisu_dict.set_updates(body)


def connection(func):
    async def wrapped(self, *args, **kwargs):
        config_bag = self._config_bag
        async with config_bag.context.getconnection() as connection:
            config_bag.connection = connection
            ret = await func(self, *args, **kwargs)
            del config_bag.connection
            return ret
    return wrapped


class TiramisuContextInformation(TiramisuConfig):
    """Manage config informations"""
    @connection
    async def get(self, name, default=undefined):
        """Get an information"""
        return await self._config_bag.context.impl_get_information(self._config_bag.connection,
                                                                   name,
                                                                   default)

    @connection
    async def set(self, name, value):
        """Set an information"""
        await self._config_bag.context.impl_set_information(self._config_bag.connection,
                                                            name,
                                                            value)

    @connection
    async def reset(self, name):
        """Remove an information"""
        await self._config_bag.context.impl_del_information(self._config_bag.connection,
                                                            name)

    @connection
    async def list(self):
        """List information's keys"""
        return await self._config_bag.context.impl_list_information(self._config_bag.connection)


class TiramisuContextValue(TiramisuConfig):
    """Manage config value"""
    @connection
    async def mandatory(self):
        """Return path of options with mandatory property without any value"""
        options = []
        async for option in self._config_bag.context.cfgimpl_get_values().mandatory_warnings(self._config_bag):
            options.append(option)
        return options

    # FIXME should be only for group/meta
    @connection
    async def set(self,
                  path: str,
                  value,
                  index=None,
                  only_config=undefined,
                  force_default=undefined,
                  force_default_if_same=undefined,
                  force_dont_change_value=undefined):
        """Set a value in config or children for a path"""
        kwargs = {}
        if only_config is not undefined:
            kwargs['only_config'] = only_config
        if force_default is not undefined:
            kwargs['force_default'] = force_default
        if force_default_if_same is not undefined:
            kwargs['force_default_if_same'] = force_default_if_same
        if force_dont_change_value is not undefined:
            kwargs['force_dont_change_value'] = force_dont_change_value
        return await self._config_bag.context.set_value(path,
                                                        index,
                                                        value,
                                                        self._config_bag,
                                                        **kwargs)

    # FIXME should be only for group/meta
    @connection
    async def reset(self,
              path: str,
              only_children: bool=False):
        """Reset value"""
        await self._config_bag.context.reset(path,
                                             only_children,
                                             self._config_bag)

    @connection
    async def dict(self,
                   flatten=False,
                   withwarning: bool=False,
                   fullpath=False,
                   leader_to_list=False):
        """Dict with path as key and value"""
        config_bag = self._config_bag
        if not withwarning and 'warnings' in config_bag.properties:
            config_bag = config_bag.copy()
            config_bag.remove_warnings()
        return await config_bag.context.make_dict(config_bag,
                                                  flatten=flatten,
                                                  fullpath=fullpath,
                                                  leader_to_list=leader_to_list)

    @connection
    async def exportation(self,
                          with_default_owner: bool=False):
        """Export all values"""
        exportation = await self._config_bag.context.cfgimpl_get_values()._p_.exportation(self._config_bag.connection)
        if not with_default_owner:
            exportation = [list(exportation[0]), list(exportation[1]), list(exportation[2]), list(exportation[3])]
            index = exportation[0].index(None)
            exportation[0].pop(index)
            exportation[1].pop(index)
            exportation[2].pop(index)
            exportation[3].pop(index)
        return exportation

    @connection
    async def importation(self, values):
        """Import values"""
        cvalues = self._config_bag.context.cfgimpl_get_values()
        connection = self._config_bag.connection
        if None not in values[0]:
            context_owner = await cvalues.get_context_owner(connection)
        else:
            context_owner = None
        await cvalues._p_.importation(connection,
                                      values)
        await self._config_bag.context.cfgimpl_reset_cache(None, None)
        if context_owner is not None:
            await cvalues._p_.setvalue(connection,
                                       None,
                                       None,
                                       context_owner,
                                       None,
                                       True)


class TiramisuContextSession(TiramisuConfig):
    """Manage Config session"""
    async def reset(self):
        await self._config_bag.context.cfgimpl_get_values()._p_._storage.delete_session()
        await self._config_bag.context.cfgimpl_get_settings()._p_._storage.delete_session()

    async def list(self):
        return await self._config_bag.context.cfgimpl_get_values()._p_._storage.list_sessions()

    async def id(self):
        """Get config name"""
        return self._config_bag.context.impl_getname()


class TiramisuContextOwner(TiramisuConfig):
    """Global owner"""
    @connection
    async def get(self):
        """Get owner"""
        return await self._config_bag.context.cfgimpl_get_values().get_context_owner(self._config_bag.connection)

    @connection
    async def set(self, owner):
        """Set owner"""
        try:
            obj_owner = getattr(owners, owner)
        except AttributeError:
            owners.addowner(owner)
            obj_owner = getattr(owners, owner)
        values = self._config_bag.context.cfgimpl_get_values()
        await values.set_context_owner(self._config_bag.connection,
                                       obj_owner)


class TiramisuContextProperty(TiramisuConfig):
    """Manage config properties"""
    @connection
    async def read_only(self):
        """Set config to read only mode"""
        old_props = self._config_bag.properties
        settings = self._config_bag.context.cfgimpl_get_settings()
        await settings.read_only(self._config_bag)
        await self._reset_config_properties(self._config_bag.connection)
        if 'force_store_value' not in old_props and \
                'force_store_value' in self._config_bag.properties:
            await self._force_store_value()

    @connection
    async def read_write(self):
        """Set config to read and write mode"""
        old_props = self._config_bag.properties
        settings = self._config_bag.context.cfgimpl_get_settings()
        connection = self._config_bag.connection
        await settings.read_write(self._config_bag)
        or_properties = settings.rw_append - settings.ro_append - SPECIAL_PROPERTIES
        permissives = frozenset(await settings.get_context_permissives(connection) | or_properties)
        await settings.set_context_permissives(connection,
                                               permissives)
        await self._reset_config_properties(connection)
        if 'force_store_value' not in old_props and \
                'force_store_value' in self._config_bag.properties:
            await self._force_store_value()

    @connection
    async def add(self, prop):
        """Add a config property"""
        settings = self._config_bag.context.cfgimpl_get_settings()
        props = set(await self.get())
        if prop not in props:
            props.add(prop)
            await self._set(self._config_bag.connection, frozenset(props))

    @connection
    async def pop(self, prop):
        """Remove a config property"""
        props = set(await self.get())
        if prop in props:
            props.remove(prop)
            await self._set(self._config_bag.connection, frozenset(props))

    async def get(self,
                  default=False):
        """Get all config properties"""
        if default:
            config = self._config_bag.context
            async with config.getconnection() as connection:
                properties = await config.cfgimpl_get_settings().get_context_properties(connection,
                                                                                        config._impl_properties_cache)
        return self._config_bag.properties

    async def _set(self,
                   connection,
                   props):
        """Personalise config properties"""
        if 'force_store_value' in props:
            force_store_value = 'force_store_value' not in self._config_bag.properties
        else:
            force_store_value = False
        context = self._config_bag.context
        await context.cfgimpl_get_settings().set_context_properties(self._config_bag.connection,
                                                                    props,
                                                                    self._config_bag.context)
        await self._reset_config_properties(connection)
        if force_store_value:
            await self._force_store_value()

    @connection
    async def reset(self):
        """Remove config properties"""
        context = self._config_bag.context
        await context.cfgimpl_get_settings().reset(None,
                                                   self._config_bag)
        await self._reset_config_properties(self._config_bag.connection)

    @connection
    async def exportation(self):
        """Export config properties"""
        return await self._config_bag.context.cfgimpl_get_settings()._p_.exportation(self._config_bag.connection)

    @connection
    async def importation(self, properties):
        """Import config properties"""
        if 'force_store_value' in properties.get(None, {}).get(None, []):
            force_store_value = 'force_store_value' not in self._config_bag.properties
        else:
            force_store_value = False
        settings = self._config_bag.context.cfgimpl_get_settings()
        connection = self._config_bag.connection
        await self._config_bag.context.cfgimpl_get_settings()._p_.importation(connection,
                                                                              properties)
        await self._config_bag.context.cfgimpl_reset_cache(None, None)
        await self._reset_config_properties(connection)
        if force_store_value:
            await self._force_store_value()

    async def _force_store_value(self):
        descr = self._config_bag.context.cfgimpl_get_description()
        await descr.impl_build_force_store_values(self._config_bag)

    async def setdefault(self,
                   properties: Set[str],
                   type: Optional[str]=None,
                   when: Optional[str]=None) -> None:
        if not isinstance(properties, frozenset):
            raise TypeError(_('properties must be a frozenset'))
        setting = self._config_bag.context.cfgimpl_get_settings()
        if type is None and when is None:
            setting.default_properties = properties
        else:
            if when not in ['append', 'remove']:
                raise ValueError(_('unknown when {} (must be in append or remove)').format(when))
            if type == 'read_only':
                if when == 'append':
                    setting.ro_append = properties
                else:
                    setting.ro_remove = properties
            elif type == 'read_write':
                if when == 'append':
                    setting.rw_append = properties
                else:
                    setting.rw_remove = properties
            else:
                raise ValueError(_('unknown type {}').format(type))

    async def getdefault(self,
                         type: Optional[str]=None,
                         when: Optional[str]=None) -> Set[str]:
        setting = self._config_bag.context.cfgimpl_get_settings()
        if type is None and when is None:
            return setting.default_properties

        if when not in ['append', 'remove']:
            raise ValueError(_('unknown when {} (must be in append or remove)').format(when))
        if type == 'read_only':
            if when == 'append':
                return setting.ro_append
            else:
                return setting.ro_remove
        elif type == 'read_write':
            if when == 'append':
                return setting.rw_append
            else:
                return setting.rw_remove
        else:
            raise ValueError(_('unknown type {}').format(type))


class TiramisuContextPermissive(TiramisuConfig):
    """Manage config permissives"""
    @connection
    async def get(self):
        """Get config permissives"""
        return await self._get()

    async def _get(self):
        return await self._config_bag.context.cfgimpl_get_settings().get_context_permissives(self._config_bag.connection)

    async def _set(self,
                   permissives):
        """Set config permissives"""
        connection = self._config_bag.connection
        await self._config_bag.context.cfgimpl_get_settings().set_context_permissives(connection, permissives)
        await self._reset_config_properties(connection)

    @connection
    async def exportation(self):
        """Export config permissives"""
        return await self._config_bag.context.cfgimpl_get_settings()._pp_.exportation(self._config_bag.connection)

    @connection
    async def importation(self, permissives):
        """Import config permissives"""
        settings = self._config_bag.context.cfgimpl_get_settings()
        connection = self._config_bag.connection
        await settings._pp_.importation(connection,
                                        permissives)
        await self._config_bag.context.cfgimpl_reset_cache(None,
                                                           None)
        await self._reset_config_properties(connection)

    @connection
    async def reset(self):
        """Remove config permissives"""
        context = self._config_bag.context
        settings = context.cfgimpl_get_settings()
        connection = self._config_bag.connection
        await settings.reset_permissives(None,
                                         self._config_bag)
        await self._reset_config_properties(connection)

    @connection
    async def add(self, prop):
        """Add a config permissive"""
        props = set(await self._get())
        props.add(prop)
        await self._set(frozenset(props))

    @connection
    async def pop(self, prop):
        """Remove a config permissive"""
        props = set(await self._get())
        if prop in props:
            props.remove(prop)
            await self._set(frozenset(props))


class TiramisuContextOption(TiramisuConfig):
    def __init__(self,
                 *args,
                 **kwargs) -> None:
        self._tiramisu_dict = None
        super().__init__(*args, **kwargs)

    @connection
    async def find(self,
                   name,
                   value=undefined,
                   type=None,
                   first=False):
        """Find an or a list of options"""
        options = []
        context = self._config_bag.context
        async for path in context.find(byname=name,
                                       byvalue=value,
                                       bytype=type,
                                       config_bag=self._config_bag):
            option = TiramisuOption(path,
                                    None,
                                    self._config_bag)
            if first:
                return option
            options.append(option)
        return options

    async def _filter(self,
                      opt,
                      subconfig,
                      config_bag):
        option_bag = OptionBag()
        option_bag.set_option(opt,
                              None,
                              config_bag)
        settings = config_bag.context.cfgimpl_get_settings()
        option_bag.properties = await settings.getproperties(option_bag)
        if opt.impl_is_optiondescription():
            await settings.validate_properties(option_bag)
            return await subconfig.get_subconfig(option_bag)
        await subconfig.getattr(opt.impl_getname(),
                                option_bag)

    async def _walk(self,
              option,
              recursive,
              type_,
              group_type,
              config_bag,
              subconfig):
        options = []
        for opt in await option.get_children(config_bag):
            try:
                subsubconfig = await self._filter(opt,
                                                  subconfig,
                                                  config_bag)
            except PropertiesOptionError:
                continue
            if opt.impl_is_optiondescription():
                if recursive:
                    options.extend(await self._walk(opt,
                                                    recursive,
                                                    type_,
                                                    group_type,
                                                    config_bag,
                                                    subsubconfig))
                if type_ == 'option' or (type_ == 'optiondescription' and \
                        group_type and opt.impl_get_group_type() != group_type):
                    continue
            elif type_ == 'optiondescription':
                continue
            options.append(TiramisuOption(opt.impl_getpath(),
                                          None,
                                          self._config_bag))
        return options

    @connection
    async def list(self,
                   type='option',
                   group_type=None,
                   recursive=False):
        """List options (by default list only option)"""
        assert type in ('all', 'option', 'optiondescription'), _('unknown list type {}').format(type)
        assert group_type is None or isinstance(group_type, groups.GroupType), \
                _("unknown group_type: {0}").format(group_type)
        config_bag = self._config_bag
        if config_bag.properties and 'warnings' in config_bag.properties:
            config_bag = config_bag.copy()
            config_bag.remove_warnings()
        option = config_bag.context.cfgimpl_get_description()
        options = []
        for opt in await self._walk(option,
                                    recursive,
                                    type,
                                    group_type,
                                    config_bag,
                                    config_bag.context):
            options.append(opt)
        return options

    async def _load_dict(self,
                         clearable="all",
                         remotable="minimum"):
        self._tiramisu_dict = TiramisuDict(await self._return_config(self._config_bag.context,
                                                                     self._config_bag.context._storage),
                                           root=None,
                                           clearable=clearable,
                                           remotable=remotable)

    async def dict(self,
                   clearable="all",
                   remotable="minimum",
                   form=[],
                   force=False):
        """convert config and option to tiramisu format"""
        if force or self._tiramisu_dict is None:
            await self._load_dict(clearable, remotable)
        return await self._tiramisu_dict.todict(form)

    async def updates(self,
                      body: List) -> Dict:
        """updates value with tiramisu format"""
        if self._tiramisu_dict is None:
            await self._load_dict()
        return await self._tiramisu_dict.set_updates(body)


class _TiramisuContextConfigReset():
    @connection
    async def reset(self):
        """Remove all datas to current config (informations, values, properties, ...)"""
        # Option's values
        settings = self._config_bag.context.cfgimpl_get_settings()
        connection = self._config_bag.connection
        context_owner = await self._config_bag.context.cfgimpl_get_values().get_context_owner(connection)
        await self._config_bag.context.cfgimpl_get_values()._p_.importation(connection, ([], [], [], []))
        await self._config_bag.context.cfgimpl_get_values()._p_.setvalue(connection,
                                                                         None,
                                                                         None,
                                                                         context_owner,
                                                                         None,
                                                                         True)
        # Option's informations
        await self._config_bag.context.cfgimpl_get_values()._p_.del_informations(connection)
        # Option's properties
        await self._config_bag.context.cfgimpl_get_settings()._p_.importation(connection, {})
        # Option's permissives
        await self._config_bag.context.cfgimpl_get_settings()._pp_.importation(connection, {})
        # Remove cache
        await self._config_bag.context.cfgimpl_reset_cache(None, None)


class _TiramisuContextConfig(TiramisuConfig, _TiramisuContextConfigReset):
    """Actions to Config"""
    async def type(self):
        """Type a Config"""
        return 'config'

    async def copy(self,
                   session_id=None,
                   storage=None):
        """Copy current config"""
        if storage is None:
            storage = self._config_bag.context._storage
        async with self._config_bag.context.getconnection() as connection:
            config = await self._config_bag.context.duplicate(connection,
                                                              session_id,
                                                              storage=storage)
        return await self._return_config(config,
                                         storage)

    async def deepcopy(self,
                       session_id=None,
                       storage=None,
                       metaconfig_prefix=None):
        """Copy current config with all parents"""
        if storage is None:
            storage = self._config_bag.context._storage
        async with self._config_bag.context.getconnection() as connection:
            config = await self._config_bag.context.duplicate(connection,
                                                              session_id,
                                                              storage=storage,
                                                              metaconfig_prefix=metaconfig_prefix,
                                                              deep=[])
        return await self._return_config(config,
                                         storage)

    async def metaconfig(self):
        """Get first meta configuration (obsolete please use parents)"""
        parent = await self.parents()
        if not parent:
            return None
        return parent[0]

    async def parents(self):
        """Get all parents of current config"""
        ret = []
        for parent in self._config_bag.context.get_parents():
            ret.append(await self._return_config(parent,
                                                 parent._storage))
        return ret

    async def path(self):
        """Get path from config (all parents name)"""
        return self._config_bag.context.cfgimpl_get_config_path()


class _TiramisuContextGroupConfig(TiramisuConfig):
    """Actions to GroupConfig"""
    async def type(self):
        """Type a Config"""
        return 'groupconfig'

    async def list(self):
        """List children's config"""
        ret = []
        for child in self._config_bag.context.cfgimpl_get_children():
            ret.append(await self._return_config(child,
                                                 child._storage))
        return ret

    @connection
    async def find(self,
                   name: str,
                   value=undefined):
        """Find an or a list of config with finding option"""
        return await GroupConfig(await self._config_bag.context.find_group(byname=name,
                                                                           byvalue=value,
                                                                           config_bag=self._config_bag))

    def __call__(self,
                 path: Optional[str]):
        """select a child Tiramisu config"""
        spaths = path.split('.')
        config = self._config_bag.context
        for spath in spaths:
            config = config.getconfig(spath)
        if isinstance(config, KernelGroupConfig):
            return self._return_config(config,
                                       None)
        return self._return_config(config,
                                   config._storage)


    async def copy(self,
                   session_id=None,
                   storage=None):
        if storage is None:
            storage = self._config_bag.context._storage
        async with self._config_bag.context.getconnection() as connection:
            config = await self._config_bag.context.duplicate(connection,
                                                              session_id,
                                                              storage=storage)
        return await self._return_config(config,
                                         storage)

    async def deepcopy(self,
                       session_id=None,
                       storage=None,
                       metaconfig_prefix=None):
        if storage is None:
            storage = self._config_bag.context._storage
        async with self._config_bag.context.getconnection() as connection:
            config = await self._config_bag.context.duplicate(connection,
                                                              session_id,
                                                              storage=storage,
                                                              metaconfig_prefix=metaconfig_prefix,
                                                              deep=[])
        return await self._return_config(config,
                                         storage)

    async def path(self):
        return self._config_bag.context.cfgimpl_get_config_path()

    async def get(self,
                  name: str) -> 'Config':
        config = self._config_bag.context.getconfig(name)
        return await self._return_config(config,
                                         config._storage)


class _TiramisuContextMixConfig(_TiramisuContextGroupConfig, _TiramisuContextConfigReset):
    """Actions to MixConfig"""
    async def type(self):
        """Type a Config"""
        return 'mixconfig'

    async def new(self,
                  session_id,
                  storage=None,
                  type='config',
                  new=None):
        """Create and add a new config"""
        config = self._config_bag.context
        if storage is None:
            storage = config._storage
        storage_obj = await storage.get()
        async with storage_obj.Connection() as connection:
            new_config = await config.new_config(connection,
                                                 session_id=session_id,
                                                 storage=storage,
                                                 type_=type,
                                                 new=new)
        return await self._return_config(new_config,
                                         storage)

    async def pop(self,
                  session_id=None,
                  config=None):
        """Remove config from MetaConfig"""
        if __debug__ and None not in [session_id, config]:
            raise APIError(_('cannot set session_id and config together'))
        pop_config = await self._config_bag.context.pop_config(session_id=session_id, config=config)
        return await self._return_config(pop_config,
                                         pop_config._storage)

    async def add(self,
                  config):
        """Add config from MetaConfig"""
        await self._config_bag.context.add_config(config)

    async def parents(self):
        """Get all parents of current config"""
        ret = []
        for parent in self._config_bag.context.get_parents():
            ret.append(await self._return_config(parent,
                                                 parent._storage))
        return ret


class _TiramisuContextMetaConfig(_TiramisuContextMixConfig):
    """Actions to MetaConfig"""
    async def type(self):
        """Type a Config"""
        return 'metaconfig'


class TiramisuContextCache(TiramisuConfig):
    async def reset(self):
        await self._config_bag.context.cfgimpl_reset_cache(None, None)

    async def set_expiration_time(self,
                            time: int) -> None:
        self._config_bag.expiration_time = time

    async def get_expiration_time(self) -> int:
        return self._config_bag.expiration_time


class TiramisuAPI(TiramisuHelp):
    _registers = {}

    def __init__(self,
                 config_bag,
                 orig_config_bags=None) -> None:
        self._config_bag = config_bag
        self._orig_config_bags = orig_config_bags
        if not self._registers:
            _registers(self._registers, 'TiramisuContext')

    def __getattr__(self, subfunc: str) -> Any:
        if subfunc == 'option':
            config_bag = self._config_bag
            return TiramisuDispatcherOption(config_bag,
                                            self._orig_config_bags)
        elif subfunc == 'forcepermissive':
            config_bag = self._config_bag.copy()
            config_bag.set_permissive()
            if self._orig_config_bags is None:
                orig_config_bags = []
            else:
                orig_config_bags = self._orig_config_bags
            orig_config_bags.append(self._config_bag)
            return TiramisuAPI(config_bag, orig_config_bags)
        elif subfunc == 'unrestraint':
            config_bag = self._config_bag.copy()
            config_bag.unrestraint()
            if self._orig_config_bags is None:
                orig_config_bags = []
            else:
                orig_config_bags = self._orig_config_bags
            orig_config_bags.append(self._config_bag)
            return TiramisuAPI(config_bag, orig_config_bags)
        elif subfunc == 'config':
            config_type = self._config_bag.context.impl_type
            if config_type == 'group':
                config = _TiramisuContextGroupConfig
            elif config_type == 'meta':
                config = _TiramisuContextMetaConfig
            elif config_type == 'mix':
                config = _TiramisuContextMixConfig
            else:
                config = _TiramisuContextConfig
            return config(self._config_bag,
                          self._orig_config_bags)
        elif subfunc in self._registers:
            config_bag = self._config_bag
            # del config_bag.permissives
            return self._registers[subfunc](config_bag,
                                            self._orig_config_bags)
        raise APIError(_('please specify a valid sub function ({})').format(subfunc))

    def __dir__(self):
        return list(self._registers.keys()) + ['unrestraint', 'forcepermissive', 'config']


class TiramisuDispatcherOption(TiramisuContextOption):
    """Select an option"""
    def __call__(self,
                 path: str,
                 index: Optional[int]=None) -> TiramisuOption:
        """Select an option by path"""
        return TiramisuOption(path,
                              index,
                              self._config_bag)

    async def __getattr__(self,
                          subfunc: str) -> Any:
        if subfunc == 'unrestraint':
            config_bag = self._config_bag.copy()
            config_bag.unrestraint()
            return TiramisuDispatcherOption(config_bag)


@asyncinit
class Config(TiramisuAPI):
    """Root config object that enables us to handle the configuration options"""
    async def __init__(self,
                       descr: OptionDescription,
                       session_id: str=None,
                       delete_old_session: bool=False,
                       storage=None,
                       display_name=None) -> None:
        if storage is None:
            storage = default_storage
        storage_obj = await storage.get()
        async with storage_obj.Connection() as connection:
            if isinstance(descr, KernelConfig):
                config = descr
            else:
                config = await KernelConfig(descr,
                                            connection=connection,
                                            session_id=session_id,
                                            delete_old_session=delete_old_session,
                                            storage=storage,
                                            display_name=display_name)
            settings = config.cfgimpl_get_settings()
            properties = await settings.get_context_properties(connection,
                                                               config._impl_properties_cache)
            permissives = await settings.get_context_permissives(connection)
        config_bag = ConfigBag(config,
                               properties=properties,
                               permissives=permissives)
        super().__init__(config_bag)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._config_bag.context.cfgimpl_get_values()._p_._storage.delete_session()
        await self._config_bag.context.cfgimpl_get_settings()._p_._storage.delete_session()

    def __del__(self):
        try:
            del self._config_bag.context
            del self._config_bag
            del self._orig_config_bags
        except:
            pass


@asyncinit
class MetaConfig(TiramisuAPI):
    """MetaConfig object that enables us to handle the sub configuration's options"""
    async def __init__(self,
                       children: 'Config'=[],
                       session_id: Union[str, None]=None,
                       delete_old_session: bool=False,
                       optiondescription: Optional[OptionDescription]=None,
                       storage=None,
                       display_name=None) -> None:
        if storage is None:
            storage = default_storage
        storage_obj = await storage.get()
        async with storage_obj.Connection() as connection:
            if isinstance(children, KernelMetaConfig):
                config = children
            else:
                _children = []
                for child in children:
                    if isinstance(child, TiramisuAPI):
                        _children.append(child._config_bag.context)
                    else:
                        _children.append(child)

                config = await KernelMetaConfig(_children,
                                                connection=connection,
                                                session_id=session_id,
                                                delete_old_session=delete_old_session,
                                                optiondescription=optiondescription,
                                                display_name=display_name,
                                                storage=storage)
            settings = config.cfgimpl_get_settings()
            properties = await settings.get_context_properties(connection,
                                                               config._impl_properties_cache)
            permissives = await settings.get_context_permissives(connection)
        config_bag = ConfigBag(config,
                               properties=properties,
                               permissives=permissives)
        super().__init__(config_bag)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._config_bag.context.cfgimpl_get_values()._p_._storage.delete_session()
        await self._config_bag.context.cfgimpl_get_settings()._p_._storage.delete_session()


@asyncinit
class MixConfig(TiramisuAPI):
    """MetaConfig object that enables us to handle the sub configuration's options"""
    async def __init__(self,
                       optiondescription: OptionDescription,
                       children: List[Config],
                       session_id: Optional[str]=None,
                       delete_old_session: bool=False,
                       storage=None,
                       display_name: Callable=None) -> None:
        if storage is None:
            storage = default_storage
        storage_obj = await storage.get()
        async with storage_obj.Connection() as connection:
            if isinstance(children, KernelMixConfig):
                config = children
            else:
                _children = []
                for child in children:
                    if isinstance(child, TiramisuAPI):
                        _children.append(child._config_bag.context)
                    else:
                        _children.append(child)

                config = await KernelMixConfig(optiondescription,
                                               _children,
                                               session_id=session_id,
                                               delete_old_session=delete_old_session,
                                               storage=storage,
                                               connection=connection,
                                               display_name=display_name)
            settings = config.cfgimpl_get_settings()
            properties = await settings.get_context_properties(connection,
                                                               config._impl_properties_cache)
            permissives = await settings.get_context_permissives(connection)
        config_bag = ConfigBag(config,
                               properties=properties,
                               permissives=permissives)
        super().__init__(config_bag)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._config_bag.context.cfgimpl_get_values()._p_._storage.delete_session()
        await self._config_bag.context.cfgimpl_get_settings()._p_._storage.delete_session()


@asyncinit
class GroupConfig(TiramisuAPI):
    """GroupConfig that enables us to access the Config"""
    async def __init__(self,
                       children,
                       session_id: Optional[str]=None) -> None:
        if isinstance(children, KernelGroupConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = await KernelGroupConfig(_children,
                                             session_id=session_id)
        config_bag = ConfigBag(config,
                               properties=None,
                               permissives=None)
        super().__init__(config_bag)
