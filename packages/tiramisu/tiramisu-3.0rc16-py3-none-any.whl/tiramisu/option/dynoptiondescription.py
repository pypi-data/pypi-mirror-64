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
import re
from typing import List, Callable


from ..i18n import _
from .optiondescription import OptionDescription
from .baseoption import BaseOption
from ..setting import OptionBag, ConfigBag, groups, undefined
from ..error import ConfigError
from ..autolib import Calculation


NAME_REGEXP = re.compile(r'^[a-zA-Z\d\-_]*$')


class DynOptionDescription(OptionDescription):
    __slots__ = ('_suffixes',)

    def __init__(self,
                 name: str,
                 doc: str,
                 children: List[BaseOption],
                 suffixes: Calculation,
                 properties=None) -> None:

        super().__init__(name,
                         doc,
                         children,
                         properties)
        # check children + set relation to this dynoptiondescription
        for child in children:
            if isinstance(child, OptionDescription):
                if __debug__ and child.impl_get_group_type() != groups.leadership:
                    raise ConfigError(_('cannot set optiondescription in a '
                                        'dynoptiondescription'))
                for chld in child._children[1]:
                    chld._setsubdyn(self)
            if __debug__ and child.impl_is_symlinkoption():
                raise ConfigError(_('cannot set symlinkoption in a '
                                    'dynoptiondescription'))
            child._setsubdyn(self)
        # add suffixes
        if __debug__ and isinstance(suffixes, Calculation):
            self._suffixes = suffixes

    def convert_suffix_to_path(self,
                               suffix):
        return suffix

    async def get_suffixes(self,
                           config_bag: ConfigBag) -> List[str]:
        option_bag = OptionBag()
        option_bag.set_option(self,
                              None,
                              config_bag)
        values = await self._suffixes.execute(option_bag)
        if __debug__:
            if not isinstance(values, list):
                raise ValueError(_('DynOptionDescription suffixes for option "{}", is not a list ({})'
                                   '').format(self.impl_get_display_name(), values))
            values_ = []
            for val in values:
                val = self.convert_suffix_to_path(val)
                if not isinstance(val, str) or re.match(NAME_REGEXP, val) is None:
                    if val is not None:
                        raise ValueError(_('invalid suffix "{}" for option "{}"'
                                           '').format(val,
                                                      self.impl_get_display_name()))
                else:
                    values_.append(val)
            if len(values_) > len(set(values_)):
                extra_values = values_.copy()
                for val in set(values_):
                    extra_values.remove(val)
                raise ValueError(_('DynOptionDescription suffixes return a list with multiple value '
                                   '"{}"''').format(extra_values))
            values = values_
        return values

    def impl_is_dynoptiondescription(self) -> bool:
        return True
