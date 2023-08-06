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
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
from typing import Optional, Iterator, Any, List


from ..i18n import _
from ..setting import ConfigBag, groups, undefined, Settings
from ..value import Values
from .baseoption import BaseOption
from .syndynoption import SynDynOption


class SynDynOptionDescription:
    __slots__ = ('_opt',
                 '_subpath',
                 '_suffix',
                 'ori_dyn')

    def __init__(self,
                 opt: BaseOption,
                 subpath: str,
                 suffix: str,
                 ori_dyn) -> None:
        self._opt = opt
        if subpath is None:
            subpath = ''
        assert isinstance(subpath, str), 'subpath must be a string, not {}'.format(type(subpath))
        self._subpath = subpath
        self._suffix = suffix
        # For a Leadership inside a DynOptionDescription
        self.ori_dyn = ori_dyn

    def __getattr__(self,
                    name: str) -> Any:
        # if not in SynDynOptionDescription, get value in self._opt
        return getattr(self._opt,
                       name)

    def impl_getopt(self) -> BaseOption:
        return self._opt

    async def get_child(self,
                        name: str,
                        config_bag: ConfigBag,
                        subpath: str) -> BaseOption:
        if name.endswith(self._suffix):
            oname = name[:-len(self._suffix)]
            try:
                child = self._children[1][self._children[0].index(oname)]
            except ValueError:
                # when oname not in self._children
                pass
            else:
                return child.to_dynoption(subpath,
                                          self._suffix,
                                          self._opt)
        raise AttributeError(_('unknown option "{0}" '
                               'in dynamic optiondescription "{1}"'
                               '').format(name, self.impl_get_display_name()))

    def impl_getname(self) -> str:
        return self._opt.impl_getname() + self._suffix

    def impl_is_dynoptiondescription(self) -> bool:
        return True

    async def get_children(self,
                           config_bag: ConfigBag,
                           dyn: bool=True):
        subpath = self.impl_getpath()
        children = []
        for child in await self._opt.get_children(config_bag):
            children.append(child.to_dynoption(subpath,
                                               self._suffix,
                                               self._opt))
        return children

    async def get_children_recursively(self,
                                       bytype: Optional[BaseOption],
                                       byname: Optional[str],
                                       config_bag: ConfigBag,
                                       self_opt: BaseOption=None) -> BaseOption:
        async for option in self._opt.get_children_recursively(bytype,
                                                               byname,
                                                               config_bag,
                                                               self):
            yield option

    def impl_getpath(self) -> str:
        subpath = self._subpath
        if subpath != '':
            subpath += '.'
        return subpath + self.impl_getname()

    def impl_get_display_name(self) -> str:
        return self._opt.impl_get_display_name() + self._suffix


class SynDynLeadership(SynDynOptionDescription):
    def get_leader(self) -> SynDynOption:
        return self._opt.get_leader().to_dynoption(self.impl_getpath(),
                                                   self._suffix,
                                                   self.ori_dyn)

    def get_followers(self) -> Iterator[SynDynOption]:
        subpath = self.impl_getpath()
        for follower in self._opt.get_followers():
            yield follower.to_dynoption(subpath,
                                        self._suffix,
                                        self.ori_dyn)

    def reset_cache(self,
                    path: str,
                    config_bag: 'ConfigBag',
                    resetted_opts: List[str]) -> None:
        leader = self.get_leader()
        followers = self.get_followers()
        self._reset_cache(path,
                          leader,
                          followers,
                          config_bag,
                          resetted_opts)

    async def pop(self,
                  *args,
                  **kwargs) -> None:
        await self._opt.pop(*args,
                            followers=self.get_followers(),
                            **kwargs)

    async def follower_force_store_value(self,
                                         values,
                                         value,
                                         option_bag,
                                         owner) -> None:
        await self._opt.follower_force_store_value(values,
                                                   value,
                                                   option_bag,
                                                   owner,
                                                   dyn=self)
