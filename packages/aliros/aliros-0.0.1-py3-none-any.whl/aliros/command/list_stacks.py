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
from aliyunsdkros.request.v20150901.DescribeStacksRequest import DescribeStacksRequest


def add_command_arguments(parser):
    parser.add_argument('--stack-id', metavar='string', required=False)
    parser.add_argument('--name', metavar='string', required=False)
    parser.add_argument('--status', metavar='string', required=False)
    parser.add_argument('--page-number', metavar='int', required=False, default=1)
    parser.add_argument('--page-size', metavar='int', required=False, default=10)


def execute(args, client):
    request = DescribeStacksRequest()
    args.stack_id and request.set_StackId(args.stack_id)
    args.name and request.set_Name(args.name)
    args.status and request.set_Status(args.status)
    request.set_PageNumber(args.page_number)
    request.set_PageSize(args.page_size)

    status, headers, body = client.get_response(request)

    if 200 <= status < 300:
        print(json.loads(body))
        return 0
    else:
        raise Exception('Unexpected errors: status=%d, error=%s' % (status, body))
