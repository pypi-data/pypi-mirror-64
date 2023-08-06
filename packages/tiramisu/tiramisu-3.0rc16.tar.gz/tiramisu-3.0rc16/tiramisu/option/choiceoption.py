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
from typing import Any

from ..setting import undefined, OptionBag
from ..i18n import _
from .option import Option
from ..autolib import Calculation
from ..error import ConfigError, display_list


class ChoiceOption(Option):
    """represents a choice out of several objects.

    The option can also have the value ``None``
    """
    __slots__ = tuple()
    _type = 'choice'
    _display_name = _('choice')

    def __init__(self,
                 name,
                 doc,
                 values,
                 *args,
                 **kwargs):

        """
        :param values: is a list of values the option can possibly take
        """
        if not isinstance(values, (Calculation, tuple)):
            raise TypeError(_('values must be a tuple or a calculation for {0}'
                             ).format(name))
        self._choice_values = values
        super().__init__(name,
                         doc,
                         *args,
                         **kwargs)

    async def impl_get_values(self,
                              option_bag):
        if isinstance(self._choice_values, Calculation):
            values = await self._choice_values.execute(option_bag)
            if values is not undefined and not isinstance(values, list):
                raise ConfigError(_('calculated values for {0} is not a list'
                                    '').format(self.impl_getname()))
        else:
            values = self._choice_values
        return values

    def validate(self,
                 value: Any) -> None:
        pass

    def sync_validate_with_option(self,
                                  value: Any,
                                  option_bag: OptionBag) -> None:
        if isinstance(self._choice_values, Calculation):
            return
        values = self._choice_values
        if values is not undefined and value not in values:
            if len(values) == 1:
                raise ValueError(_('only "{0}" is allowed'
                                   '').format(values[0]))
            raise ValueError(_('only {0} are allowed'
                               '').format(display_list(values, add_quote=True)))

    async def validate_with_option(self,
                                   value: Any,
                                   option_bag: OptionBag) -> None:
        values = await self.impl_get_values(option_bag)
        if values is not undefined and value not in values:
            if len(values) == 1:
                raise ValueError(_('only "{0}" is allowed'
                                   '').format(values[0]))
            raise ValueError(_('only {0} are allowed'
                               '').format(display_list(values, add_quote=True)))
