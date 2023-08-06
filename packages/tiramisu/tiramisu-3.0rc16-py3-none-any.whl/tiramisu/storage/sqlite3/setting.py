# -*- coding: utf-8 -*-
"default plugin for setting: set it in a simple dictionary"
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
from .sqlite3db import Sqlite3DB
from ...log import log


class Properties(Sqlite3DB):
    __slots__ = tuple()

    def __init__(self, storage):
        super(Properties, self).__init__(storage)

    # properties
    async def setproperties(self,
                            connection,
                            path,
                            index,
                            properties):
        await self.delproperties(connection,
                                 path,
                                 index)
        await connection.execute("INSERT INTO property(path, tiram_index, properties, session_id) VALUES "
                                 "(?, ?, ?, ?)", (path,
                                                  index,
                                                  self._sqlite_encode(properties),
                                                  self._session_id))

    async def getproperties(self,
                            connection,
                            path,
                            index,
                            default_properties):
        sql = 'SELECT properties FROM property WHERE session_id = ? '
        params = [self._session_id]
        if path is None:
             sql += "AND path is NULL "
        else:
             sql += "AND path = ? "
             params.append(path)
        if index is None:
             sql += "AND tiram_index is NULL LIMIT 1"
        else:
             sql += "AND tiram_index = ? LIMIT 1"
             params.append(index)
        value = await connection.select(sql, params)
        if value is None:
            return set(default_properties)
        else:
            return set(self._sqlite_decode(value[0]))

    async def delproperties(self,
                            connection,
                            path,
                            index):
        sql = 'DELETE FROM property WHERE session_id = ? '
        params = [self._session_id]
        if path is None:
            sql += 'AND path is NULL '
        else:
            sql += 'AND path = ? '
            params.append(path)
        if index is None:
            sql += 'AND tiram_index is NULL'
        else:
            params.append(index)
            sql += 'AND tiram_index = ?'
        await connection.execute(sql, params)

    async def exportation(self,
                          connection):
        """return all modified settings in a dictionary
        example: {'path1': set(['prop1', 'prop2'])}
        """
        ret = {}
        for path, tiram_index, properties, _ in await connection.select("SELECT * FROM property "
                                                                        "WHERE session_id = ?",
                                                                        (self._session_id,),
                                                                        only_one=False):
            ret.setdefault(path, {})[tiram_index] = self._sqlite_decode(properties)
        return ret

    async def importation(self,
                          connection,
                          properties):
        await connection.execute("DELETE FROM property WHERE session_id = ?", (self._session_id,))
        for path, indexed_properties in properties.items():
            for index, property_ in indexed_properties.items():
                await connection.execute("INSERT INTO property(path, tiram_index, properties, session_id) "
                                         "VALUES (?, ?, ?, ?)", (path,
                                                                 index,
                                                                 self._sqlite_encode(property_),
                                                                 self._session_id,
                                                                 ))

    def getconnection(self):
        return self._storage.getconnection()


class Permissives(Sqlite3DB):
    __slots__ = tuple()

    # permissive
    async def setpermissives(self,
                             connection,
                             path,
                             index,
                             permissive):
        log.debug('setpermissive %s %s %s %s', path, index, permissive, id(self))
        await self.delpermissive(connection,
                                 path,
                                 index)
        await connection.execute("INSERT INTO permissive(path, tiram_index, permissives, session_id) "
                                 "VALUES (?, ?, ?, ?)", (path,
                                                         index,
                                                         self._sqlite_encode(permissive),
                                                         self._session_id))

    async def getpermissives(self,
                             connection,
                             path,
                             index):
        sql = 'SELECT permissives FROM permissive WHERE session_id = ? '
        params = [self._session_id]
        if path is None:
             sql += "AND path is NULL "
        else:
             sql += "AND path = ? "
             params.append(path)
        if index is None:
             sql += "AND tiram_index is NULL LIMIT 1"
        else:
             sql += "AND tiram_index = ? LIMIT 1"
             params.append(index)
        permissives = await connection.select(sql, params)
        if permissives is None:
            ret = frozenset()
        else:
            ret = frozenset(self._sqlite_decode(permissives[0]))
        log.debug('getpermissive %s %s %s', path, ret, id(self))
        return ret

    async def delpermissive(self,
                            connection,
                            path,
                            index):
        sql = 'DELETE FROM permissive WHERE session_id = ? '
        params = [self._session_id]
        if path is None:
            sql += 'AND path is NULL '
        else:
            sql += 'AND path = ? '
            params.append(path)
        if index is None:
            sql += 'AND tiram_index is NULL'
        else:
            params.append(index)
            sql += 'AND tiram_index = ?'
        await connection.execute(sql, params)

    async def exportation(self,
                          connection):
        """return all modified permissives in a dictionary
        example: {'path1': set(['perm1', 'perm2'])}
        """
        ret = {}
        sql = "SELECT path, tiram_index, permissives FROM permissive WHERE session_id = ?"
        for path, index, permissives in await connection.select(sql,
                                                                (self._session_id,),
                                                                only_one=False):
            ret.setdefault(path, {})[index] = self._sqlite_decode(permissives)
        return ret

    async def importation(self,
                          connection,
                          permissives):
        await connection.execute("DELETE FROM permissive WHERE session_id = ?", (self._session_id,))
        for path, indexed_permissives in permissives.items():
            for index, permissive in indexed_permissives.items():
                await connection.execute("INSERT INTO permissive(path, tiram_index, permissives, session_id) "
                                         "VALUES (?, ?, ?, ?)", (path,
                                                                 index,
                                                                 self._sqlite_encode(permissive),
                                                                 self._session_id,
                                                                 ))
