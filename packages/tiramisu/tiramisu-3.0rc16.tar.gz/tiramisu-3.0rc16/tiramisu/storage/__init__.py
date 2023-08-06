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

"""Config's informations are, by default, volatiles. This means, all values and
settings changes will be lost.

The storage is the system Tiramisu uses to communicate with various DB.

Storage is basic components used to set Config informations in DB.
"""


from time import time
from random import randint
from os import environ
from os.path import split
from typing import Dict
from ..error import ConfigError
from ..i18n import _
from .cacheobj import Cache


DEFAULT_STORAGE = MEMORY_STORAGE = 'dictionary'
MODULE_PATH = split(split(split(__file__)[0])[0])[1]


class Storage:
    """Object to store storage's type. If a Config is already set,
    default storage is store as selected storage. You cannot change it
    after.
    """
    def __init__(self,
                 engine=None) -> None:
        self.storage_type = engine
        self.mod = None
        self.kwargs = {}

    def engine(self,
               engine) -> None:
        if self.mod is not None:
            raise ValueError(_('cannot change setting when storage is already in use'))
        self.storage_type = engine

    def setting(self,
                **kwargs: Dict[str, str]) -> None:
        if self.mod is not None:
            raise ValueError(_('cannot change setting when storage is already in use'))
        self.kwargs = kwargs

    async def get(self):
        if self.storage_type is None:
            self.storage_type = environ.get('TIRAMISU_STORAGE', DEFAULT_STORAGE)
        if self.mod is None:
            modulepath = '{0}.storage.{1}'.format(MODULE_PATH,
                                                  self.storage_type)
            try:
                mod = __import__(modulepath)
            except ImportError:  # pragma: no cover
                raise SystemError(_('cannot import the storage {0}').format(
                    self.storage_type))
            for token in modulepath.split(".")[1:]:
                mod = getattr(mod, token)
            self.mod = mod
            for key, value in self.kwargs.items():
                setattr(mod.SETTING, key, value)
            del self.kwargs
            await self.mod.init()
        return self.mod


default_storage = Storage()
memory_storage = Storage(engine=MEMORY_STORAGE)


def gen_storage_id(session_id,
                   config):
    if session_id is not None:
        return session_id
    return 'c' + str(id(config)) + str(int(time())) + str(randint(0, 50000))


async def get_storages(context,
                       session_id,
                       delete_old_session,
                       storage,
                       connection):
    session_id = gen_storage_id(session_id,
                                context)
    if storage is None:
        storage = default_storage
    imp = await storage.get()
    imp_storage = await imp.Storage(connection,
                                    session_id,
                                    delete_old_session)
    properties = imp.Properties(imp_storage)
    permissives = imp.Permissives(imp_storage)
    values = imp.Values(imp_storage)
    return storage, properties, permissives, values, session_id


async def get_default_values_storages(connection):
    imp = await memory_storage.get()
    storage = await imp.Storage(connection,
                                '__validator_storage',
                                delete_old_session=True)
    return imp.Values(storage)


async def get_default_settings_storages(connection):
    imp = await memory_storage.get()
    storage = await imp.Storage(connection,
                                '__validator_storage',
                                delete_old_session=True)
    properties = imp.Properties(storage)
    permissives = imp.Permissives(storage)
    return properties, permissives


async def list_sessions(storage=default_storage):
    """List all available session
    """
    stor = await storage.get()
    return await stor.list_sessions()


async def delete_session(session_id,
                         storage=default_storage):
    """Delete a selected session, be careful, you can deleted a session
    use by an other instance
    :params session_id: id of session to delete
    """
    storage_module = await storage.get()
    await storage_module.value.delete_session(session_id)
    await storage_module.storage.delete_session(session_id)


__all__ = ('list_sessions', 'delete_session')
