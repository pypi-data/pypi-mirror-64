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

import json
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    Text = 1


@dataclass
class MessageContent:
    pass


@dataclass
class TextMessageContent(MessageContent):
    text: str


@dataclass
class Message:
    conversation_id: str
    sent_at: datetime
    sender_id: str
    type: MessageType
    content: MessageContent


class MessageJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message) or isinstance(obj, MessageContent):
            return obj.__dict__

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, MessageType):
            return obj.name

        return json.JSONEncoder.default(self, obj)
