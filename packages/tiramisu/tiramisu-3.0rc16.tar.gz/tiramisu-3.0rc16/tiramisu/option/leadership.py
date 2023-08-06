# -*- coding: utf-8 -*-
"Leadership support"
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
import weakref
from itertools import chain
from typing import List, Iterator, Optional, Any


from ..i18n import _
from ..setting import groups, undefined, OptionBag, Settings, ALLOWED_LEADER_PROPERTIES
from ..value import Values
from .optiondescription import OptionDescription
from .syndynoptiondescription import SynDynLeadership
from .baseoption import BaseOption
from .option import Option
from ..error import LeadershipError
from ..autolib import Calculation, ParamOption


class Leadership(OptionDescription):
    __slots__ = ('leader',
                 'followers')

    def __init__(self,
                 name: str,
                 doc: str,
                 children: List[BaseOption],
                 properties=None) -> None:
        super().__init__(name,
                         doc,
                         children,
                         properties=properties)
        self._group_type = groups.leadership
        followers = []
        if len(children) < 2:
            raise ValueError(_('a leader and a follower are mandatories in leadership "{}"'
                               '').format(name))
        leader = children[0]
        for idx, child in enumerate(children):
            if __debug__:
                if child.impl_is_symlinkoption():
                    raise ValueError(_('leadership "{0}" shall not have '
                                       "a symlinkoption").format(self.impl_get_display_name()))
                if not isinstance(child, Option):
                    raise ValueError(_('leadership "{0}" shall not have '
                                       'a subgroup').format(self.impl_get_display_name()))
                if not child.impl_is_multi():
                    raise ValueError(_('only multi option allowed in leadership "{0}" but option '
                                       '"{1}" is not a multi'
                                       '').format(self.impl_get_display_name(),
                                                  child.impl_get_display_name()))
                if idx != 0:
                    default = child.impl_getdefault()
                    if default != [] and not isinstance(default, Calculation):
                        raise ValueError(_('not allowed default value for follower option "{0}" '
                                           'in leadership "{1}"'
                                           '').format(child.impl_get_display_name(),
                                                      self.impl_get_display_name()))
            if idx != 0:
                # remove empty property for follower
                child._properties = frozenset(child._properties - {'empty', 'unique'})
                followers.append(child)
            child._add_dependency(self)
            child._leadership = weakref.ref(self)
        if __debug__:
            callback, callback_params = leader.impl_get_callback()
            options = []
            if callback is not None and callback_params is not None:
                for callbk in chain(callback_params.args, callback_params.kwargs.values()):
                    if isinstance(callbk, ParamOption) and callbk.option in followers:
                        raise ValueError(_("callback of leader's option shall "
                                           "not refered to a follower's ones"))

            for prop in leader.impl_getproperties():
                if prop not in ALLOWED_LEADER_PROPERTIES and not isinstance(prop, Calculation):
                    raise LeadershipError(_('leader cannot have "{}" property').format(prop))

    def is_leader(self,
                  opt: Option) -> bool:
        leader = self.get_leader()
        return opt == leader or (opt.impl_is_dynsymlinkoption() and opt.opt == leader)

    def get_leader(self) -> Option:
        return self._children[1][0]

    def get_followers(self) -> Iterator[Option]:
        for follower in self._children[1][1:]:
            yield follower

    def in_same_group(self,
                      opt: Option) -> bool:
        if opt.impl_is_dynsymlinkoption():
            opt = opt.opt
        return opt in self._children[1]

    async def reset(self,
                    values: Values,
                    option_bag: OptionBag) -> None:
        config_bag = option_bag.config_bag.copy()
        config_bag.remove_validation()
        for follower in self.get_followers():
            soption_bag = OptionBag()
            soption_bag.set_option(follower,
                                   None,
                                   config_bag)
            soption_bag.properties = await config_bag.context.cfgimpl_get_settings().getproperties(soption_bag)
            await values.reset(soption_bag)

    async def follower_force_store_value(self,
                                         values,
                                         value,
                                         option_bag,
                                         owner,
                                         dyn=None) -> None:
        settings = option_bag.config_bag.context.cfgimpl_get_settings()
        if value:
            rgevalue = range(len(value))
            if dyn is None:
                dyn = self
            for follower in await dyn.get_children(option_bag.config_bag):
                foption_bag = OptionBag()
                foption_bag.set_option(follower,
                                       None,
                                       option_bag.config_bag)
                if 'force_store_value' in await settings.getproperties(foption_bag):
                    for index in rgevalue:
                        foption_bag = OptionBag()
                        foption_bag.set_option(follower,
                                               index,
                                               option_bag.config_bag)
                        foption_bag.properties = await settings.getproperties(foption_bag)
                        await values._setvalue(foption_bag,
                                               await values.getvalue(foption_bag),
                                               owner)

    async def pop(self,
                  values: Values,
                  index: int,
                  option_bag: OptionBag,
                  followers: Optional[List[Option]]=undefined) -> None:
        if followers is undefined:
            # followers are not undefined only in SynDynLeadership
            followers = self.get_followers()
        config_bag = option_bag.config_bag.copy()
        config_bag.remove_validation()
        for follower in followers:
            follower_path = follower.impl_getpath()
            followerlen = await values._p_.get_max_length(config_bag.connection,
                                                          follower_path)
            soption_bag = OptionBag()
            soption_bag.set_option(follower,
                                   index,
                                   config_bag)
            # do not check force_default_on_freeze or force_metaconfig_on_freeze
            soption_bag.properties = set()
            is_default = await values.is_default_owner(soption_bag,
                                                       validate_meta=False)
            if not is_default and followerlen > index:
                await values._p_.resetvalue_index(config_bag.connection,
                                                  follower_path,
                                                  index)
            if followerlen > index + 1:
                for idx in range(index + 1, followerlen):
                    if await values._p_.hasvalue(config_bag.connection,
                                                 follower_path,
                                                 idx):
                        await values._p_.reduce_index(config_bag.connection,
                                                      follower_path,
                                                      idx)

    def reset_cache(self,
                    path: str,
                    config_bag: 'ConfigBag',
                    resetted_opts: List[Option]) -> None:
        self._reset_cache(path,
                          self.get_leader(),
                          self.get_followers(),
                          config_bag,
                          resetted_opts)

    def _reset_cache(self,
                     path: str,
                     leader: Option,
                     followers: List[Option],
                     config_bag: 'ConfigBag',
                     resetted_opts: List[Option]) -> None:
        super().reset_cache(path,
                            config_bag,
                            resetted_opts)
        leader.reset_cache(leader.impl_getpath(),
                           config_bag,
                           None)
        for follower in followers:
            spath = follower.impl_getpath()
            follower.reset_cache(spath,
                                 config_bag,
                                 None)
            # do not reset dependencies option
            # resetted_opts.append(spath)

    def impl_is_leadership(self) -> None:
        return True

    def to_dynoption(self,
                     rootpath: str,
                     suffix: str,
                     ori_dyn) -> SynDynLeadership:
        return SynDynLeadership(self,
                                rootpath,
                                suffix,
                                ori_dyn)
