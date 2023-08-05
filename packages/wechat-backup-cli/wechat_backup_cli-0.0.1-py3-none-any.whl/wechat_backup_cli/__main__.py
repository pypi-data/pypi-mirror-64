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
import argparse
import importlib


def print_help():
    usage = '''usage: wechat-backup <platform> <command> [parameters]
To see help text, you can run:
  wechat-backup <platform> <command> --help
'''
    sys.stderr.write(usage)


def main():
    if len(sys.argv) < 3 or sys.argv[1][0] == '-':
        print_help()
        return -1

    parser = argparse.ArgumentParser()

    parser.add_argument('platform')
    parser.add_argument('command')

    command = importlib.import_module('wechat_backup_cli.%s.command.%s' % (sys.argv[1], sys.argv[2].replace('-', '_')))

    command.add_command_arguments(parser)

    args = parser.parse_args()

    return command.execute(args=args)


if __name__ == '__main__':
    sys.exit(main())
