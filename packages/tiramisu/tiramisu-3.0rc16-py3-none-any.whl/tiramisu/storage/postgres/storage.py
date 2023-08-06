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
from asyncpg import create_pool
from asyncpg.exceptions import UniqueViolationError
import warnings
from os.path import join
from typing import Optional, Dict

from ...i18n import _
from ...error import ConflictError
from ...asyncinit import asyncinit


class Setting:
    """:param dsn: something like postgres://tiramisu:tiramisu@localhost:5432/tiramisu
    """
    __slots__ = ('dsn',)
    def __init__(self):
        self.dsn = 'postgres://tiramisu:tiramisu@localhost:5432/tiramisu'
        # FIXME
        self.dsn = 'postgres:///tiramisu?host=/var/run/postgresql/&user=tiramisu'

    def __setattr__(self, key, value):
        if hasattr(self, key) and getattr(self, key) == value:
            return
        if POOL is not None:  # pragma: no cover
            raise Exception(_('cannot change setting when connexion is already '
                              'opened'))
        super().__setattr__(key, value)


POOL = None
PERSISTENT = True
SETTING = Setting()


class Connection:
    async def __aenter__(self):
        self.connection = await POOL.acquire()
        self.transaction = self.connection.transaction()
        await self.transaction.__aenter__()
        return self

    async def __aexit__(self,
                        type,
                        value,
                        traceback):
        await self.transaction.__aexit__(type,
                                         value,
                                         traceback)
        await self.connection.close()

    async def fetch(self,
                       *args):
        return await self.connection.fetch(*args)

    async def fetchrow(self,
                       *args):
        return await self.connection.fetchrow(*args)

    async def fetchval(self,
                       *args):
        return await self.connection.fetchval(*args)

    async def execute(self,
                      *args):
        await self.connection.execute(*args)


async def list_sessions():
    async with Connection() as connection:
        return await _list_sessions(connection)


async def _list_sessions(connection):
    return [row[0] for row in await connection.fetch("SELECT session FROM session")]


async def delete_session(session_id):
    async with Connection() as connection:
        database_id = await connection.fetchval("SELECT session_id FROM session WHERE session = $1", session_id)
        if database_id is not None:
            await _delete_session(database_id,
                                  connection)


async def _delete_session(database_id,
                          connection):
    await connection.execute('DELETE FROM property WHERE session_id = $1', database_id)
    await connection.execute('DELETE FROM permissive WHERE session_id = $1', database_id)
    await connection.execute('DELETE FROM value WHERE session_id = $1', database_id)
    await connection.execute('DELETE FROM information WHERE session_id = $1', database_id)
    await connection.execute('DELETE FROM session WHERE session_id = $1', database_id)


async def init():
    # self.pool = await connect(dsn=SETTING.dsn)
    global POOL
    if POOL is None:
        POOL = await create_pool(dsn=SETTING.dsn)
        #print('    async with POOL.acquire() as connection:')
        #print('        async with connection.transaction():')
        sql = """
CREATE TABLE IF NOT EXISTS session(session_id SERIAL, session TEXT UNIQUE, PRIMARY KEY(session_id));
CREATE TABLE IF NOT EXISTS property(path TEXT, idx INTEGER, properties BYTEA, session_id INTEGER, PRIMARY KEY(path, idx, session_id), FOREIGN KEY(session_id) REFERENCES session(session_id));
CREATE TABLE IF NOT EXISTS permissive(path TEXT, idx INTEGER, permissives BYTEA, session_id INTEGER, PRIMARY KEY(path, idx, session_id), FOREIGN KEY(session_id) REFERENCES session(session_id));
CREATE TABLE IF NOT EXISTS value(path TEXT, value BYTEA, owner TEXT, idx INTEGER, session_id INTEGER, PRIMARY KEY (path, idx, session_id), FOREIGN KEY(session_id) REFERENCES session(session_id));
CREATE TABLE IF NOT EXISTS information(key TEXT, value BYTEA, session_id INTEGER, path TEXT, PRIMARY KEY (key, session_id), FOREIGN KEY(session_id) REFERENCES session(session_id));"""
        #print('            await connection.execute("""'+sql+'""")')
        await POOL.execute(sql)


@asyncinit
class Storage:
    __slots__ = ('pool',
                 'database_id',
                 'session_id',
                 'created')
    storage = 'postgres'

    async def __init__(self,
                       connection: Connection,
                       session_id: str,
                       delete_old_session: bool) -> None:
        if not isinstance(session_id, str):
            raise ValueError(_('session_id has to be a string'))
        self.database_id = None
        self.session_id = session_id
        select = await connection.fetchval("SELECT session_id FROM session WHERE session = $1",
                                           self.session_id)
        if select is not None:
            if delete_old_session:
                await self.delete_session()
            else:
                self.database_id = select
        if self.database_id is None:
            self.database_id = await connection.fetchval('INSERT INTO session(session) VALUES ($1) RETURNING session_id',
                                                         self.session_id)

    def convert_index(self, index):
        if index is None:
            index = -1
        return index

    def convert_path(self, path):
        if path is None:
            path = '_none'
        return path

    def load_index(self, index):
        if index == -1:
            index = None
        return index

    def load_path(self, path):
        if path == '_none':
            path = None
        return path

    async def delete_session(self):
        if self.database_id is not None:
            await _delete_session(self.database_id,
                                  POOL)
        self.database_id = None

    async def list_sessions(self,
                            connection):
        return await _list_sessions(connection)

    def getconnection(self):
        return Connection()
