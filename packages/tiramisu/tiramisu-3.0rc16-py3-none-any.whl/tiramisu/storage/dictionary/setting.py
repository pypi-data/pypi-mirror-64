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
from copy import deepcopy
from ...log import log


class Properties:
    __slots__ = ('_storage',)

    def __init__(self, storage):
        # properties attribute: the name of a property enables this property
        # key is None for global properties
        self._storage = storage

    # properties
    async def setproperties(self,
                            connection,
                            path,
                            index,
                            properties):
        log.debug('setproperties %s %s %s', path, index, properties)
        self._storage.get_properties().setdefault(path, {})[index] = properties

    async def getproperties(self,
                            connection,
                            path,
                            index,
                            default_properties):
        properties = self._storage.get_properties()
        if path not in properties:
            ret = frozenset(default_properties)
        else:
            ret = properties[path].get(index, frozenset(default_properties))
        log.debug('getproperties %s %s %s', path, index, ret)
        return ret

    async def delproperties(self,
                            connection,
                            path,
                            index):
        log.debug('delproperties %s', path)
        properties = self._storage.get_properties()
        if path in properties and index in properties[path]:
            del(properties[path][index])


    async def exportation(self,
                          connection):
        """return all modified settings in a dictionary
        example: {'path1': set(['prop1', 'prop2'])}
        """
        return deepcopy(self._storage.get_properties())

    async def importation(self,
                          connection,
                          properties):
        self._storage.set_properties(properties)

    def getconnection(self):
        return self._storage.getconnection()


class Permissives:
    __slots__ = ('_storage',)

    def __init__(self, storage):
        # permissive properties
        self._storage = storage

    async def setpermissives(self,
                             connection,
                             path,
                             index,
                             permissives):
        log.debug('setpermissives %s %s', path, permissives)
        self._storage.get_permissives().setdefault(path, {})[index] = permissives

    async def getpermissives(self,
                             connection,
                             path,
                             index):
        permissives = self._storage.get_permissives()
        if not path in permissives:
            ret = frozenset()
        else:
            ret = permissives[path].get(index, frozenset())
        log.debug('getpermissives %s %s', path, ret)
        return ret

    async def delpermissive(self,
                            connection,
                            path,
                            index):
        log.debug('delpermissive %s', path)
        permissives = self._storage.get_permissives()
        if path in permissives and index in permissives[path]:
            del(permissives[path][index])

    async def exportation(self,
                          connection):
        """return all modified permissives in a dictionary
        example: {'path1': set(['perm1', 'perm2'])}
        """
        return deepcopy(self._storage.get_permissives())

    async def importation(self,
                          connection,
                          permissives):
        self._storage.set_permissives(permissives)

    def getconnection(self):
        return self._storage.getconnection()
