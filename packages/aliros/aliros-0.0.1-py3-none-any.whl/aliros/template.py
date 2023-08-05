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

import yaml
import re


class UrlReader:
    supported_schemes = ['file']

    @staticmethod
    def parse_url(url):
        m = re.match(r'^(?P<scheme>[a-z][a-z0-9+\-.]*):(?P<path>.+)', url)

        if m and m.group('scheme') not in UrlReader.supported_schemes:
            raise Exception('URL scheme "%s" not supported.' % m.group('scheme'))

        if not m:
            scheme = 'file'
            path = url
        else:
            scheme = m.group('scheme')
            path = m.group('path')

        return scheme, path

    @staticmethod
    def open(url):
        scheme, path = UrlReader.parse_url(url)

        method = getattr(UrlReader, 'open_%s' % scheme)

        return method(path)

    @staticmethod
    def open_file(path):
        return open(path, 'r')


class Template:
    def __init__(self):
        self.content = {}

    def load(self, url):
        stream = UrlReader.open(url)
        self.content = self.parse_content(''.join(stream.readlines()))


class Template_YAML(Template):

    @staticmethod
    def constructor_Ref(loader, node):
        value = loader.construct_scalar(node)
        return {'Ref': value}

    @staticmethod
    def constructor_GetAtt(loader, node):
        value = loader.construct_scalar(node).split('.')
        return {'Fn::GetAtt': [value[0], value[1]]}

    @staticmethod
    def constructor_Select(loader, node):
        value = loader.construct_sequence(node)
        return {'Fn::Select': value}

    @staticmethod
    def constructor_Join(loader, node):
        value = loader.construct_sequence(node)
        return {'Fn::Join': value}

    @staticmethod
    def add_constructors(loader):
        yaml.add_constructor(u'!Ref', Template_YAML.constructor_Ref, loader)
        yaml.add_constructor(u'!GetAtt', Template_YAML.constructor_GetAtt, loader)
        yaml.add_constructor(u'!Select', Template_YAML.constructor_Select, loader)
        yaml.add_constructor(u'!Join', Template_YAML.constructor_Join, loader)

    def parse_content(self, content):
        return yaml.safe_load(content)


Template_YAML.add_constructors(yaml.SafeLoader)
