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
from ipaddress import ip_address, ip_network

from ..error import ConfigError
from ..setting import undefined, Undefined, OptionBag
from ..i18n import _
from .option import Option


class BroadcastOption(Option):
    __slots__ = tuple()
    _type = 'broadcast_address'
    _display_name = _('broadcast address')

    def validate(self,
                 value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(_('invalid string'))
        if value.count('.') != 3:
            raise ValueError()
        for val in value.split('.'):
            if val.startswith("0") and len(val) > 1:
                raise ValueError()
        try:
            ip_address(value)
        except ValueError:
            raise ValueError()
