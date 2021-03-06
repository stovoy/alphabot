#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2014 Nextdoor.com, Inc

import argparse
import logging
import os
import sys

from tornado import ioloop, gen
import requests

import alphabot.bot

requests.packages.urllib3.disable_warnings()

FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)
logging.captureWarnings(True)
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Alphabot')
parser.add_argument('--version', help='Show version and exit', dest='version',
                    action='store_true', default=False)
parser.add_argument('-S', '--scripts', dest='scripts', metavar='dir',
                    action='store', default=[], nargs='+',
                    help=('Direcotry to fetch bot scripts. '
                          'Can be specified multiple times'))
parser.add_argument('-e', '--engine', dest='engine', action='store',
                    default='cli', help='What chat engine to use. Slack or cli')

args = parser.parse_args()

__author__ = ('Mikhail Simin <mikhail@nextdoor.com>',)
__version__ = '0.0.1'

def start_ioloop():
    try:
        ioloop.IOLoop.instance().run_sync(start_alphabot)
    except KeyboardInterrupt:
        pass
    except alphabot.bot.AlphaBotException as e:
        log.critical('Alphabot failed. Reason: %s' % e)

@gen.coroutine
def start_alphabot():

    bot = alphabot.bot.get_instance(engine=args.engine)

    full_path_scripts = [os.path.abspath(s) for s in args.scripts]
    log.debug('full path scripts: %s' % full_path_scripts)
    yield bot.setup(memory_type='dict', script_paths=full_path_scripts)
    yield bot.start()

if __name__ == '__main__':
    if args.version:
        print(__version__)
        exit()

    start_ioloop()
