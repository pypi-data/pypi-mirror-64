# -*- coding: utf-8 -*-
# Copyright (C) 2014-2020 Team tiramisu (see AUTHORS for all contributors)
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
from copy import copy
from typing import Optional, Iterator, Union, List


from ..i18n import _
from ..setting import ConfigBag, OptionBag, groups, undefined, owners, Undefined
from .baseoption import BaseOption
from .syndynoptiondescription import SynDynOptionDescription, SynDynLeadership
from ..error import ConfigError, ConflictError


class CacheOptionDescription(BaseOption):
    __slots__ = ('_cache_force_store_values',)

    def impl_already_build_caches(self) -> bool:
        return self.impl_is_readonly()

    async def _build_cache(self,
                           path='',
                           _consistencies=None,
                           _consistencies_id=0,
                           currpath: List[str]=None,
                           cache_option=None,
                           force_store_values=None,
                           display_name=None) -> None:
        """validate options and set option has readonly option
        """
        # _consistencies is None only when we start to build cache
        if _consistencies is None:
            init = True
            _consistencies = {}
            if __debug__:
                cache_option = []
            force_store_values = []
            currpath = []
        else:
            init = False

        if self.impl_is_readonly():
            # cache already set
            raise ConfigError(_('option description seems to be part of an other '
                                'config'))
        for option in await self.get_children(config_bag=undefined,
                                              dyn=False):
            if __debug__:
                cache_option.append(option)
            sub_currpath = currpath + [option.impl_getname()]
            subpath = '.'.join(sub_currpath)
            if isinstance(option, OptionDescription):
                await option._build_cache(subpath,
                                          _consistencies,
                                          _consistencies_id,
                                          sub_currpath,
                                          cache_option,
                                          force_store_values,
                                          display_name)
            else:
                is_multi = option.impl_is_multi()
                if not option.impl_is_symlinkoption():
                    properties = option.impl_getproperties()
                    if 'force_store_value' in properties:
                        if __debug__:
                            if option.issubdyn():
                                raise ConfigError(_('the dynoption "{0}" cannot have '
                                                    '"force_store_value" property').format(
                                                        option.impl_get_display_name()))
                        force_store_values.append((subpath, option))
                    if __debug__ and ('force_default_on_freeze' in properties or \
                            'force_metaconfig_on_freeze' in properties) and \
                            'frozen' not in properties and \
                            option.impl_is_leader():
                        raise ConfigError(_('a leader ({0}) cannot have '
                                            '"force_default_on_freeze" or '
                                            '"force_metaconfig_on_freeze" '
                                            'property without "frozen"'
                                            '').format(option.impl_get_display_name()))
            if option.impl_is_readonly():
                raise ConflictError(_('duplicate option: {0}').format(option))
            if not self.impl_is_readonly() and display_name:
                option._display_name_function = display_name
            option._path = subpath
            option._set_readonly()
        if init:
            self._cache_force_store_values = force_store_values
            self._path = self._name
            self._set_readonly()

    async def impl_build_force_store_values(self,
                                            config_bag: ConfigBag) -> None:
        if 'force_store_value' not in config_bag.properties:
            return
        values = config_bag.context.cfgimpl_get_values()
        for subpath, option in self._cache_force_store_values:
            if not await values._p_.hasvalue(config_bag.connection,
                                             subpath):
                if option.impl_is_follower():
                    option_bag = OptionBag()
                    leader = option.impl_get_leadership().get_leader()
                    option_bag.set_option(leader,
                                          None,
                                          config_bag)
                    option_bag.properties = frozenset()
                    follower_len = len(await values.getvalue(option_bag))
                    for index in range(follower_len):
                        option_bag = OptionBag()
                        option_bag.set_option(option,
                                              index,
                                              config_bag)
                        option_bag.properties = frozenset()
                        await values._p_.setvalue(config_bag.connection,
                                                  subpath,
                                                  await values.getvalue(option_bag),
                                                  owners.forced,
                                                  index,
                                                  False)
                else:
                    option_bag = OptionBag()
                    option_bag.set_option(option,
                                          None,
                                          config_bag)
                    option_bag.properties = frozenset()
                    await values._p_.setvalue(config_bag.connection,
                                              subpath,
                                              await values.getvalue(option_bag),
                                              owners.forced,
                                              None,
                                              False)


class OptionDescriptionWalk(CacheOptionDescription):
    __slots__ = ('_children',)

    async def get_child(self,
                        name: str,
                        config_bag: ConfigBag,
                        subpath: str) -> Union[BaseOption, SynDynOptionDescription]:
        # if not dyn
        if name in self._children[0]:
            return self._children[1][self._children[0].index(name)]
        # if dyn
        for child in self._children[1]:
            if child.impl_is_dynoptiondescription():
                cname = child.impl_getname()
                if name.startswith(cname):
                    for suffix in await child.get_suffixes(config_bag):
                        if name == cname + child.convert_suffix_to_path(suffix):
                            return child.to_dynoption(subpath,
                                                      suffix,
                                                      child)
        if self.impl_get_group_type() == groups.root:
            raise AttributeError(_('unknown option "{0}" '
                                   'in root optiondescription'
                                   '').format(name))
        else:
            raise AttributeError(_('unknown option "{0}" '
                                   'in optiondescription "{1}"'
                                   '').format(name, self.impl_get_display_name()))

    async def get_children(self,
                           config_bag: Union[ConfigBag, Undefined],
                           dyn: bool=True) -> Union[BaseOption, SynDynOptionDescription]:
        if not dyn or config_bag is undefined or \
                config_bag.context.cfgimpl_get_description() == self:
            subpath = ''
        else:
            subpath = self.impl_getpath()
        children = []
        for child in self._children[1]:
            if dyn and child.impl_is_dynoptiondescription():
                for suffix in await child.get_suffixes(config_bag):
                    children.append(child.to_dynoption(subpath,
                                                       suffix,
                                                       child))
            else:
                children.append(child)
        return children

    async def get_children_recursively(self,
                                       bytype: Optional[BaseOption],
                                       byname: Optional[str],
                                       config_bag: ConfigBag,
                                       self_opt: BaseOption=None) -> Iterator[Union[BaseOption, SynDynOptionDescription]]:
        if self_opt is None:
            self_opt = self
        for option in await self_opt.get_children(config_bag):
            if option.impl_is_optiondescription():
                async for subopt in option.get_children_recursively(bytype,
                                                                    byname,
                                                                    config_bag):
                    yield subopt
            elif (byname is None or option.impl_getname() == byname) and \
                    (bytype is None or isinstance(option, bytype)):
                yield option


class OptionDescription(OptionDescriptionWalk):
    """Config's schema (organisation, group) and container of Options
    The `OptionsDescription` objects lives in the `tiramisu.config.Config`.
    """
    __slots__ = ('_group_type',)

    def __init__(self,
                 name: str,
                 doc: str,
                 children: List[BaseOption],
                 properties=None) -> None:
        """
        :param children: a list of options (including optiondescriptions)

        """
        assert isinstance(children, list), _('children in optiondescription "{}" '
                                             'must be a list').format(name)
        super().__init__(name,
                         doc=doc,
                         properties=properties)
        child_names = []
        if __debug__:
            dynopt_names = []
        for child in children:
            name = child.impl_getname()
            child_names.append(name)
            if __debug__ and child.impl_is_dynoptiondescription():
                dynopt_names.append(name)

        # before sorting
        children_ = (tuple(child_names), tuple(children))

        if __debug__:
            # better performance like this
            child_names.sort()
            old = None
            for child in child_names:
                if child == old:
                    raise ConflictError(_('duplicate option name: '
                                          '"{0}"').format(child))
                if dynopt_names:
                    for dynopt in dynopt_names:
                        if child != dynopt and child.startswith(dynopt):
                            raise ConflictError(_('the option\'s name "{}" start as '
                                                  'the dynoptiondescription\'s name "{}"').format(child, dynopt))
                old = child
        self._children = children_
        # the group_type is useful for filtering OptionDescriptions in a config
        self._group_type = groups.default

    def impl_is_optiondescription(self) -> bool:
        return True

    def impl_is_dynoptiondescription(self) -> bool:
        return False

    def impl_is_leadership(self) -> bool:
        return False

    # ____________________________________________________________
    def impl_set_group_type(self,
                            group_type: groups.GroupType) -> None:
        """sets a given group object to an OptionDescription

        :param group_type: an instance of `GroupType` or `LeadershipGroupType`
                              that lives in `setting.groups`
        """
        if __debug__:
            if self._group_type != groups.default:
                raise ValueError(_('cannot change group_type if already set '
                                   '(old {0}, new {1})').format(self._group_type,
                                                               group_type))
            if not isinstance(group_type, groups.GroupType):
                raise ValueError(_('group_type: {0}'
                                   ' not allowed').format(group_type))
            if isinstance(group_type, groups.LeadershipGroupType):
                raise ConfigError('please use Leadership object instead of OptionDescription')
        self._group_type = group_type

    def impl_get_group_type(self) -> groups.GroupType:
        return self._group_type

    def to_dynoption(self,
                     rootpath: str,
                     suffix: str,
                     ori_dyn) -> SynDynOptionDescription:
        return SynDynOptionDescription(self,
                                       rootpath,
                                       suffix,
                                       ori_dyn)
