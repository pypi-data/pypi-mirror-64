# -*- coding: utf-8 -*-
# Copyright (C) 2018-2020 Team tiramisu (see AUTHORS for all contributors)
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
from typing import Any
from ..setting import undefined, OptionBag
from .baseoption import BaseOption


class SynDynOption:
    """SynDynOption is an Option include un DynOptionDescription with specified prefix
    """
    __slots__ = ('rootpath',
                 'opt',
                 'suffix',
                 'ori_dyn',
                 '__weakref__')

    def __init__(self,
                 opt: BaseOption,
                 rootpath: str,
                 suffix: str,
                 ori_dyn) -> None:
        self.opt = opt
        self.rootpath = rootpath
        self.suffix = suffix
        self.ori_dyn = ori_dyn

    def __getattr__(self,
                    name: str) -> Any:
        return getattr(self.opt,
                       name)

    def __eq__(self,
               left: BaseOption) -> bool:
        if not isinstance(left, SynDynOption):
            return False
        return self.opt == left.opt and \
               self.rootpath == left.rootpath and \
               self.suffix == left.suffix

    def impl_getname(self) -> str:
        return self.opt.impl_getname() + self.suffix

    def impl_get_display_name(self) -> str:
        return self.opt.impl_get_display_name(dyn_name=self.impl_getname()) + self.suffix

    def impl_getsuffix(self) -> str:
        return self.suffix

    def impl_getpath(self) -> str:
        return self.rootpath + '.' + self.impl_getname()

    def impl_is_dynsymlinkoption(self) -> bool:
        return True

    def impl_get_leadership(self):
        leadership = self.opt.impl_get_leadership()
        if leadership:
            return leadership.to_dynoption(self.rootpath,
                                           self.suffix,
                                           self.ori_dyn)
