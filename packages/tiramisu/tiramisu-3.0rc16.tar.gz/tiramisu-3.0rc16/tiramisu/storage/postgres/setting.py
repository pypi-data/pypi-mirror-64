# -*- coding: utf-8 -*-
"default plugin for setting: set it in a simple dictionary"
# Copyright (C) 2020 Team tiramisu (see AUTHORS for all contributors)
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
try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps
from ...log import log


class Properties:
    __slots__ = ('_storage',)

    def __init__(self, storage):
        self._storage = storage

    # properties
    async def setproperties(self,
                            connection,
                            path,
                            index,
                            properties):
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        await self.delproperties(connection, path, index)
        sql = "INSERT INTO property(path, idx, properties, session_id) VALUES ($1, $2, $3, $4)"
        params = [path, index, dumps(properties), self._storage.database_id]
        await connection.execute(sql, *params)

    async def getproperties(self,
                            connection,
                            path,
                            index,
                            default_properties):
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        sql = 'SELECT properties FROM property WHERE path = $1 AND session_id = $2 AND idx = $3'
        params = [path, self._storage.database_id, index]
        value = await connection.fetchval(sql, *params)
        if value is None:
            return set(default_properties)
        else:
            return set(loads(value))

    async def delproperties(self,
                            connection,
                            path,
                            index):
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        sql = 'DELETE FROM property WHERE session_id = $1 AND path = $2 AND idx = $3'
        params = [self._storage.database_id, path, index]
        await connection.execute(sql, *params)

    async def exportation(self,
                          connection):
        """return all modified settings in a dictionary
        example: {'path1': set(['prop1', 'prop2'])}
        """
        ret = {}
        for path, idx, properties, _ in await connection.fetch("SELECT * FROM property "
                                                                       "WHERE session_id = $1",
                                                                       self._storage.database_id):
            idx = self._storage.load_index(idx)
            path = self._storage.load_path(path)
            ret.setdefault(path, {})[idx] = loads(properties)
        return ret

    async def importation(self,
                          connection,
                          properties):
        await connection.execute("DELETE FROM property WHERE session_id = $1", self._storage.database_id)
        for path, indexed_properties in properties.items():
            path = self._storage.convert_path(path)
            for index, property_ in indexed_properties.items():
                index = self._storage.convert_index(index)
                await connection.execute("INSERT INTO property(path, idx, properties, session_id) "
                                         "VALUES ($1,$2,$3,$4)", path,
                                                                 index,
                                                                 dumps(property_),
                                                                 self._storage.database_id)

    def getconnection(self):
        return self._storage.getconnection()


class Permissives:
    __slots__ = ('_storage',)

    def __init__(self,
                 storage):
        self._storage = storage

    # permissive
    async def setpermissives(self,
                             connection,
                             path,
                             index,
                             permissive):
        # log.debug('setpermissive %s %s %s %s', path, index, permissive, id(self))
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        await self.delpermissive(connection,
                                 path,
                                 index)
        await connection.execute("INSERT INTO permissive(path, idx, permissives, session_id) "
                                 "VALUES ($1,$2,$3,$4)", path,
                                                         index,
                                                         dumps(permissive),
                                                         self._storage.database_id)

    async def getpermissives(self,
                             connection,
                             path,
                             index):
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        sql = 'SELECT permissives FROM permissive WHERE session_id = $1 AND path = $2 AND idx = $3'
        params = [self._storage.database_id, path, index]
        permissives = await connection.fetchval(sql,
                                                *params)
        if permissives is None:
            return frozenset()
        else:
            return loads(permissives)
        # log.debug('getpermissive %s %s %s', path, ret, id(self))

    async def delpermissive(self,
                            connection,
                            path,
                            index):
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        sql = 'DELETE FROM permissive WHERE session_id = $1 AND path = $2 AND idx = $3'
        params = [self._storage.database_id, path, index]
        await connection.execute(sql, *params)

    async def exportation(self,
                          connection):
        """return all modified permissives in a dictionary
        example: {'path1': set(['perm1', 'perm2'])}
        """
        ret = {}
        sql = "SELECT path, idx, permissives FROM permissive WHERE session_id = $1"
        for path, index, permissives in await connection.fetch(sql,
                                                               self._storage.database_id):
            ret.setdefault(self._storage.load_path(path), {})[self._storage.load_index(index)] = loads(permissives)
        return ret

    async def importation(self,
                          connection,
                          permissives):
        await connection.execute("DELETE FROM permissive WHERE session_id = $1", self._storage.database_id)
        for path, indexed_permissives in permissives.items():
            for index, permissive in indexed_permissives.items():
                index = self._storage.convert_index(index)
                path = self._storage.convert_path(path)
                await connection.execute("INSERT INTO permissive(path, idx, permissives, session_id) "
                                         "VALUES ($1,$2,$3,$4)", path,
                                                                 index,
                                                                 dumps(permissive),
                                                                 self._storage.database_id)

    def getconnection(self):
        return self._storage.getconnection()
