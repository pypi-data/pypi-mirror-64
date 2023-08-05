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

from aliros.stack import find_stack_id, send_request
from aliyunsdkros.request.v20150901.DeleteStackRequest import DeleteStackRequest


def add_command_arguments(parser):
    parser.add_argument('--stack-name', metavar='string', required=True)


def execute(args, client):
    request = DeleteStackRequest()

    request.set_StackName(args.stack_name)
    request.set_StackId(find_stack_id(client, args.stack_name))

    send_request(client, request)
