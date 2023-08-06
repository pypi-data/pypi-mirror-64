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

from ..i18n import _
from .stroption import RegexpOption


class UsernameOption(RegexpOption):
    __slots__ = tuple()
    #regexp build with 'man 8 adduser' informations
    _regexp = re.compile(r"^[a-z_][a-z0-9_-]{0,30}[$a-z0-9_-]{0,1}$")
    _type = 'username'
    _display_name = _('unix username')


class GroupnameOption(UsernameOption):
    __slots__ = tuple()
    _type = 'groupname'
    _display_name = _('unix groupname')
