# -*- coding: utf-8 -*-
# Copyright (C) 2013-2020 Team tiramisu (see AUTHORS for all contributors)
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
# ____________________________________________________________
from ...i18n import _
from ...error import ConflictError
from ...asyncinit import asyncinit


class Setting:
    """Dictionary storage has no particular setting.
    """
    __slots__ = tuple()


SETTING = Setting()
_list_sessions = {}
PERSISTENT = True


async def init():
    pass


class Connection:
    async def __aenter__(self):
        return self

    async def __aexit__(self,
                        type,
                        value,
                        traceback):
        pass


async def list_sessions():
    lst = list(_list_sessions.keys())
    if '__validator_storage' in lst:
        lst.remove('__validator_storage')
    return lst


async def delete_session(session_id):
    try:
        del _list_sessions[session_id]
    except KeyError:
        pass


@asyncinit
class Storage:
    __slots__ = ('session_id',)
    storage = 'dictionary'

    def add_session(self):
        # values (('path1',), (index1,), (value1,), ('owner1'))
        _list_sessions[self.session_id] = {'values': ([], [], [], []),
                                           'informations': {},
                                           'properties': {},
                                           'permissives': {}}

    async def __init__(self,
                       connection: Connection,
                       session_id: str,
                       delete_old_session: bool) -> None:
        if not isinstance(session_id, str):
            raise ValueError(_('session_id has to be a string'))
        self.session_id = session_id
        if self.session_id not in _list_sessions:
            self.add_session()

    async def delete_session(self):
        await delete_session(self.session_id)

    async def list_sessions(self):
        return await list_sessions()

    def get_session(self):
        if self.session_id not in _list_sessions:
            self.add_session()
        return _list_sessions.get(self.session_id, {})

    def get_values(self):
        return self.get_session()['values']

    def set_values(self, values):
        self.get_session()['values'] = values

    def get_informations(self):
        return self.get_session()['informations']

    def set_informations(self, informations):
        self.get_session()['informations'] = informations

    def get_properties(self):
        return self.get_session()['properties']

    def set_properties(self, properties):
        self.get_session()['properties'] = properties

    def get_permissives(self):
        return self.get_session()['permissives']

    def set_permissives(self, permissives):
        self.get_session()['permissives'] = permissives

    def getconnection(self):
        return Connection()
