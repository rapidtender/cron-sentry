from argparse import ArgumentParser
from datetime import datetime
from os import getenv, SEEK_END
from string import join
from subprocess import call
from sys import argv
from tempfile import TemporaryFile
from time import time
from uuid import uuid4

from .version import VERSION
from raven import Client

MAX_MESSAGE_SIZE = 1000

parser = ArgumentParser(description='Wraps commands and reports failing ones to sentry')
# FIXME: Should we also use a configuration file ?
parser.add_argument(
    '--dsn',
    metavar='SENTRY_DSN',
    default=getenv('SENTRY_DSN'),
    help='Sentry server address',
)
parser.add_argument(
    '--version',
    action='version',
    version=VERSION,
)
parser.add_argument(
    'cmd',
    nargs='*',
    help='The command to run',
)

def run(args=argv[1:]):
    opts = parser.parse_args(args)
    runner = CommandReporter(**vars(opts))
    runner.run()

class CommandReporter(object):
    def __init__(self, cmd, dsn):
        if len(cmd) <= 1:
            cmd = cmd[0]

        self.dsn = dsn
        self.command = cmd
        self.raven = None

    def run(self):
        buf = TemporaryFile()
        start = time()

        exit_status = call(self.command, stdout=buf, stderr=buf, shell=True)
        
        if exit_status > 0:
            elapsed = time() - start
            self.report_fail(exit_status, buf, elapsed)

        buf.close()
        
    def report_fail(self, exit_status, buf, elapsed):
        if self.dsn is None:
            return

        # Hack to get the file size since the tempfile doesn't exist anymore
        buf.seek(0, SEEK_END)
        file_size = buf.tell()
        if file_size < MAX_MESSAGE_SIZE:
            buf.seek(0)
            last_lines = buf.readlines()
        else:
            buf.seek(-(MAX_MESSAGE_SIZE-3), SEEK_END)
            last_lines = ['...'] + buf.readlines()
        
        if self.raven is None:
            self.raven = Client(dsn=self.dsn)

        raven = self.raven
        event_id = uuid4().hex
        culprit = join(self.command)
        message = u'Failed with exit status %d' % (exit_status,)

        data = {
            'culprit': culprit,
            'event_id': event_id,
            'extra': {
                'sys.argv': argv[:],
                'exit_status': 1,
            },
            'level': 40,
            'message': message,
            'modules': {},
            'platform': 'shell',
            'logger': 'cron',
            'project': raven.project,
            'sentry.interfaces.Exception': {
                'module': u'exceptions',
                'type': 'WOOT',
                'value': u'exceptions must be old-style classes or derived from BaseException, not str'
            },
            'sentry.interfaces.Stacktrace': {
                'frames': [{
                    'context_line': u'raise "woot"',
                    'filename': 'raven_cron/runner.py',
                    'lineno': len(last_lines),
                    'pre_context': last_lines,
                    'post_context': [],
                }],
            },
            'server_name': raven.name,
            'tags': {},
            'time_spent': 0.010372161865234375,
            'timestamp': datetime.utcnow(),
        }
        raven.send(**data)
        print data.get('event_id')
