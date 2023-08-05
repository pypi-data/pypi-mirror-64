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


from typing import Iterable
from ..utils import md5_utf8, sqlite_connect
from ..message import Message
from ..backup import WeChatBackup


class WeChatBackup_iOS(WeChatBackup):
    def __init__(self, user_id: str, doc_dir: str):
        super().__init__(user_id=user_id)

        self.doc_dir = doc_dir
        self.db = sqlite_connect('%s/%s/DB/MM.sqlite' % (doc_dir, md5_utf8(user_id)))

    def get_messages(self, conversation_id: str = None) -> Iterable[Message]:
        table_name = 'Chat_%s' % md5_utf8(conversation_id)

        sql = f'''
            SELECT
                '{conversation_id}' AS conversation_id,
                CreateTime AS sent_at,
                Message AS content,
                Type AS type,
                NOT Des AS is_send,

                TableVer, ImgStatus, MesLocalID, MesSvrID, Status
            FROM {table_name}
            WHERE Type=1
            ORDER BY CreateTime
        '''

        c = self.db.cursor()

        return [self.convert_raw_message(row) for row in c.execute(sql).fetchall()]
