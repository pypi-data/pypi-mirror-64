# -*- coding: utf-8 -*-
" with sqlite3 engine"
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
import sqlite3
import warnings
from os.path import join
from typing import Optional, Dict

from ...i18n import _
from ...error import ConflictError
from ...asyncinit import asyncinit


global CONN
CONN = None


async def init():
    global CONN
    if CONN is None:
        CONN = sqlite3.connect(_gen_filename())
        CONN.text_factory = str
        session_table = 'CREATE TABLE IF NOT EXISTS session(session_id INTEGER, session TEXT UNIQUE, PRIMARY KEY(session_id))'
        settings_table = 'CREATE TABLE IF NOT EXISTS property(path TEXT, tiram_index INTEGER, properties TEXT, session_id INTEGER, PRIMARY KEY(path, tiram_index, session_id), ' \
                         'FOREIGN KEY(session_id) REFERENCES session(session_id))'
        permissives_table = 'CREATE TABLE IF NOT EXISTS permissive(path TEXT, tiram_index INTEGER, permissives TEXT, session_id INTEGER, ' \
                            'PRIMARY KEY(path, tiram_index, session_id), ' \
                            'FOREIGN KEY(session_id) REFERENCES session(session_id))'
        values_table = 'CREATE TABLE IF NOT EXISTS value(path TEXT, value TEXT, owner TEXT, idx INTEGER, session_id INTEGER, ' \
                       'PRIMARY KEY (path, idx, session_id), ' \
                       'FOREIGN KEY(session_id) REFERENCES session(session_id))'
        informations_table = 'CREATE TABLE IF NOT EXISTS information(key TEXT, value TEXT, session_id INTEGER, path TEXT, ' \
                             'PRIMARY KEY (key, session_id), ' \
                             'FOREIGN KEY(session_id) REFERENCES session(session_id))'
        cursor = CONN.cursor()
        cursor.execute(session_table)
        cursor.execute(values_table)
        cursor.execute(informations_table)
        cursor.execute(settings_table)
        cursor.execute(permissives_table)
        CONN.commit()


class Connection:
    async def __aenter__(self):
        self.connection = CONN.cursor()
        return self

    async def __aexit__(self,
                        type,
                        value,
                        traceback):
        if type is None:
            CONN.commit()
        else:
            CONN.rollback()
        self.connection.close()

    async def execute(self,
                      sql: str,
                      params: Optional[Dict]=None) -> None:
        if params is None:
            params = tuple()
        self.connection.execute(sql, params)

    async def select(self,
                     sql: str,
                     params: Optional[Dict]=None,
                     only_one: bool=True) -> 'Row':
        if params is None:
            params = tuple()
        self.connection.execute(sql, params)
        if only_one:
            return self.connection.fetchone()
        else:
            return self.connection.fetchall()


class Setting:
    """:param extension: database file extension (by default: db)
    :param dir_database: root database directory (by default: /tmp)
    """
    __slots__ = ('extension',
                 'dir_database',
                 'name')

    def __init__(self):
        self.extension = 'db'
        self.dir_database = '/tmp'
        self.name = 'tiramisu'

    def __setattr__(self, key, value):
        if CONN is not None:  # pragma: no cover
            raise Exception(_('cannot change setting when connexion is already '
                              'opened'))
        super().__setattr__(key, value)


PERSISTENT = True
SETTING = Setting()


def _gen_filename():
    return join(SETTING.dir_database, '{0}.{1}'.format(SETTING.name, SETTING.extension))


async def list_sessions():
    if not CONN:
        warnings.warn_explicit(Warning(_('Cannot list sessions, please connect to database first')),
                               category=Warning,
                               filename=__file__,
                               lineno=63)
        return []
    cursor = CONN.cursor()
    return await _list_sessions(cursor)


async def _list_sessions(cursor):
    names = [row[0] for row in cursor.execute("SELECT session FROM session").fetchall()]
    return names


async def delete_session(session_id):
    cursor = CONN.cursor()
    ret = cursor.execute("SELECT session_id FROM session WHERE session = ?",
                         (session_id,)).fetchone()
    if ret is not None:
        database_id = ret[0]
        await _delete_session(database_id,
                              cursor)
    cursor.close()

async def _delete_session(database_id,
                          cursor):
    cursor.execute("DELETE FROM property WHERE session_id = ?", (database_id,))
    cursor.execute("DELETE FROM permissive WHERE session_id = ?", (database_id,))
    cursor.execute("DELETE FROM value WHERE session_id = ?", (database_id,))
    cursor.execute("DELETE FROM information WHERE session_id = ?", (database_id,))
    cursor.execute("DELETE FROM session WHERE session_id = ?", (database_id,))
    CONN.commit()


@asyncinit
class Storage:
    __slots__ = ('_conn',
                 '_cursor',
                 'session_id',
                 'session_name',
                 'created')
    storage = 'sqlite3'

    async def __init__(self,
                       connection: Connection,
                       session_id: str,
                       delete_old_session: bool) -> None:
        if not isinstance(session_id, str):
            raise ValueError(_('session_id has to be a string'))
        self.created = False
        self.session_id = None
        self.session_name = session_id
        select = await connection.select("SELECT session_id FROM session WHERE session = ?", (session_id,))
        if select is not None:
            if delete_old_session:
                self.delete_session()
            else:
                self.session_id = select[0]
        if self.session_id is None:
            await connection.execute('INSERT INTO session(session) VALUES (?)',
                                     (session_id,))
            self.session_id = connection.connection.lastrowid
        self.created = True

    async def delete_session(self):
        if self.session_id is not None:
            await _delete_session(self.session_id,
                                  CONN)
        self.session_id = None

    async def list_sessions(self):
        return await _list_sessions(self._cursor)

    def getconnection(self):
        return Connection()


def getsession():
    pass
