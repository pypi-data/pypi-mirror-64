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

from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime
from .message import Message, MessageType, TextMessageContent


class WeChatBackup(ABC):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def convert_raw_message(self, row: dict):
        return Message(
            conversation_id=row['conversation_id'],
            sent_at=datetime.fromtimestamp(row['sent_at']),
            sender_id=row['is_send'] == 1 and self.user_id or row['conversation_id'],
            type=MessageType(row['type']),
            content=TextMessageContent(text=row['content'])
        )

    @abstractmethod
    def get_messages(self, conversation_id: str = None) -> Iterable[dict]:
        pass
