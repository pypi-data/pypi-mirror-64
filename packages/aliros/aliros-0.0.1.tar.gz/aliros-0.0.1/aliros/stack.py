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


def find_stack_id(client, stack_name):
    request = DescribeStacksRequest()
    request.set_Name(stack_name)
    status, headers, body = client.get_response(request)
    response = json.loads(body)

    if response['TotalCount'] > 1:
        raise Exception('Multiple stacks found with name "%s".' % stack_name)

    if response['TotalCount'] == 0:
        raise Exception('Stack with name "%s" not found.' % stack_name)

    return response['Stacks'][0]['Id']


def send_request(client, request):
    status, headers, body = client.get_response(request)

    if 200 <= status < 300:
        print(json.loads(body))
        return 0
    else:
        raise Exception('Unexpected errors: status=%d, error=%s' % (status, body))
