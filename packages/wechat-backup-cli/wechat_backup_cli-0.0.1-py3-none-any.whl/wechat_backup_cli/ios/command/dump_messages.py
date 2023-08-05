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
from wechat_backup.ios.backup import WeChatBackup_iOS
from wechat_backup.message import MessageJSONEncoder


def add_command_arguments(parser):
    parser.add_argument('--document-dir', metavar='string', required=True, help='Documents path of WeChat backup')
    parser.add_argument('--conversation-id', metavar='string', required=True, help='ID of conversation')
    parser.add_argument('--user-id', metavar='string', required=True, help='ID of your account')


def execute(args):
    backup = WeChatBackup_iOS(user_id=args.user_id, doc_dir=args.document_dir)

    messages = backup.get_messages(conversation_id=args.conversation_id)

    print(json.dumps(messages, cls=MessageJSONEncoder, indent=4, ensure_ascii=False))
