# -*- coding: utf-8 -*-
"default plugin for value: set it in a simple dictionary"
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
from ...setting import undefined
from ...i18n import _
from ...log import log
from .storage import delete_session

from copy import deepcopy


class Values:
    __slots__ = ('_values',
                 '_informations',
                 '_storage',
                 '__weakref__')
    def __init__(self, storage):
        """init plugin means create values storage
        """
        #self._values = ([], [], [], [])
        #self._informations = {}
        self._storage = storage

    def _setvalue_info(self, nb, idx, value, index, follower_idx=None):
        lst = self._storage.get_values()[nb]
        if index is None or nb == 0:
            # not follower or path
            lst[idx] = value
        else:
            # follower
            if nb == 1 and index in lst[idx]:
                follower_idx = lst[idx].index(index)
            tval = list(lst[idx])
            if follower_idx is None:
                tval.append(value)
            else:
                tval[follower_idx] = value
            lst[idx] = tval
        return follower_idx

    def _add_new_value(self, index, nb, value):
        if index is None or nb == 0:
            # not follower or path
            self._storage.get_values()[nb].append(value)
        else:
            # follower
            self._storage.get_values()[nb].append([value])

    def _add_new_value(self, index, nb, value):
        if index is None or nb == 0:
            # not follower or path
            self._storage.get_values()[nb].append(value)
        else:
            # follower
            self._storage.get_values()[nb].append([value])

    # value
    async def setvalue(self,
                       connection,
                       path,
                       value,
                       owner,
                       index,
                       new=False):
        """set value for a path
        a specified value must be associated to an owner
        """
        log.debug('setvalue %s %s %s %s %s', path, value, owner, index, id(self))

        #if isinstance(value, list):
        #    value = value
        values = self._storage.get_values()
        if not new and path in values[0]:
            idx = values[0].index(path)
            self._setvalue_info(0, idx, path, index)
            follower_idx = self._setvalue_info(1, idx, index, index)
            self._setvalue_info(2, idx, value, index, follower_idx)
            self._setvalue_info(3, idx, owner, index, follower_idx)
        else:
            self._add_new_value(index, 0, path)
            self._add_new_value(index, 1, index)
            self._add_new_value(index, 2, value)
            self._add_new_value(index, 3, owner)

    async def hasvalue(self,
                       connection,
                       path,
                       index=None):
        """if path has a value
        return: boolean
        """
        values = self._storage.get_values()
        has_path = path in values[0]
        log.debug('hasvalue %s %s %s %s', path, index, has_path, id(self))
        if index is None:
            return has_path
        elif has_path:
            path_idx = values[0].index(path)
            indexes = values[1][path_idx]
            return index in indexes
        return False

    async def reduce_index(self,
                           connection,
                           path,
                           index):
        """
        _values == ((path1, path2), ((idx1_1, idx1_2), None), ((value1_1, value1_2), value2), ((owner1_1, owner1_2), owner2))
        """
        log.debug('reduce_index %s %s %s', path, index, id(self))
        values = self._storage.get_values()
        path_idx = values[0].index(path)
        # get the "index" position
        subidx = values[1][path_idx].index(index)
        # reduce to one the index
        values[1][path_idx][subidx] -= 1

    async def resetvalue_index(self,
                               connection,
                               path,
                               index):
        log.debug('resetvalue_index %s %s %s', path, index, id(self))
        values = self._storage.get_values()
        def _resetvalue(nb):
            del self._storage.get_values()[nb][path_idx]

        def _resetvalue_index(nb):
            del self._storage.get_values()[nb][path_idx][subidx]

        path_idx = values[0].index(path)
        indexes = values[1][path_idx]
        if index in indexes:
            subidx = indexes.index(index)
            if len(values[1][path_idx]) == 1:
                _resetvalue(0)
                _resetvalue(1)
                _resetvalue(2)
                _resetvalue(3)
            else:
                _resetvalue_index(1)
                _resetvalue_index(2)
                _resetvalue_index(3)

    async def resetvalue(self,
                         connection,
                         path):
        """remove value means delete value in storage
        """
        log.debug('resetvalue %s %s', path, id(self))
        values = self._storage.get_values()
        def _resetvalue(nb):
            values[nb].pop(idx)
        if path in values[0]:
            idx = values[0].index(path)
            _resetvalue(0)
            _resetvalue(1)
            _resetvalue(2)
            _resetvalue(3)

    # owner
    async def setowner(self,
                       connection,
                       path,
                       owner,
                       index):
        """change owner for a path
        """
        values = self._storage.get_values()
        idx = values[0].index(path)
        if index is None:
            follower_idx = None
        else:
            follower_idx = values[1][idx].index(index)
        self._setvalue_info(3, idx, owner, index, follower_idx)

    async def getowner(self,
                       connection,
                       path,
                       default,
                       index=None,
                       with_value=False):
        """get owner for a path
        return: owner object
        """
        owner, value = self._getvalue(path,
                                      index,
                                      with_value)
        if owner is undefined:
            owner = default
        log.debug('getvalue %s %s %s %s %s', path, index, value, owner, id(self))
        if with_value:
            return owner, value
        else:
            return owner

    def _getvalue(self,
                  path,
                  index,
                  with_value):
        """
        _values == ((path1, path2), ((idx1_1, idx1_2), None), ((value1_1, value1_2), value2), ((owner1_1, owner1_2), owner2))
        """
        values = self._storage.get_values()
        value = undefined
        if path in values[0]:
            path_idx = values[0].index(path)
            indexes = values[1][path_idx]
            if indexes is None:
                if index is not None:  # pragma: no cover
                    raise ValueError('index is forbidden for {}'.format(path))
                owner = values[3][path_idx]
                if with_value:
                    value = values[2][path_idx]
            else:
                if index is None:  # pragma: no cover
                    raise ValueError('index is mandatory for {}'.format(path))
                if index in indexes:
                    subidx = indexes.index(index)
                    owner = values[3][path_idx][subidx]
                    if with_value:
                        value = values[2][path_idx][subidx]
                else:
                    owner = undefined
        else:
            owner = undefined
        if isinstance(value, tuple):
            value = list(value)
        return owner, value

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
        informations = self._storage.get_informations()
        informations.setdefault(path, {})
        informations[path][key] = value

    async def get_information(self,
                              connection,
                              path,
                              key,
                              default):
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        value = self._storage.get_informations().get(path, {}).get(key, default)
        if value is undefined:
            raise ValueError(_("information's item"
                               " not found: {0}").format(key))
        return value

    async def del_information(self,
                              connection,
                              path,
                              key,
                              raises):
        informations = self._storage.get_informations()
        if path in informations and key in informations[path]:
            del informations[path][key]
        else:
            if raises:
                raise ValueError(_("information's item not found {0}").format(key))

    async def list_information(self,
                               connection,
                               path):
        informations = self._storage.get_informations()
        if path in informations:
            return informations[path].keys()
        else:
            return []

    async def del_informations(self,
                               connection):
        self._storage.set_informations({})

    async def exportation(self,
                          connection):
        return deepcopy(self._storage.get_values())

    async def importation(self,
                          connection,
                          export):
        self._storage.set_values(deepcopy(export))

    async def get_max_length(self,
                             connection,
                             path):
        values = self._storage.get_values()
        if path in values[0]:
            idx = values[0].index(path)
        else:
            return 0
        return max(values[1][idx]) + 1

    def getconnection(self):
        return self._storage.getconnection()
