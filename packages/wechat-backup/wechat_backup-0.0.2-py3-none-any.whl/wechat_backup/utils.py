# -*- coding: utf-8 -*-
# Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import hashlib
import sqlite3


def md5_utf8(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))

    return m.hexdigest()


def sqlite_connect(path: str) -> sqlite3.Connection:
    def dict_factory(cursor, row) -> dict:
        d = {}
        for i, col in enumerate(cursor.description):
            d[col[0]] = row[i]
        return d

    conn = sqlite3.connect(path)
    conn.row_factory = dict_factory

    return conn
