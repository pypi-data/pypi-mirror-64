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

import sys
import os
import importlib
import argparse
import configparser
from aliyunsdkcore import client


def print_help():
    usage = '''usage: aliros <command> [parameters]
To see help text, you can run:

  aliros <command> --help
aliros: error: the following arguments are required: command\n'''
    sys.stderr.write(usage)


def main():
    if len(sys.argv) < 2 or sys.argv[1][0] == '-':
        print_help()
        return -1

    parser = argparse.ArgumentParser()

    parser.add_argument('command')

    # add common arguments
    group = parser.add_argument_group('common')

    group.add_argument('--region', metavar='string', help='region to use, overrides config/env settings', required=False, default=os.getenv('ALICLOUD_REGION'))
    group.add_argument('--profile', metavar='string', help='specific profile from your credential file', required=False, default=os.getenv('ALICLOUD_PROFILE') or 'default')

    try:
        command = importlib.import_module('aliros.command.%s' % sys.argv[1].replace('-', '_'))
    except ImportError:
        sys.stderr.write('command "%s" not found.\n' % sys.argv[1])
        return -1

    command.add_command_arguments(parser)
    args = parser.parse_args()

    region = args.region
    profile = args.profile

    config = configparser.ConfigParser()
    if region is None:
        config.read(os.getenv('HOME') + '/.aliros/config')
        region = config.get(profile, 'region')

    config.read(os.getenv('HOME') + '/.aliros/credentials')
    access_key_id = config.get(profile, 'alicloud_access_key_id')
    secret_access_key = config.get(profile, 'alicloud_secret_access_key')

    return command.execute(args=args, client=client.AcsClient(access_key_id, secret_access_key, region))


if __name__ == '__main__':
    main()
