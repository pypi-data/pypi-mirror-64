# -*- coding: utf-8 -*-
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
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"options handler global entry point"
import weakref
from copy import copy


from .error import PropertiesOptionError, ConfigError, ConflictError, \
                   LeadershipError
from .option import SynDynOptionDescription, DynOptionDescription, Leadership
from .option.baseoption import BaseOption, valid_name
from .setting import OptionBag, ConfigBag, Settings, undefined, groups
from .storage import get_storages, gen_storage_id, get_default_values_storages, list_sessions, Cache
from .value import Values
from .i18n import _
from .asyncinit import asyncinit


@asyncinit
class SubConfig:
    """Sub configuration management entry.
    Tree if OptionDescription's responsability. SubConfig are generated
    on-demand. A Config is also a SubConfig.
    Root Config is call context below
    """
    __slots__ = ('_impl_context',
                 '_impl_descr',
                 '_impl_path',
                 '_impl_length')

    async def __init__(self,
                       descr,
                       context,
                       config_bag=None,
                       subpath=None):
        """ Configuration option management class

        :param descr: describes the configuration schema
        :type descr: an instance of ``option.OptionDescription``
        :param context: the current root config
        :type context: `Config`
        :type subpath: `str` with the path name
        """
        # main option description
        if __debug__ and descr is not None and \
                (not isinstance(descr, (BaseOption, SynDynOptionDescription)) or
                 not descr.impl_is_optiondescription()):
            try:
                msg = descr.impl_get_displayname()
            except AttributeError:
                msg = descr
            raise TypeError(_('"{0}" must be an optiondescription, not an {1}'
                              ).format(msg, type(descr)))
        self._impl_descr = descr
        self._impl_context = context
        self._impl_path = subpath
        if descr is not None and descr.impl_is_leadership():
            leader = descr.get_leader()
            leaderpath = leader.impl_getname()
            cconfig_bag = config_bag.copy()
            cconfig_bag.remove_validation()
            moption_bag = OptionBag()
            moption_bag.set_option(leader,
                                   None,
                                   cconfig_bag)
            moption_bag.properties = await self.cfgimpl_get_settings().getproperties(moption_bag)
            value = await self.getattr(leaderpath,
                                       moption_bag)
            self._impl_length = len(value)

    def cfgimpl_get_length(self):
        return self._impl_length

    async def cfgimpl_get_length_leadership(self,
                                      option_bag):
        if option_bag.option.impl_is_symlinkoption():
            context = self.cfgimpl_get_context()
            path = option_bag.option.impl_getopt().impl_getpath()
            subconfig, _ = await context.cfgimpl_get_home_by_path(path,
                                                                  option_bag.config_bag)
            return subconfig.cfgimpl_get_length()
        else:
            return self.cfgimpl_get_length()

    async def reset_one_option_cache(self,
                                     desc,
                                     resetted_opts,
                                     option_bag):

        if option_bag.path in resetted_opts:
            return
        resetted_opts.append(option_bag.path)
        for woption in option_bag.option._get_dependencies(self.cfgimpl_get_description()):
            option = woption()
            if option.impl_is_dynoptiondescription():
                subpath = option.impl_getpath().rsplit('.', 1)[0]
                for suffix in await option.get_suffixes(option_bag.config_bag):
                    doption = option.to_dynoption(subpath,
                                                  suffix,
                                                  option)
                    doption_bag = OptionBag()
                    doption_bag.set_option(doption,
                                           option_bag.index,
                                           option_bag.config_bag)
                    doption_bag.properties = await self.cfgimpl_get_settings().getproperties(doption_bag)
                    await self.reset_one_option_cache(desc,
                                                      resetted_opts,
                                                      doption_bag)
            elif option.issubdyn():
                # it's an option in dynoptiondescription, remove cache for all generated option
                dynopt = option.getsubdyn()
                rootpath = dynopt.impl_getpath()
                subpaths = [rootpath] + option.impl_getpath()[len(rootpath) + 1:].split('.')[:-1]
                for suffix in await dynopt.get_suffixes(option_bag.config_bag):
                    path_suffix = dynopt.convert_suffix_to_path(suffix)
                    subpath = '.'.join([subp + path_suffix for subp in subpaths])
                    doption = option.to_dynoption(subpath,
                                                  suffix,
                                                  dynopt)
                    doption_bag = OptionBag()
                    doption_bag.set_option(doption,
                                           option_bag.index,
                                           option_bag.config_bag)
                    doption_bag.properties = await self.cfgimpl_get_settings().getproperties(doption_bag)
                    await self.reset_one_option_cache(desc,
                                                      resetted_opts,
                                                      doption_bag)
            else:
                doption_bag = OptionBag()
                doption_bag.set_option(option,
                                       option_bag.index,
                                       option_bag.config_bag)
                doption_bag.properties = None
                await self.reset_one_option_cache(desc,
                                                  resetted_opts,
                                                  doption_bag)
            del option
        option_bag.option.reset_cache(option_bag.path,
                                      option_bag.config_bag,
                                      resetted_opts)

    async def cfgimpl_reset_cache(self,
                                  option_bag,
                                  resetted_opts=None):
        """reset all settings in cache
        """
        if resetted_opts is None:
            resetted_opts = []

        context = self.cfgimpl_get_context()
        desc = context.cfgimpl_get_description()
        if option_bag is not None:
            await self.reset_one_option_cache(desc,
                                              resetted_opts,
                                              option_bag)
        else:
            context._impl_values_cache.reset_all_cache()
            context._impl_properties_cache.reset_all_cache()

    async def cfgimpl_get_home_by_path(self,
                                       path: str,
                                       config_bag: ConfigBag,
                                       validate_properties=True) -> ('Subconfig', str):
        """:returns: tuple (config, name)"""
        path = path.split('.')
        for step in path[:-1]:
            option_bag = OptionBag()
            option = await self.cfgimpl_get_description().get_child(step,
                                                                    config_bag,
                                                                    self.cfgimpl_get_path())
            option_bag.set_option(option,
                                  None,
                                  config_bag)
            option_bag.properties = await self.cfgimpl_get_settings().getproperties(option_bag)
            self = await self.get_subconfig(option_bag,
                                            validate_properties)
        assert isinstance(self, SubConfig), _('unknown option {}').format(path[-1])
        return self, path[-1]

    # ______________________________________________________________________
    def cfgimpl_get_context(self):
        return self._impl_context()

    def cfgimpl_get_description(self):
        assert self._impl_descr is not None, _('there is no option description for this config'
                                               ' (may be GroupConfig)')
        return self._impl_descr

    def cfgimpl_get_settings(self):
        return self.cfgimpl_get_context()._impl_settings

    def cfgimpl_get_values(self):
        return self.cfgimpl_get_context()._impl_values

    async def setattr(self,
                      value,
                      option_bag):
        if option_bag.option.impl_is_symlinkoption():
            raise ConfigError(_("can't set value to a SymLinkOption"))
        context = option_bag.config_bag.context
        await context.cfgimpl_get_settings().validate_properties(option_bag)
        if option_bag.option.impl_is_leader() and len(value) < self._impl_length:
            raise LeadershipError(_('cannot reduce length of the leader "{}"'
                                    '').format(option_bag.option.impl_get_display_name()))
        return await context.cfgimpl_get_values().setvalue(value,
                                                           option_bag)

    async def delattr(self,
                      option_bag):
        option = option_bag.option
        if option.impl_is_symlinkoption():
            raise ConfigError(_("can't delete a SymLinkOption"))
        values = self.cfgimpl_get_values()
        if option_bag.index is not None:
            await values.reset_follower(option_bag)
        else:
            await values.reset(option_bag)

    def _get_subpath(self, name):
        if self._impl_path is None:
            subpath = name
        else:
            subpath = self._impl_path + '.' + name
        return subpath

    async def get_subconfig(self,
                            option_bag: OptionBag,
                            validate_properties: bool=True) -> 'SubConfig':
        if validate_properties:
            await self.cfgimpl_get_settings().validate_properties(option_bag)
        return await SubConfig(option_bag.option,
                               self._impl_context,
                               option_bag.config_bag,
                               option_bag.path)

    async def getattr(self,
                      name,
                      option_bag,
                      from_follower=False,
                      needs_re_verify_follower_properties=False,
                      need_help=True):
        """
        :return: option's value if name is an option name, OptionDescription
                 otherwise
        """
        config_bag = option_bag.config_bag
        if '.' in name:
            self, name = await self.cfgimpl_get_home_by_path(name,
                                                             config_bag)

        option = option_bag.option
        if option.impl_is_symlinkoption():
            soption_bag = OptionBag()
            soption_bag.set_option(option.impl_getopt(),
                                   option_bag.index,
                                   config_bag)
            soption_bag.properties = await self.cfgimpl_get_settings().getproperties(soption_bag)
            soption_bag.ori_option = option
            context = self.cfgimpl_get_context()
            return await context.getattr(soption_bag.path,
                                   soption_bag)

        #if not from_follower or needs_re_verify_follower_properties:
        if option.impl_is_follower() and not from_follower:
            needs_re_verify_follower_properties = await self.cfgimpl_get_settings().has_properties_index(option_bag)
        if not option.impl_is_follower() or \
                (needs_re_verify_follower_properties and option_bag.index is not None) or \
                (not needs_re_verify_follower_properties and (not from_follower or option_bag.index is None)):
            await self.cfgimpl_get_settings().validate_properties(option_bag,
                                                                  need_help=need_help)

        if option.impl_is_follower() and not from_follower:
            length = await self.cfgimpl_get_length_leadership(option_bag)
            follower_len = await self.cfgimpl_get_values()._p_.get_max_length(option_bag.config_bag.connection,
                                                                              option_bag.path)
            if follower_len > length:
                raise LeadershipError(_('the follower option "{}" has greater length ({}) than the leader '
                                        'length ({})').format(option.impl_get_display_name(),
                                                              follower_len,
                                                              length,
                                                              option_bag.index))

        if option.impl_is_follower() and option_bag.index is None:
            value = []
            for idx in range(length):
                soption_bag = OptionBag()
                soption_bag.set_option(option,
                                       idx,
                                       config_bag)
                try:
                    soption_bag.properties = await self.cfgimpl_get_settings().getproperties(soption_bag)
                    value.append(await self.getattr(name,
                                                    soption_bag,
                                                    from_follower=True,
                                                    needs_re_verify_follower_properties=needs_re_verify_follower_properties))
                except PropertiesOptionError as err:
                    value.append(err)
        else:
            value = await self.cfgimpl_get_values().get_cached_value(option_bag)
        self.cfgimpl_get_settings().validate_mandatory(value,
                                                       option_bag)
        return value

    async def find(self,
                   bytype,
                   byname,
                   byvalue,
                   config_bag,
                   _subpath=None,
                   raise_if_not_found=True,
                   only_path=undefined,
                   only_option=undefined,
                   with_option=False):
        """
        convenience method for finding an option that lives only in the subtree

        :param first: return only one option if True, a list otherwise
        :return: find list or an exception if nothing has been found
        """
        async def _filter_by_value(soption_bag):
            try:
                value = await context.getattr(path,
                                              soption_bag)
            except PropertiesOptionError:
                return False
            if isinstance(value, list):
                return byvalue in value
            else:
                return value == byvalue

        found = False
        if only_path is not undefined:
            async def _fake_iter():
                yield only_option
            options = _fake_iter()
        else:
            options = self.cfgimpl_get_description().get_children_recursively(bytype,
                                                                              byname,
                                                                              config_bag)
        context = self.cfgimpl_get_context()
        async for option in options:
            option_bag = OptionBag()
            path = option.impl_getpath()
            option_bag.set_option(option,
                                  None,
                                  config_bag)
            option_bag.properties = await self.cfgimpl_get_settings().getproperties(option_bag)
            if byvalue is not undefined and not await _filter_by_value(option_bag):
                continue
            elif config_bag.properties:
                #remove option with propertyerror, ...
                try:
                    if '.' in path:
                        subconfig, subpath = await context.cfgimpl_get_home_by_path(path,
                                                                                    config_bag)
                    else:
                        subconfig = self
                        subpath = path
                    await subconfig.cfgimpl_get_description().get_child(subpath,
                                                                        config_bag,
                                                                        subconfig.cfgimpl_get_path())
                    await self.cfgimpl_get_settings().validate_properties(option_bag)
                except PropertiesOptionError:
                    continue
            found = True
            if not with_option:
                yield path
            else:
                yield path, option
        self._find_return_results(found,
                                  raise_if_not_found)

    def _find_return_results(self,
                             found,
                             raise_if_not_found):
        if not found and raise_if_not_found:
            raise AttributeError(_("no option found in config"
                                   " with these criteria"))

    async def make_dict(self,
                        config_bag,
                        flatten=False,
                        fullpath=False,
                        leader_to_list=False):
        """exports the whole config into a `dict`
        :returns: dict of Option's name (or path) and values
        """
        pathsvalues = {}
        await self._make_dict(config_bag,
                              [],
                              flatten,
                              fullpath,
                              pathsvalues,
                              leader_to_list)
        return pathsvalues

    async def _make_dict(self,
                         config_bag,
                         _currpath,
                         flatten,
                         fullpath,
                         pathsvalues,
                         leader_to_list):
        for opt in await self.cfgimpl_get_description().get_children(config_bag):
            if leader_to_list and opt.impl_is_optiondescription() and opt.impl_is_leadership():
                # leader
                children = await opt.get_children(config_bag)
                leader = children[0]
                loption_bag = OptionBag()
                loption_bag.set_option(leader,
                                       None,
                                       config_bag)
                loption_bag.properties = await self.cfgimpl_get_settings().getproperties(loption_bag)
                leader_pathsvalues = {}
                leader_currpath = _currpath + [leader.impl_getname()]
                await self._make_sub_dict(leader_pathsvalues,
                                          leader_currpath,
                                          loption_bag,
                                          flatten,
                                          fullpath,
                                          leader_to_list)
                if not leader_pathsvalues:
                    continue
                leader_name = list(leader_pathsvalues.keys())[0]
                pathsvalues[leader_name] = []
                subconfig = await SubConfig(opt,
                                            self._impl_context,
                                            config_bag,
                                            opt.impl_getpath())
                for idx, value in enumerate(leader_pathsvalues[leader_name]):
                    leadership_pathsvalues = {leader_name: value}
                    for follower_opt in children[1:]:
                        foption_bag = OptionBag()
                        foption_bag.set_option(follower_opt,
                                               idx,
                                               config_bag)
                        try:
                            foption_bag.properties = await self.cfgimpl_get_settings().getproperties(foption_bag)
                            await subconfig._make_sub_dict(leadership_pathsvalues,
                                                           leader_currpath,
                                                           foption_bag,
                                                           flatten,
                                                           fullpath,
                                                           leader_to_list)
                        except PropertiesOptionError as err:
                            if err.proptype in (['mandatory'], ['empty']):
                                raise err
                            continue
                    pathsvalues[leader_name].append(leadership_pathsvalues)
            else:
                soption_bag = OptionBag()
                soption_bag.set_option(opt,
                                       None,
                                       config_bag)
                try:
                    soption_bag.properties = await self.cfgimpl_get_settings().getproperties(soption_bag)
                    await self._make_sub_dict(pathsvalues,
                                              _currpath,
                                              soption_bag,
                                              flatten,
                                              fullpath,
                                              leader_to_list)
                except PropertiesOptionError as err:
                    if err.proptype in (['mandatory'], ['empty']):
                        raise err
                    continue

    async def _make_sub_dict(self,
                             pathsvalues,
                             _currpath,
                             option_bag,
                             flatten,
                             fullpath,
                             leader_to_list):
        option = option_bag.option
        name = option.impl_getname()
        if option.impl_is_optiondescription():
            await self.cfgimpl_get_settings().validate_properties(option_bag,
                                                                  need_help=False)
            subconfig = await SubConfig(option_bag.option,
                                        self._impl_context,
                                        option_bag.config_bag,
                                        option_bag.path)
            await subconfig._make_dict(option_bag.config_bag,
                                       _currpath + [name],
                                       flatten,
                                       fullpath,
                                       pathsvalues,
                                       leader_to_list)
        else:
            ret = await self.getattr(name,
                                     option_bag,
                                     need_help=False)
            if flatten:
                name_ = option.impl_getname()
            elif fullpath:
                name_ = option.impl_getpath()
            else:
                name_ = '.'.join(_currpath + [name])
            pathsvalues[name_] = ret

    def cfgimpl_get_path(self,
                         dyn=True):
        descr = self.cfgimpl_get_description()
        if not dyn and descr.impl_is_dynoptiondescription():
            return descr.impl_getopt().impl_getpath()
        return self._impl_path


class _CommonConfig(SubConfig):
    "abstract base class for the Config, KernelGroupConfig and the KernelMetaConfig"
    __slots__ = ('_impl_values',
                 '_impl_values_cache',
                 '_impl_settings',
                 '_impl_properties_cache',
                 '_impl_permissives_cache',
                 'parents',
                 'impl_type')

    async def _impl_build_all_caches(self):
        descr = self.cfgimpl_get_description()
        if not descr.impl_already_build_caches():
            descr._group_type = groups.root
            await descr._build_cache(display_name=self._display_name)
        if not hasattr(descr, '_cache_force_store_values'):
            raise ConfigError(_('option description seems to be part of an other '
                                'config'))

    def get_parents(self):
        for parent in self.parents:
            yield parent()

    # information
    async def impl_set_information(self,
                                   connection,
                                   key,
                                   value):
        """updates the information's attribute

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        await self._impl_values.set_information(connection,
                                                key,
                                                value)

    async def impl_get_information(self,
                                   connection,
                                   key,
                                   default=undefined):
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        return await self._impl_values.get_information(connection,
                                                       key,
                                                       default)

    async def impl_del_information(self,
                                   connection,
                                   key,
                                   raises=True):
        await self._impl_values.del_information(connection,
                                                key,
                                                raises)

    async def impl_list_information(self,
                                    connection):
        return await self._impl_values.list_information(connection)

    def __getstate__(self):
        raise NotImplementedError()

    async def _gen_fake_values(self,
                               connection):
        fake_config = await KernelConfig(self._impl_descr,
                                         force_values=await get_default_values_storages(connection),
                                         force_settings=self.cfgimpl_get_settings(),
                                         display_name=self._display_name,
                                         connection=connection)
        export = await self.cfgimpl_get_values()._p_.exportation(connection)
        await fake_config.cfgimpl_get_values()._p_.importation(connection,
                                                               export)
        fake_config.parents = self.parents
        return fake_config

    async def duplicate(self,
                        connection,
                        session_id=None,
                        force_values=None,
                        force_settings=None,
                        storage=None,
                        metaconfig_prefix=None,
                        child=None,
                        deep=None):
        assert isinstance(self, (KernelConfig, KernelMixConfig)), _('cannot duplicate {}').format(self.__class__.__name__)
        if isinstance(self, KernelConfig):
            duplicated_config = await KernelConfig(self._impl_descr,
                                                   _duplicate=True,
                                                   session_id=session_id,
                                                   force_values=force_values,
                                                   force_settings=force_settings,
                                                   storage=storage,
                                                   connection=connection,
                                                   display_name=self._display_name)
        else:
            if session_id is None and metaconfig_prefix is not None:
                session_id = metaconfig_prefix + self.impl_getname()
            duplicated_config = await KernelMetaConfig([],
                                                       _duplicate=True,
                                                       optiondescription=self._impl_descr,
                                                       session_id=session_id,
                                                       storage=storage,
                                                       connection=connection,
                                                       display_name=self._display_name)
        duplicated_values = duplicated_config.cfgimpl_get_values()
        duplicated_settings = duplicated_config.cfgimpl_get_settings()
        await duplicated_values._p_.importation(connection,
                                                await self.cfgimpl_get_values()._p_.exportation(connection))
        properties = await self.cfgimpl_get_settings()._p_.exportation(connection)
        await duplicated_settings._p_.importation(connection,
                                                  properties)
        await duplicated_settings._pp_.importation(connection,
                                                   await self.cfgimpl_get_settings()._pp_.exportation(connection))
        duplicated_settings.ro_append = self.cfgimpl_get_settings().ro_append
        duplicated_settings.rw_append = self.cfgimpl_get_settings().rw_append
        duplicated_settings.ro_remove = self.cfgimpl_get_settings().ro_remove
        duplicated_settings.rw_remove = self.cfgimpl_get_settings().rw_remove
        duplicated_settings.default_properties = self.cfgimpl_get_settings().default_properties
        await duplicated_config.cfgimpl_reset_cache(None, None)
        if child is not None:
            duplicated_config._impl_children.append(child)
            child.parents.append(weakref.ref(duplicated_config))
        if self.parents:
            if deep is not None:
                for parent in self.parents:
                    wparent = parent()
                    if wparent not in deep:
                        deep.append(wparent)
                        duplicated_config = await wparent.duplicate(connection,
                                                                    deep=deep,
                                                                    storage=storage,
                                                                    metaconfig_prefix=metaconfig_prefix,
                                                                    child=duplicated_config)
            else:
                duplicated_config.parents = self.parents
                for parent in self.parents:
                    parent()._impl_children.append(duplicated_config)
        return duplicated_config

    def cfgimpl_get_config_path(self):
        path = self._impl_name
        for parent in self.parents:
            wparent = parent()
            if wparent is None:
                raise ConfigError(_('parent of {} not already exists').format(self._impl_name))
            path = parent().cfgimpl_get_config_path() + '.' + path
        return path


# ____________________________________________________________
@asyncinit
class KernelConfig(_CommonConfig):
    "main configuration management entry"
    __slots__ = ('__weakref__',
                 '_impl_name',
                 '_display_name',
                 '_impl_symlink',
                 '_storage')
    impl_type = 'config'

    async def __init__(self,
                       descr,
                       connection,
                       session_id=None,
                       delete_old_session=False,
                       force_values=None,
                       force_settings=None,
                       display_name=None,
                       _duplicate=False,
                       storage=None):
        """ Configuration option management class

        :param descr: describes the configuration schema
        :type descr: an instance of ``option.OptionDescription``
        :param context: the current root config
        :type context: `Config`
        :param session_id: name of the session
        :type session_id: `str`
        """
        self.parents = []
        self._impl_symlink = []
        self._display_name = display_name
        if isinstance(descr, Leadership):
            raise ConfigError(_('cannot set leadership object has root optiondescription'))
        if isinstance(descr, DynOptionDescription):
            raise ConfigError(_('cannot set dynoptiondescription object has root optiondescription'))
        if force_settings is not None and force_values is not None:
            if isinstance(force_settings, tuple):
                self._impl_settings = Settings(force_settings[0],
                                               force_settings[1])
            else:
                self._impl_settings = force_settings
            self._impl_permissives_cache = Cache()
            self._impl_properties_cache = Cache()
            self._impl_values = await Values(force_values,
                                             connection)
            self._impl_values_cache = Cache()
        else:
            storage, properties, permissives, values, session_id = await get_storages(self,
                                                                                      session_id,
                                                                                      delete_old_session,
                                                                                      storage,
                                                                                      connection)
            if not valid_name(session_id):
                raise ValueError(_("invalid session ID: {0} for config").format(session_id))
            self._impl_settings = Settings(properties,
                                           permissives)
            self._impl_permissives_cache = Cache()
            self._impl_properties_cache = Cache()
            self._impl_values = await Values(values,
                                             connection)
            self._impl_values_cache = Cache()
        self._storage = storage
        self._impl_context = weakref.ref(self)
        await super().__init__(descr,
                               self._impl_context,
                               None,
                               None)
        if None in [force_settings, force_values]:
            await self._impl_build_all_caches()
        self._impl_name = session_id

    def impl_getname(self):
        return self._impl_name

    def getconnection(self):
        return self.cfgimpl_get_settings()._p_.getconnection()


@asyncinit
class KernelGroupConfig(_CommonConfig):
    __slots__ = ('__weakref__',
                 '_impl_children',
                 '_impl_name')
    impl_type = 'group'

    async def __init__(self,
                       children,
                       session_id=None,
                       _descr=None):
        assert isinstance(children, list), _("groupconfig's children must be a list")
        names = []
        for child in children:
            assert isinstance(child,
                              _CommonConfig), _("groupconfig's children must be Config, MetaConfig or GroupConfig")
            name_ = child._impl_name
            names.append(name_)
        if len(names) != len(set(names)):
            for idx in range(1, len(names) + 1):
                name = names.pop(0)
                if name in names:
                    raise ConflictError(_('config name must be uniq in '
                                          'groupconfig for "{0}"').format(name))
        self._impl_children = children
        self.parents = []
        session_id = gen_storage_id(session_id, self)
        assert valid_name(session_id), _("invalid session ID: {0} for config").format(session_id)
        config_bag = ConfigBag(self,
                               properties=None,
                               permissives=None)
        await super().__init__(_descr,
                               weakref.ref(self),
                               config_bag,
                               None)
        self._impl_name = session_id

    def cfgimpl_get_children(self):
        return self._impl_children

    async def cfgimpl_reset_cache(self,
                                  option_bag,
                                  resetted_opts=None):
        if resetted_opts is None:
            resetted_opts = []
        if isinstance(self, KernelMixConfig):
            await super().cfgimpl_reset_cache(option_bag,
                                              resetted_opts=copy(resetted_opts))
        for child in self._impl_children:
            if option_bag is not None:
                coption_bag = option_bag.copy()
                cconfig_bag = coption_bag.config_bag.copy()
                cconfig_bag.context = child
                coption_bag.config_bag = cconfig_bag
            else:
                coption_bag = None
            await child.cfgimpl_reset_cache(coption_bag,
                                            resetted_opts=copy(resetted_opts))

    async def set_value(self,
                        path,
                        index,
                        value,
                        config_bag,
                        only_config=False):
        """Setattr not in current KernelGroupConfig, but in each children
        """
        ret = []
        for child in self._impl_children:
            cconfig_bag = config_bag.copy()
            cconfig_bag.context = child
            if isinstance(child, KernelGroupConfig):
                ret.extend(await child.set_value(path,
                                                 index,
                                                 value,
                                                 cconfig_bag,
                                                 only_config=only_config))
            else:
                settings = child.cfgimpl_get_settings()
                properties = await settings.get_context_properties(config_bag.connection,
                                                                   child._impl_properties_cache)
                permissives = await settings.get_context_permissives(config_bag.connection)
                cconfig_bag.properties = properties
                cconfig_bag.permissives = permissives
                try:
                    subconfig, name = await child.cfgimpl_get_home_by_path(path,
                                                                           cconfig_bag)
                    option = await subconfig.cfgimpl_get_description().get_child(name,
                                                                                 cconfig_bag,
                                                                                 child.cfgimpl_get_path())
                    option_bag = OptionBag()
                    option_bag.set_option(option,
                                          index,
                                          cconfig_bag)
                    option_bag.properties = await settings.getproperties(option_bag)
                    await child.setattr(value,
                                        option_bag)
                except PropertiesOptionError as err:
                    ret.append(PropertiesOptionError(err._option_bag,
                                                     err.proptype,
                                                     err._settings,
                                                     err._opt_type,
                                                     err._name,
                                                     err._orig_opt))
                except (ValueError, LeadershipError, AttributeError) as err:
                    ret.append(err)
        return ret


    async def find_group(self,
                         config_bag,
                         byname=None,
                         bypath=undefined,
                         byoption=undefined,
                         byvalue=undefined,
                         raise_if_not_found=True,
                         _sub=False):
        """Find first not in current KernelGroupConfig, but in each children
        """
        # if KernelMetaConfig, all children have same OptionDescription in
        # context so search only one time the option for all children
        if bypath is undefined and byname is not None and \
                isinstance(self,
                           KernelMixConfig):
            async for bypath, byoption in self.find(bytype=None,
                                                    byvalue=undefined,
                                                    byname=byname,
                                                    config_bag=config_bag,
                                                    raise_if_not_found=raise_if_not_found,
                                                    with_option=True):
                break
            byname = None

        ret = []
        for child in self._impl_children:
            if isinstance(child, KernelGroupConfig):
                ret.extend(await child.find_group(byname=byname,
                                                  bypath=bypath,
                                                  byoption=byoption,
                                                  byvalue=byvalue,
                                                  config_bag=config_bag,
                                                  raise_if_not_found=False,
                                                  _sub=True))
            else:
                cconfig_bag = config_bag.copy()
                cconfig_bag.context = child
                settings = child.cfgimpl_get_settings()
                properties = await settings.get_context_properties(config_bag.connection,
                                                                   child._impl_properties_cache)
                permissives = await settings.get_context_permissives(config_bag.connection)
                cconfig_bag.properties = properties
                cconfig_bag.permissives = permissives
                async for path in child.find(None,
                                             byname,
                                             byvalue,
                                             config_bag=cconfig_bag,
                                             raise_if_not_found=False,
                                             only_path=bypath,
                                             only_option=byoption):
                    ret.append(child)
                    break
        if not _sub:
            self._find_return_results(ret != [],
                                      raise_if_not_found)
        return ret

    def impl_getname(self):
        return self._impl_name

    async def reset(self,
                    connection,
                    path):
        for child in self._impl_children:
            settings = child.cfgimpl_get_settings()
            properties = await settings.get_context_properties(connection,
                                                               child._impl_properties_cache)
            permissives = await settings.get_context_permissives(connection)
            config_bag = ConfigBag(child,
                                   properties=properties,
                                   permissives=permissives)
            config_bag.connection = connection
            config_bag.remove_validation()
            subconfig, name = await child.cfgimpl_get_home_by_path(path,
                                                                   config_bag)
            option = await subconfig.cfgimpl_get_description().get_child(name,
                                                                         config_bag,
                                                                         subconfig.cfgimpl_get_path())
            option_bag = OptionBag()
            option_bag.set_option(option,
                                  None,
                                  config_bag)
            option_bag.properties = await child.cfgimpl_get_settings().getproperties(option_bag)
            option_bag.config_bag.context = child
            await child.cfgimpl_get_values().reset(option_bag)

    def getconfig(self,
                  name):
        for child in self._impl_children:
            if name == child.impl_getname():
                return child
        raise ConfigError(_('unknown config "{}"').format(name))

    def getconnection(self):
        if self.impl_type == 'group':
            # Get the first storage, assume that all children have same storage
            return self._impl_children[0].getconnection()
        return self.cfgimpl_get_settings()._p_.getconnection()


@asyncinit
class KernelMixConfig(KernelGroupConfig):
    __slots__ = ('_display_name',
                 '_impl_symlink',
                 '_storage')
    impl_type = 'mix'

    async def __init__(self,
                       optiondescription,
                       children,
                       connection,
                       session_id=None,
                       delete_old_session=False,
                       storage=None,
                       display_name=None,
                       _duplicate=False):
        # FIXME _duplicate
        self._display_name = display_name
        self._impl_symlink = []
        for child in children:
            if not isinstance(child, (KernelConfig, KernelMixConfig)):
                raise TypeError(_("child must be a Config, MixConfig or MetaConfig"))
            child.parents.append(weakref.ref(self))
        storage, properties, permissives, values, session_id = await get_storages(self,
                                                                                  session_id,
                                                                                  delete_old_session,
                                                                                  storage,
                                                                                  connection)
        self._impl_settings = Settings(properties,
                                       permissives)
        self._impl_permissives_cache = Cache()
        self._impl_properties_cache = Cache()
        self._impl_values = await Values(values,
                                         connection)
        self._impl_values_cache = Cache()
        self._storage = storage
        await super().__init__(children,
                               session_id=session_id,
                               _descr=optiondescription)
        await self._impl_build_all_caches()

    async def set_value(self,
                        path,
                        index,
                        value,
                        config_bag,
                        force_default=False,
                        force_dont_change_value=False,
                        force_default_if_same=False,
                        only_config=False):
        """only_config: could be set if you want modify value in all Config included in
                        this KernelMetaConfig
        """
        if only_config:
            if force_default or force_default_if_same or force_dont_change_value:
                raise ValueError(_('force_default, force_default_if_same or '
                                   'force_dont_change_value cannot be set with'
                                   ' only_config'))
            return await super().set_value(path,
                                           index,
                                           value,
                                           config_bag,
                                           only_config=only_config)
        ret = []
        subconfig, name = await self.cfgimpl_get_home_by_path(path,
                                                              config_bag)
        option = await subconfig.cfgimpl_get_description().get_child(name,
                                                                     config_bag,
                                                                     self.cfgimpl_get_path())
        option_bag = OptionBag()
        option_bag.set_option(option,
                              index,
                              config_bag)
        option_bag.properties = await self.cfgimpl_get_settings().getproperties(option_bag)
        if force_default or force_default_if_same or force_dont_change_value:
            if force_default and force_dont_change_value:
                raise ValueError(_('force_default and force_dont_change_value'
                                   ' cannot be set together'))
            for child in self._impl_children:
                cconfig_bag = config_bag.copy()
                cconfig_bag.context = child
                settings = child.cfgimpl_get_settings()
                properties = await settings.get_context_properties(config_bag.connection,
                                                                   child._impl_properties_cache)
                permissives = await settings.get_context_permissives(config_bag.connection)
                cconfig_bag.properties = properties
                cconfig_bag.permissives = permissives
                try:
                    subconfig2, name = await child.cfgimpl_get_home_by_path(path,
                                                                            cconfig_bag)
                    if self.impl_type == 'meta':
                        moption_bag = option_bag.copy()
                        del moption_bag.properties
                        del moption_bag.permissives

                        moption_bag.config_bag = cconfig_bag
                        moption_bag.properties = await settings.getproperties(moption_bag)
                    else:
                        option = await subconfig2.cfgimpl_get_description().get_child(name,
                                                                                      cconfig_bag,
                                                                                      child.cfgimpl_get_path())
                        moption_bag = OptionBag()
                        moption_bag.set_option(option,
                                               index,
                                               cconfig_bag)
                        moption_bag.properties = await settings.getproperties(moption_bag)
                    if force_default_if_same:
                        if not await child.cfgimpl_get_values()._p_.hasvalue(config_bag.connection,
                                                                             path):
                            child_value = undefined
                        else:
                            child_value = await subconfig2.getattr(name,
                                                                   moption_bag)
                    if force_default or (force_default_if_same and value == child_value):
                        await child.cfgimpl_get_values().reset(moption_bag)
                        continue
                    if force_dont_change_value:
                        child_value = await child.getattr(name,
                                                          moption_bag)
                        if value != child_value:
                            await subconfig2.setattr(child_value,
                                                     moption_bag)
                except PropertiesOptionError as err:
                    ret.append(PropertiesOptionError(err._option_bag,
                                                     err.proptype,
                                                     err._settings,
                                                     err._opt_type,
                                                     err._name,
                                                     err._orig_opt))
                except (ValueError, LeadershipError, AttributeError) as err:
                    ret.append(err)

        try:
            if self.impl_type == 'meta':
                moption_bag = option_bag.copy()
                #del option_bag.properties
                #del option_bag.permissives
                moption_bag.config_bag = config_bag
                moption_bag.properties = await config_bag.context.cfgimpl_get_settings().getproperties(moption_bag)
            else:
                moption_bag = option_bag
            await subconfig.setattr(value,
                                    moption_bag)
        except (PropertiesOptionError, ValueError, LeadershipError) as err:
            ret.append(err)
        return ret

    async def reset(self,
                    path,
                    only_children,
                    config_bag):
        rconfig_bag = config_bag.copy()
        rconfig_bag.remove_validation()
        if self.impl_type == 'meta':
            subconfig, name = await self.cfgimpl_get_home_by_path(path,
                                                                  config_bag)
            option = await subconfig.cfgimpl_get_description().get_child(name,
                                                                         config_bag,
                                                                         subconfig.cfgimpl_get_path())
            option_bag = OptionBag()
            option_bag.set_option(option,
                                  None,
                                  rconfig_bag)
            option_bag.properties = await self.cfgimpl_get_settings().getproperties(option_bag)
        elif not only_children:
            try:
                subconfig, name = await self.cfgimpl_get_home_by_path(path,
                                                                      config_bag)
                option = await subconfig.cfgimpl_get_description().get_child(name,
                                                                             config_bag,
                                                                             subconfig.cfgimpl_get_path())
                option_bag = OptionBag()
                option_bag.set_option(option,
                                      None,
                                      rconfig_bag)
                option_bag.properties = await self.cfgimpl_get_settings().getproperties(option_bag)
            except AttributeError:
                only_children = True
        for child in self._impl_children:
            rconfig_bag.context = child
            try:
                if self.impl_type == 'meta':
                    moption_bag = option_bag
                    moption_bag.config_bag = rconfig_bag
                else:
                    subconfig, name = await child.cfgimpl_get_home_by_path(path,
                                                                           rconfig_bag)
                    option = await subconfig.cfgimpl_get_description().get_child(name,
                                                                                 rconfig_bag,
                                                                                 child.cfgimpl_get_path())
                    moption_bag = OptionBag()
                    moption_bag.set_option(option,
                                           None,
                                           rconfig_bag)
                    moption_bag.properties = await self.cfgimpl_get_settings().getproperties(moption_bag)
                await child.cfgimpl_get_values().reset(moption_bag)
            except AttributeError:
                pass
            if isinstance(child, KernelMixConfig):
                await child.reset(path,
                                  False,
                                  rconfig_bag)
        if not only_children:
            option_bag.config_bag = config_bag
            await self.cfgimpl_get_values().reset(option_bag)

    async def new_config(self,
                         connection,
                         session_id,
                         type_='config',
                         storage=None,
                         new=None,
                         ):
        if new is None:
            new = session_id not in await list_sessions()
        if new and session_id in [child.impl_getname() for child in self._impl_children]:
            raise ConflictError(_('config name must be uniq in '
                                  'groupconfig for {0}').format(session_id))
        assert type_ in ('config', 'metaconfig', 'mixconfig'), _('unknown type {}').format(type_)
        if type_ == 'config':
            config = await KernelConfig(self._impl_descr,
                                        session_id=session_id,
                                        storage=storage,
                                        connection=connection,
                                        display_name=self._display_name)
        elif type_ == 'metaconfig':
            config = await KernelMetaConfig([],
                                            optiondescription=self._impl_descr,
                                            session_id=session_id,
                                            storage=storage,
                                            connection=connection,
                                            display_name=self._display_name)
        elif type_ == 'mixconfig':
            config = await KernelMixConfig(children=[],
                                           optiondescription=self._impl_descr,
                                           session_id=session_id,
                                           storage=storage,
                                           connection=connection,
                                           display_name=self._display_name)
        # Copy context properties/permissives
        if new:
            settings = config.cfgimpl_get_settings()
            properties = await self.cfgimpl_get_settings().get_context_properties(connection,
                                                                                  config._impl_properties_cache)
            await settings.set_context_properties(connection,
                                                  properties,
                                                  config)
            await settings.set_context_permissives(connection,
                                                   await self.cfgimpl_get_settings().get_context_permissives(connection))
            settings.ro_append = self.cfgimpl_get_settings().ro_append
            settings.rw_append = self.cfgimpl_get_settings().rw_append
            settings.ro_remove = self.cfgimpl_get_settings().ro_remove
            settings.rw_remove = self.cfgimpl_get_settings().rw_remove
            settings.default_properties = self.cfgimpl_get_settings().default_properties

        config.parents.append(weakref.ref(self))
        self._impl_children.append(config)
        return config

    async def add_config(self,
                         apiconfig):
        config = apiconfig._config_bag.context
        if config.impl_getname() in [child.impl_getname() for child in self._impl_children]:
            raise ConflictError(_('config name must be uniq in '
                                  'groupconfig for {0}').format(config.impl_getname()))

        config.parents.append(weakref.ref(self))
        self._impl_children.append(config)
        await config.cfgimpl_reset_cache(None, None)

    async def pop_config(self,
                         session_id,
                         config):
        if session_id is not None:
            for idx, child in enumerate(self._impl_children):
                if session_id == child.impl_getname():
                    await child.cfgimpl_reset_cache(None, None)
                    self._impl_children.pop(idx)
                    break
            else:
                raise ConfigError(_('cannot find the config {}').format(session_id))
        if config is not None:
            self._impl_children.remove(config)
            child = config
        for index, parent in enumerate(child.parents):
            if parent() == self:
                child.parents.pop(index)
                break
        else:
            raise ConfigError(_('cannot find the config {}').format(self.session_id))
        return child


@asyncinit
class KernelMetaConfig(KernelMixConfig):
    __slots__ = tuple()
    impl_type = 'meta'

    async def __init__(self,
                       children,
                       connection,
                       session_id=None,
                       delete_old_session=False,
                       optiondescription=None,
                       storage=None,
                       display_name=None,
                       _duplicate=False):
        descr = None
        self._display_name = display_name
        if optiondescription is not None:
            if not _duplicate:
                new_children = []
                for child_session_id in children:
                    assert isinstance(child_session_id, str), _('MetaConfig with optiondescription'
                                                                ' must have string has child, '
                                                                'not {}').format(child_session_id)
                    new_children.append(await KernelConfig(optiondescription,
                                                           connection,
                                                           delete_old_session=delete_old_session,
                                                           session_id=child_session_id,
                                                           display_name=self._display_name))
                children = new_children
            descr = optiondescription
        for child in children:
            if __debug__ and not isinstance(child, (KernelConfig,
                                                    KernelMetaConfig)):
                raise TypeError(_("child must be a Config or MetaConfig"))
            if descr is None:
                descr = child.cfgimpl_get_description()
            elif descr is not child.cfgimpl_get_description():
                raise ValueError(_('all config in metaconfig must '
                                   'have the same optiondescription'))
        await super().__init__(descr,
                               children,
                               connection,
                               delete_old_session=delete_old_session,
                               storage=storage,
                               session_id=session_id)

    async def add_config(self,
                         apiconfig):
        if self._impl_descr is not apiconfig._config_bag.context.cfgimpl_get_description():
            raise ValueError(_('metaconfig must '
                               'have the same optiondescription'))
        await super().add_config(apiconfig)
