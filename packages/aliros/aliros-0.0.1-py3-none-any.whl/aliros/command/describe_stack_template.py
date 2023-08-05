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
from aliyunsdkros.request.v20150901.DescribeTemplateRequest import DescribeTemplateRequest
from aliyunsdkros.request.v20150901.DescribeStacksRequest import DescribeStacksRequest


def add_command_arguments(parser):
    parser.add_argument('--stack-name', metavar='string', required=True)


def execute(args, client):
    request = DescribeStacksRequest()
    request.set_Name(args.stack_name)
    status, headers, body = client.get_response(request)
    response = json.loads(body)

    if response['TotalCount'] != 1:
        raise Exception('Stacks with name "%s" not unique.' % args.stack_name)

    stack_id = response['Stacks'][0]['Id']

    request = DescribeTemplateRequest()

    request.set_StackName(args.stack_name)
    request.set_StackId(stack_id)

    status, headers, body = client.get_response(request)

    if 200 <= status < 300:
        print(json.loads(body))
        return 0
    else:
        raise Exception('Unexpected errors: status=%d, error=%s' % (status, body))
