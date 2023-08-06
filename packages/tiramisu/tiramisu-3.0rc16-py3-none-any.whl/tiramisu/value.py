# -*- coding: utf-8 -*-
"takes care of the option's values and multi values"
# Copyright (C) 2013-2020 Team tiramisu (see AUTHORS for all contributors)
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
import weakref
from typing import Optional, Any, Callable
from .error import ConfigError, PropertiesOptionError
from .setting import owners, undefined, forbidden_owners, OptionBag, ConfigBag
from .autolib import Calculation, carry_out_calculation, Params
from .i18n import _
from .asyncinit import asyncinit


@asyncinit
class Values:
    """The `Config`'s root is indeed  in charge of the `Option()`'s values,
    but the values are physicaly located here, in `Values`, wich is also
    responsible of a caching utility.
    """
    __slots__ = ('_p_',
                 '__weakref__')

    async def __init__(self,
                       storage,
                       connection):
        """
        Initializes the values's dict.

        :param storage: where values or owners are stored

        """
        # store the storage
        self._p_ = storage
        # set default owner
        owner = await self._p_.getowner(connection,
                                        None,
                                        None,
                                        None)
        if owner is None:
            await self._p_.setvalue(connection,
                                    None,
                                    None,
                                    owners.user,
                                    None,
                                    new=True)

    #______________________________________________________________________
    # get value

    async def get_cached_value(self,
                               option_bag):
        """get value directly in cache if set
        otherwise calculated value and set it in cache

        :returns: value
        """
        # try to retrive value in cache
        setting_properties = option_bag.config_bag.properties
        cache = option_bag.config_bag.context._impl_values_cache
        is_cached, value, validated = cache.getcache(option_bag.path,
                                                     option_bag.config_bag.expiration_time,
                                                     option_bag.index,
                                                     setting_properties,
                                                     option_bag.properties,
                                                     'value')
        if not validated:
            # no cached value so get value
            value = await self.getvalue(option_bag)
            # validate value
            await option_bag.option.impl_validate(value,
                                                  option_bag,
                                                  check_error=True)
            # store value in cache
            validator = 'validator' in setting_properties and 'demoting_error_warning' not in setting_properties
            if not is_cached or validator:
                cache.setcache(option_bag.path,
                               option_bag.index,
                               value,
                               option_bag.properties,
                               setting_properties,
                               validator)
        if 'warnings' in setting_properties:
            await option_bag.option.impl_validate(value,
                                                  option_bag,
                                                  check_error=False)
        if isinstance(value, list):
            # return a copy, so value cannot be modified
            from copy import copy
            value = copy(value)
        # and return it
        return value

    async def force_to_metaconfig(self, option_bag):
        # force_metaconfig_on_freeze in config => to metaconfig
        # force_metaconfig_on_freeze in option + config is kernelconfig => to metaconfig
        settings = option_bag.config_bag.context.cfgimpl_get_settings()
        if 'force_metaconfig_on_freeze' in option_bag.properties:
            settings = option_bag.config_bag.context.cfgimpl_get_settings()
            if 'force_metaconfig_on_freeze' in option_bag.option.impl_getproperties() and \
                    not await settings._p_.getproperties(option_bag.config_bag.connection,
                                                         option_bag.path,
                                                         None,
                                                         frozenset()):
                # if force_metaconfig_on_freeze is only in option (not in config)
                return option_bag.config_bag.context.impl_type == 'config'
            else:
                return True
        return False

    async def _do_value_list(self,
                             value: Any,
                             option_bag: OptionBag):
        ret = []
        for val in value:
            if isinstance(val, (list, tuple)):
                ret.append(await self._do_value_list(val, option_bag))
            elif isinstance(val, Calculation):
                ret.append(await val.execute(option_bag))
            else:
                ret.append(val)
        return ret

    async def getvalue(self,
                       option_bag):
        """actually retrieves the value

        :param path: the path of the `Option`
        :param index: index for a follower `Option`

        :returns: value
        """

        # get owner and value from store
        # index allowed only for follower
        index = option_bag.index
        is_follower = option_bag.option.impl_is_follower()
        if index is None or not is_follower:
            _index = None
        else:
            _index = index
        owner, value = await self._p_.getowner(option_bag.config_bag.connection,
                                               option_bag.path,
                                               owners.default,
                                               index=_index,
                                               with_value=True)
        if owner == owners.default or \
                ('frozen' in option_bag.properties and \
                 ('force_default_on_freeze' in option_bag.properties or await self.force_to_metaconfig(option_bag))):
            value = await self.getdefaultvalue(option_bag)
        else:
            value = await self.calc_value(option_bag, value)
        return value

    async def calc_value(self,
                         option_bag,
                         value,
                         reset_cache=True):
        if isinstance(value, Calculation):
            value = await value.execute(option_bag,
                                        leadership_must_have_index=True)
        elif isinstance(value, (list, tuple)):
            value = await self._do_value_list(value, option_bag)
        if reset_cache:
            await self.calculate_reset_cache(option_bag, value)
        return value

    async def getdefaultvalue(self,
                              option_bag):
        """get default value:
        - get parents config value or
        - get calculated value or
        - get default value
        """
        moption_bag = await self._get_modified_parent(option_bag)
        if moption_bag is not None:
            # retrieved value from parent config
            return await moption_bag.config_bag.context.cfgimpl_get_values().get_cached_value(moption_bag)

        if option_bag.option.impl_has_callback():
            # default value is a calculated value
            value = await self.calculate_value(option_bag)
            if value is not undefined:
                return value

        # now try to get default value:
        value = await self.calc_value(option_bag,
                                      option_bag.option.impl_getdefault())
        if option_bag.option.impl_is_multi() and option_bag.index is not None and isinstance(value, (list, tuple)):
            # if index, must return good value for this index
            if len(value) > option_bag.index:
                value = value[option_bag.index]
            else:
                # no value for this index, retrieve default multi value
                # default_multi is already a list for submulti
                value = await self.calc_value(option_bag,
                                        option_bag.option.impl_getdefault_multi())
        return value

    async def calculate_reset_cache(self,
                                    option_bag,
                                    value):
        if not 'expire' in option_bag.properties:
            return
        cache = option_bag.config_bag.context._impl_values_cache
        is_cache, cache_value, validated = cache.getcache(option_bag.path,
                                                          None,
                                                          option_bag.index,
                                                          option_bag.config_bag.properties,
                                                          option_bag.properties,
                                                          'value')
        if not is_cache or cache_value == value:
            # calculation return same value as previous value,
            # so do not invalidate cache
            return
        # calculated value is a new value, so reset cache
        await option_bag.config_bag.context.cfgimpl_reset_cache(option_bag)

    async def calculate_value(self,
                              option_bag: OptionBag) -> Any:

        # if value has callback, calculate value
        callback, callback_params = option_bag.option.impl_get_callback()
        value = await self.carry_out_calculation(option_bag,
                                                 callback,
                                                 callback_params)
        if isinstance(value, list) and option_bag.index is not None:
            # if value is a list and index is set
            if option_bag.option.impl_is_submulti() and (value == [] or not isinstance(value[0], list)):
                # return value only if it's a submulti and not a list of list
                await self.calculate_reset_cache(option_bag, value)
                return value
            if len(value) > option_bag.index:
                # return the value for specified index if found
                await self.calculate_reset_cache(option_bag, value[option_bag.index])
                return value[option_bag.index]
            # there is no calculate value for this index,
            # so return an other default value
        else:
            if option_bag.option.impl_is_submulti():
                if isinstance(value, list):
                    # value is a list, but no index specified
                    if (value != [] and not isinstance(value[0], list)):
                        # if submulti, return a list of value
                        value = [value]
                elif option_bag.index is not None:
                    # if submulti, return a list of value
                    value = [value]
                else:
                    # return a list of list for a submulti
                    value = [[value]]
            elif option_bag.option.impl_is_multi() and not isinstance(value, list) and option_bag.index is None:
                # return a list for a multi
                value = [value]
            await self.calculate_reset_cache(option_bag, value)
            return value
        return undefined

    async def carry_out_calculation(self,
                                    option_bag: OptionBag,
                                    callback: Callable,
                                    callback_params: Optional[Params]) -> Any:
        return await carry_out_calculation(option_bag.option,
                                           callback=callback,
                                           callback_params=callback_params,
                                           index=option_bag.index,
                                           config_bag=option_bag.config_bag)
    def isempty(self,
                opt,
                value,
                force_allow_empty_list=False,
                index=None):
        "convenience method to know if an option is empty"
        empty = opt._empty
        if index in [None, undefined] and opt.impl_is_multi():
            isempty = value is None or (not force_allow_empty_list and value == []) or \
                None in value or empty in value
        else:
            isempty = value is None or value == empty or (opt.impl_is_submulti() and value == [])
        return isempty

    #______________________________________________________________________
    # set value
    async def setvalue(self,
                       value,
                       option_bag):
        context = option_bag.config_bag.context
        owner = await self.get_context_owner(option_bag.config_bag.connection)
        if 'validator' in option_bag.config_bag.properties:
            await self.setvalue_validation(value,
                                           option_bag)

        if isinstance(value, list):
            # copy
            value = value.copy()
        await self._setvalue(option_bag,
                             value,
                             owner)
        setting_properties = option_bag.config_bag.properties
        validator = 'validator' in setting_properties and 'demoting_error_warning' not in setting_properties
        if validator:
            cache = option_bag.config_bag.context._impl_values_cache
            cache.setcache(option_bag.path,
                           option_bag.index,
                           value,
                           option_bag.properties,
                           setting_properties,
                           validator)
        if 'force_store_value' in setting_properties and option_bag.option.impl_is_leader():
            await option_bag.option.impl_get_leadership().follower_force_store_value(self,
                                                                                     value,
                                                                                     option_bag,
                                                                                     owners.forced)

    async def setvalue_validation(self,
                                  value,
                                  option_bag):
        settings = option_bag.config_bag.context.cfgimpl_get_settings()
        # First validate properties with this value
        opt = option_bag.option
        settings.validate_frozen(option_bag)
        val = await self.calc_value(option_bag, value, False)
        settings.validate_mandatory(val,
                                    option_bag)
        # Value must be valid for option
        await opt.impl_validate(val,
                                option_bag,
                                check_error=True)
        if 'warnings' in option_bag.config_bag.properties:
            # No error found so emit warnings
            await opt.impl_validate(value,
                                    option_bag,
                                    check_error=False)

    async def _setvalue(self,
                        option_bag,
                        value,
                        owner):
        await option_bag.config_bag.context.cfgimpl_reset_cache(option_bag)
        await self._p_.setvalue(option_bag.config_bag.connection,
                                option_bag.path,
                                value,
                                owner,
                                option_bag.index)

    async def _get_modified_parent(self,
                                   option_bag: OptionBag) -> Optional[OptionBag]:
        """ Search in differents parents a Config with a modified value
        If not found, return None
        For follower option, return the Config where leader is modified
        """
        def build_option_bag(option_bag, parent):
            doption_bag = option_bag.copy()
            config_bag = option_bag.config_bag.copy()
            config_bag.context = parent
            config_bag.unrestraint()
            doption_bag.config_bag = config_bag
            return doption_bag

        for parent in option_bag.config_bag.context.get_parents():
            doption_bag = build_option_bag(option_bag, parent)
            if 'force_metaconfig_on_freeze' in option_bag.properties:
                # remove force_metaconfig_on_freeze only if option in metaconfig
                # hasn't force_metaconfig_on_freeze properties
                ori_properties = doption_bag.properties
                doption_bag.properties = await doption_bag.config_bag.context.cfgimpl_get_settings().getproperties(doption_bag)
                if not await self.force_to_metaconfig(doption_bag):
                    doption_bag.properties = ori_properties - {'force_metaconfig_on_freeze'}
                else:
                    doption_bag.properties = ori_properties
            parent_owner = await parent.cfgimpl_get_values().getowner(doption_bag,
                                                                      only_default=True)
            if parent_owner != owners.default:
                return doption_bag

        return None


    #______________________________________________________________________
    # owner

    async def is_default_owner(self,
                               option_bag,
                               validate_meta=True):
        return await self.getowner(option_bag,
                                   validate_meta=validate_meta,
                                   only_default=True) == owners.default

    async def getowner(self,
                       option_bag,
                       validate_meta=True,
                       only_default=False):
        """
        retrieves the option's owner

        :param opt: the `option.Option` object
        :param force_permissive: behaves as if the permissive property
                                 was present
        :returns: a `setting.owners.Owner` object
        """
        context = option_bag.config_bag.context
        opt = option_bag.option
        if opt.impl_is_symlinkoption():
            option_bag.ori_option = opt
            opt = opt.impl_getopt()
            option_bag.option = opt
            option_bag.path = opt.impl_getpath()
        settings = context.cfgimpl_get_settings()
        await settings.validate_properties(option_bag)
        if 'frozen' in option_bag.properties and \
                'force_default_on_freeze' in option_bag.properties:
            return owners.default
        if only_default:
            if await self._p_.hasvalue(option_bag.config_bag.connection,
                                       option_bag.path,
                                       option_bag.index):
                owner = 'not_default'
            else:
                owner = owners.default
        else:
            owner = await self._p_.getowner(option_bag.config_bag.connection,
                                            option_bag.path,
                                            owners.default,
                                            index=option_bag.index)
        if validate_meta is not False and (owner is owners.default or \
                                           'frozen' in option_bag.properties and 'force_metaconfig_on_freeze' in option_bag.properties):
            moption_bag = await self._get_modified_parent(option_bag)
            if moption_bag is not None:
                owner = await moption_bag.config_bag.context.cfgimpl_get_values().getowner(moption_bag,
                                                                                           only_default=only_default)
            elif 'force_metaconfig_on_freeze' in option_bag.properties:
                return owners.default
        return owner

    async def setowner(self,
                       owner,
                       option_bag):
        """
        sets a owner to an option

        :param opt: the `option.Option` object
        :param owner: a valid owner, that is a `setting.owners.Owner` object
        """
        opt = option_bag.option
        if opt.impl_is_symlinkoption():
            raise ConfigError(_("can't set owner for the symlinkoption \"{}\""
                                "").format(opt.impl_get_display_name()))
        if owner in forbidden_owners:
            raise ValueError(_('set owner "{0}" is forbidden').format(str(owner)))

        if not await self._p_.hasvalue(option_bag.config_bag.connection,
                                       option_bag.path):
            raise ConfigError(_('no value for {0} cannot change owner to {1}'
                                '').format(option_bag.path, owner))
        option_bag.config_bag.context.cfgimpl_get_settings().validate_frozen(option_bag)
        await self._p_.setowner(option_bag.config_bag.connection,
                                option_bag.path,
                                owner,
                                index=option_bag.index)
    #______________________________________________________________________
    # reset

    async def reset(self,
                    option_bag):
        context = option_bag.config_bag.context
        hasvalue = await self._p_.hasvalue(option_bag.config_bag.connection,
                                           option_bag.path)
        setting_properties = option_bag.config_bag.properties

        if hasvalue and 'validator' in option_bag.config_bag.properties:
            fake_context = await context._gen_fake_values(option_bag.config_bag.connection)
            config_bag = option_bag.config_bag.copy()
            config_bag.remove_validation()
            config_bag.context = fake_context
            soption_bag = option_bag.copy()
            soption_bag.config_bag = config_bag
            fake_value = fake_context.cfgimpl_get_values()
            await fake_value.reset(soption_bag)
            soption_bag.config_bag.properties = option_bag.config_bag.properties
            value = await fake_value.getdefaultvalue(soption_bag)
            await fake_value.setvalue_validation(value,
                                                 soption_bag)
        opt = option_bag.option
        if opt.impl_is_leader():
            await opt.impl_get_leadership().reset(self,
                                                  option_bag)
        if hasvalue:
            if 'force_store_value' in option_bag.config_bag.properties and 'force_store_value' in option_bag.properties:
                value = await self.getdefaultvalue(option_bag)

                await self._setvalue(option_bag,
                                     value,
                                     owners.forced)
            else:
                # for leader only
                value = None
                await self._p_.resetvalue(option_bag.config_bag.connection,
                                          option_bag.path)
            await context.cfgimpl_reset_cache(option_bag)
            if 'force_store_value' in setting_properties and option_bag.option.impl_is_leader():
                if value is None:
                    value = await self.getdefaultvalue(option_bag)
                await option_bag.option.impl_get_leadership().follower_force_store_value(self,
                                                                                         value,
                                                                                         option_bag,
                                                                                         owners.forced)

    async def reset_follower(self,
                             option_bag):
        if await self._p_.hasvalue(option_bag.config_bag.connection,
                                   option_bag.path,
                                   index=option_bag.index):
            context = option_bag.config_bag.context
            setting_properties = option_bag.config_bag.properties
            if 'validator' in setting_properties:
                fake_context = await context._gen_fake_values(option_bag.config_bag.connection)
                fake_value = fake_context.cfgimpl_get_values()
                config_bag = option_bag.config_bag.copy()
                config_bag.remove_validation()
                config_bag.context = fake_context
                soption_bag = option_bag.copy()
                soption_bag.config_bag = config_bag
                await fake_value.reset_follower(soption_bag)
                value = await fake_value.getdefaultvalue(soption_bag)
                await fake_value.setvalue_validation(value,
                                                     soption_bag)
            if 'force_store_value' in setting_properties and 'force_store_value' in option_bag.properties:
                value = await self.getdefaultvalue(option_bag)

                await self._setvalue(option_bag,
                                     value,
                                     owners.forced)
            else:
                await self._p_.resetvalue_index(option_bag.config_bag.connection,
                                                option_bag.path,
                                                option_bag.index)
            await context.cfgimpl_reset_cache(option_bag)

    async def reset_leadership(self,
                               index,
                               option_bag,
                               subconfig):
        current_value = await self.get_cached_value(option_bag)
        length = len(current_value)
        if index >= length:
            raise IndexError(_('index {} is greater than the length {} '
                               'for option "{}"').format(index,
                                                         length,
                                                         option_bag.option.impl_get_display_name()))
        current_value.pop(index)
        await subconfig.cfgimpl_get_description().pop(self,
                                                      index,
                                                      option_bag)
        await self.setvalue(current_value,
                            option_bag)

    #______________________________________________________________________
    # information

    async def set_information(self,
                              connection,
                              key,
                              value,
                              path=None):
        """updates the information's attribute

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        await self._p_.set_information(connection,
                                       path,
                                       key,
                                       value)

    async def get_information(self,
                              connection,
                              key,
                              default=undefined,
                              path=None):
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        return await self._p_.get_information(connection,
                                              path,
                                              key,
                                              default)

    async def del_information(self,
                              connection,
                              key,
                              raises=True,
                              path=None):
        await self._p_.del_information(connection,
                                       path,
                                       key,
                                       raises)

    async def list_information(self,
                               connection,
                               path=None):
        return await self._p_.list_information(connection,
                                               path)

    #______________________________________________________________________
    # mandatory warnings
    async def _mandatory_warnings(self,
                                  context,
                                  config_bag,
                                  description,
                                  currpath,
                                  subconfig,
                                  od_config_bag):
        settings = context.cfgimpl_get_settings()
        for option in await description.get_children(config_bag):
            name = option.impl_getname()
            if option.impl_is_optiondescription():
                try:
                    option_bag = OptionBag()
                    option_bag.set_option(option,
                                          None,
                                          od_config_bag)
                    option_bag.properties = await settings.getproperties(option_bag)

                    subsubconfig = await subconfig.get_subconfig(option_bag)
                except PropertiesOptionError as err:
                    pass
                else:
                    async for option in  self._mandatory_warnings(context,
                                                                  config_bag,
                                                                  option,
                                                                  currpath + [name],
                                                                  subsubconfig,
                                                                  od_config_bag):
                        yield option
            elif not option.impl_is_symlinkoption():
                # don't verifying symlink
                try:
                    if not option.impl_is_follower():
                        option_bag = OptionBag()
                        option_bag.set_option(option,
                                              None,
                                              config_bag)
                        option_bag.properties = await settings.getproperties(option_bag)
                        if 'mandatory' in option_bag.properties or 'empty' in option_bag.properties:
                            await subconfig.getattr(name,
                                                    option_bag)
                    else:
                        for index in range(subconfig.cfgimpl_get_length()):
                            option_bag = OptionBag()
                            option_bag.set_option(option,
                                                  index,
                                                  config_bag)
                            option_bag.properties = await settings.getproperties(option_bag)
                            if 'mandatory' in option_bag.properties or 'empty' in option_bag.properties:
                                await subconfig.getattr(name,
                                                        option_bag)
                except PropertiesOptionError as err:
                    if err.proptype in (['mandatory'], ['empty']):
                        yield option.impl_getpath()
                except ConfigError:
                    pass

    async def mandatory_warnings(self,
                                 config_bag):
        """convenience function to trace Options that are mandatory and
        where no value has been set

        :returns: generator of mandatory Option's path
        """
        context = config_bag.context
        # copy
        od_setting_properties = config_bag.properties - {'mandatory', 'empty'}
        setting_properties = set(config_bag.properties) - {'warnings'}
        setting_properties.update(['mandatory', 'empty'])
        nconfig_bag = ConfigBag(context=config_bag.context,
                                properties=frozenset(setting_properties),
                                permissives=config_bag.permissives)
        nconfig_bag.connection = config_bag.connection
        nconfig_bag.set_permissive()
        od_config_bag = ConfigBag(context=nconfig_bag.context,
                                  properties=frozenset(od_setting_properties),
                                  permissives=nconfig_bag.permissives)
        od_config_bag.connection = config_bag.connection
        od_config_bag.set_permissive()

        descr = context.cfgimpl_get_description()
        async for option in  self._mandatory_warnings(context,
                                                      nconfig_bag,
                                                      descr,
                                                      [],
                                                      context,
                                                      od_config_bag):
            yield option

    #____________________________________________________________
    # default owner methods
    async def set_context_owner(self,
                                connection,
                                owner):
        ":param owner: sets the default value for owner at the Config level"
        if owner in forbidden_owners:
            raise ValueError(_('set owner "{0}" is forbidden').format(str(owner)))

        await self._p_.setowner(connection,
                                None,
                                owner,
                                index=None)

    async def get_context_owner(self,
                                connection):
        return await self._p_.getowner(connection,
                                       None,
                                       None,
                                       None)
