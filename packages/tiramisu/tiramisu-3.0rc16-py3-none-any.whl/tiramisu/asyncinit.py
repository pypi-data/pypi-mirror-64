# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Team tiramisu (see AUTHORS for all contributors)
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
# largely inspired by https://github.com/kchmck/pyasyncinit
# ____________________________________________________________
from functools import wraps


def asyncinit(obj):
    @wraps(obj.__new__)
    async def new(cls, *args, **kwargs):
        instance = object.__new__(cls)  # (cls, *args, **kwargs)
        await instance.__init__(*args, **kwargs)
        return instance
    obj.__new__ = new
    return obj
