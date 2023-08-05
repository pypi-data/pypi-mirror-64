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
from aliros.template import Template_YAML
from aliros.stack import send_request
from aliyunsdkros.request.v20150901.CreateStacksRequest import CreateStacksRequest


def add_command_arguments(parser):
    parser.add_argument('--stack-name', metavar='string', required=True, help='name of stack')
    parser.add_argument('--template-url', metavar='string', required=True, help='url of template file')
    parser.add_argument('--timeout-mins', metavar='int', required=False, default=60, help='minutes to be timeout')
    parser.add_argument('--disable-rollback', required=False, default=False, action='store_true',
                        help='disable rollback if failed')
    parser.add_argument('--parameters-url', metavar='string', required=False, help='url of file with parameters')


def execute(args, client):
    template = Template_YAML()
    template.load(args.template_url)

    body = {
        'Name': args.stack_name,
        'Template': json.dumps(template.content),
        'TimeoutMins': args.timeout_mins,
        'DisableRollback': args.disable_rollback
    }

    if args.parameters_url is not None:
        parameters = Template_YAML()
        parameters.load(args.parameters_url)
        body['Parameters'] = parameters.content

    request = CreateStacksRequest()
    request.set_content(json.dumps(body))
    request.set_content_type('application/json')

    send_request(client, request)
