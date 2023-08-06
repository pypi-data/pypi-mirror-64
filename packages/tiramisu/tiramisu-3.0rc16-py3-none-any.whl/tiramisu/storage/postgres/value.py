# -*- coding: utf-8 -*-
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
from ...setting import undefined, owners
from ...i18n import _
from ...log import log
from .storage import delete_session


class Values:
    __slots__ = ('__weakref__',
                 '_storage')

    def __init__(self,
                 storage):
        """init plugin means create values storage
        """
        self._storage = storage

    # value
    async def setvalue(self,
                       connection,
                       path,
                       value,
                       owner,
                       index,
                       new=False):
        """set value for an option
        a specified value must be associated to an owner
        """
        # log.debug('setvalue %s %s %s %s %s', path, value, owner, index, commit)
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        sql = 'INSERT INTO value(value, owner, session_id, path, idx) VALUES ($1,$2,$3,$4,$5)'
        idx = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        params = [dumps(value), str(owner), self._storage.database_id, path, idx]
        if new is False:
            if index != -1:
                await self.resetvalue_index(connection,
                                            path,
                                            index)
            else:
                await self.resetvalue(connection,
                                      path)
        await connection.execute(sql,
                                 *params)

    async def hasvalue(self,
                       connection,
                       path,
                       index=None):
        """if opt has a value
        return: boolean
        """
        # log.debug('hasvalue %s %s', path, index)
        if index is not None:
            index = self._storage.convert_index(index)
            path = self._storage.convert_path(path)
            request = "SELECT value FROM value WHERE path = $1 AND session_id = $2  AND idx = $3"
            params = (path, self._storage.database_id, index)
        else:
            path = self._storage.convert_path(path)
            request = "SELECT value FROM value WHERE path = $1 AND session_id = $2"
            params = (path, self._storage.database_id)
        ret = await connection.fetchrow(request, *params)
        return ret is not None


    async def reduce_index(self,
                           connection,
                           path,
                           index):
        """
        _values == ((path1, path2), ((idx1_1, idx1_2), None),
                    ((value1_1, value1_2), value2), ((owner1_1, owner1_2), owner2))
        """
        # log.debug('reduce_index %s %s %s', path, index, id(self))
        await connection.execute("UPDATE value SET idx = $1 WHERE path = $2 and idx = $3 "
                                 "AND session_id = $4",
                                 index - 1, path, index, self._storage.database_id)

    async def resetvalue_index(self,
                               connection,
                               path,
                               index):
        """remove value means delete value in storage
        """
        # log.debug('resetvalue_index %s %s', path, index)
        await connection.execute("DELETE FROM value WHERE path = $1 AND session_id = $2 AND idx = $3",
                                 path, self._storage.database_id, index)
        await self.hasvalue(connection,
                            path,
                            index)

    async def resetvalue(self,
                         connection,
                         path):
        """remove value means delete value in storage
        """
        # log.debug('resetvalue %s', path)
        await connection.execute("DELETE FROM value WHERE path = $1 AND session_id = $2",
                                 path, self._storage.database_id)

    # owner
    async def setowner(self,
                       connection,
                       path,
                       owner,
                       index):
        """change owner for an option
        """
        # log.debug('setowner %s %s %s', path, owner, index)
        index = self._storage.convert_index(index)
        path = self._storage.convert_path(path)
        await connection.execute("UPDATE value SET owner = $1 WHERE path = $2 and idx = $3 AND session_id = $4",
                                 str(owner), path, index, self._storage.database_id)

    async def getowner(self,
                       connection,
                       path,
                       default,
                       index,
                       with_value=False):
        """get owner for an option
        return: owner object
        """
        # log.debug('getowner %s %s %s %s', path, default, index, with_value)
        path = self._storage.convert_path(path)
        index = self._storage.convert_index(index)
        request = "SELECT owner, value FROM value WHERE session_id = $1 AND path = $2 AND idx = $3"
        params = [self._storage.database_id, path, index]
        owner = await connection.fetchrow(request, *params)
        if owner is None:
            if not with_value:
                return default
            return default, None
        # autocreate owners
        try:
            nowner = getattr(owners, owner[0])
        except AttributeError:  # pragma: no cover
            owners.addowner(owner[0])
            nowner = getattr(owners, owner[0])
        if not with_value:
            return nowner
        value = loads(owner[1])
        return nowner, value

    async def set_information(self,
                              connection,
                              path,
                              key,
                              value):
        """updates the information's attribute
        (which is a dictionary)

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        # log.debug('set_information %s %s', key, value)
        path = self._storage.convert_path(path)
        await connection.execute("DELETE FROM information WHERE key = $1 AND session_id = $2 AND path = $3",
                                 key, self._storage.database_id, path)
        await connection.execute("INSERT INTO information(key, value, session_id, path) VALUES "
                                 "($1, $2, $3, $4)", key, dumps(value), self._storage.database_id, path)

    async def get_information(self,
                              connection,
                              path,
                              key,
                              default):
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        # log.debug('get_information %s %s', key, default)
        path = self._storage.convert_path(path)
        value = await connection.fetchval("SELECT value FROM information WHERE key = $1 AND "
                                          "session_id = $2 AND path = $3",
                                          key, self._storage.database_id, path)
        if value is None:
            if default is undefined:
                raise ValueError(_("information's item"
                                   " not found: {0}").format(key))
            return default
        else:
            return loads(value)

    async def del_information(self,
                              connection,
                              path,
                              key,
                              raises):
        # log.debug('del_information %s %s', key, raises)
        path = self._storage.convert_path(path)
        information = await connection.fetchval("SELECT value FROM information WHERE key = $1 "
                                                "AND session_id = $2 AND path = $3",
                                                key, self._storage.database_id, path)
        if raises and information is None:
            raise ValueError(_("information's item not found {0}").format(key))
        await connection.execute("DELETE FROM information WHERE key = $1 AND session_id = $2 AND path = $3",
                                 key, self._storage.database_id, path)

    async def list_information(self,
                               connection,
                               path):
        path = self._storage.convert_path(path)
        return [row[0] for row in await connection.fetch("SELECT key FROM information WHERE session_id = $1 AND path = $2",
                                                         self._storage.database_id, path)]

    async def del_informations(self,
                               connection):
        await connection.execute("DELETE FROM information WHERE session_id = $1",
                                 self._storage.database_id)

    async def exportation(self,
                          connection):
        # log.debug('exportation')
        ret = [[], [], [], []]
        rows = await connection.fetch("SELECT path, value, owner, idx FROM value WHERE "
                                      "session_id = $1", self._storage.database_id)
        for row in rows:
            path = self._storage.load_path(row[0])
            value = loads(row[1])
            owner = row[2]
            index = self._storage.load_index(row[3])
            if index is None:
                ret[0].append(path)
                ret[1].append(index)
                ret[2].append(value)
                ret[3].append(owner)
            else:
                if path in ret[0]:
                    path_idx = ret[0].index(path)
                    ret[1][path_idx].append(index)
                    ret[2][path_idx].append(value)
                    ret[3][path_idx].append(owner)
                else:
                    ret[0].append(path)
                    ret[1].append([index])
                    ret[2].append([value])
                    ret[3].append([owner])
        return ret

    async def importation(self,
                          connection,
                          export):
        # log.debug('importation')
        request = "DELETE FROM value WHERE session_id = $1"
        await connection.execute(request, self._storage.database_id)
        for idx, path in enumerate(export[0]):
            path = self._storage.convert_path(path)
            index = self._storage.convert_index(export[1][idx])
            value = export[2][idx]
            owner = export[3][idx]
            if index == -1:
                await connection.execute("INSERT INTO value(path, value, owner, idx, session_id) VALUES "
                                         "($1, $2, $3, $4, $5)", path, dumps(value),
                                                            str(owner), index,
                                                            self._storage.database_id)
            else:
                for val in zip(index, value, owner):
                    await connection.execute("INSERT INTO value(path, value, owner, idx, session_id)"
                                             "VALUES ($1, $2, $3, $4, $5)", path,
                                                                            dumps(val[1]),
                                                                            str(val[2]), val[0],
                                                                            self._storage.database_id)

    async def get_max_length(self,
                             connection,
                             path):
        # log.debug('get_max_length %s', path)
        val_max = await connection.fetchval("SELECT max(idx) FROM value WHERE path = $1 AND session_id = $2",
                                            path, self._storage.database_id)
        if val_max is None:
            return 0
        return val_max + 1

    def getconnection(self):
        return self._storage.getconnection()
