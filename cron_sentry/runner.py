import sys
from os import getenv, SEEK_END
from raven import Client
from raven.transport import HTTPTransport
from subprocess import call
from tempfile import TemporaryFile
from argparse import ArgumentParser, REMAINDER
from sys import argv
from time import time
from .version import VERSION
import logging


# 4096 is more than Sentry will accept by default. SENTRY_MAX_EXTRA_VARIABLE_SIZE in the Sentry configuration 
# also needs to be increased to allow longer strings.
DEFAULT_STRING_MAX_LENGTH = 4096


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
# basic logging for the whole application....
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


parser = ArgumentParser(
    description='Wraps commands and reports those that fail to Sentry.',
    epilog=('The Sentry server address can also be specified through ' +
            'the SENTRY_DSN environment variable ' +
            '(and the --dsn option can be omitted).'),
    usage='cron-sentry [-h] [--dsn SENTRY_DSN] [-M STRING_MAX_LENGTH] [--version] cmd [arg ...]',
)
parser.add_argument(
    '--dsn',
    metavar='SENTRY_DSN',
    default=getenv('SENTRY_DSN'),
    help='Sentry server address',
)

parser.add_argument(
    '-M', '--string-max-length', '--max-message-length',
    type=int,
    default=DEFAULT_STRING_MAX_LENGTH,
    help='The maximum characters of a string that should be sent to Sentry (defaults to {0})'.format(DEFAULT_STRING_MAX_LENGTH),
)
parser.add_argument(
    '--version',
    action='version',
    version=VERSION,
)
parser.add_argument(
    'cmd',
    nargs=REMAINDER,
    help='The command to run',
)


def run(args=argv[1:]):
    opts = parser.parse_args(args)

    if opts.dsn == "": # dsn has been explicitly set to an empty var
        pass
    if opts.dsn == None:
        sys.stderr.write("ERROR: DSN is missing, set SENTRY_DSN to an empty variable in your environment to run cron-sentry without remote logging\n")
        sys.exit(1)

    if opts.cmd:
        # make cron-sentry work with both approaches:
        #
        #     cron-sentry --dsn http://dsn -- command --arg1 value1
        #     cron-sentry --dsn http://dsn command --arg1 value1
        #
        # see more details at https://github.com/Yipit/cron-sentry/pull/6
        if opts.cmd[0] == '--':
            cmd = opts.cmd[1:]
        else:
            cmd = opts.cmd
        runner = CommandReporter(
            cmd=cmd,
            dsn=opts.dsn,
            string_max_length=opts.string_max_length,
        )
        sys.exit(runner.run())
    else:
        sys.stderr.write("ERROR: Missing command parameter!\n")
        parser.print_usage()
        sys.exit(1)


class CommandReporter(object):
    def __init__(self, cmd, dsn, string_max_length):
        self.dsn = dsn
        self.command = cmd
        self.string_max_length = string_max_length

    def run(self):
        start = time()

        with TemporaryFile() as stdout:
            with TemporaryFile() as stderr:
                try:
                    exit_status = call(self.command, stdout=stdout, stderr=stderr)
                except:
                    exit_status = 1

                send_failed = False
                if exit_status > 0:
                    last_lines_stdout = self._get_last_lines(stdout)
                    last_lines_stderr = self._get_last_lines(stderr)
                    elapsed = int((time() - start) * 1000)
                    send_failed = self.report_fail(exit_status, last_lines_stdout, last_lines_stderr, elapsed)

                if send_failed:
                    stderr.seek(0)
                    error = stderr.read()
                    error += "\nError running {}, but failed to send to Sentry".format(self.command)
                    sys.stderr.write(error)

                stdout.seek(0)
                sys.stdout.write(stdout.read())

                return exit_status

    def report_fail(self, exit_status, last_lines_stdout, last_lines_stderr, elapsed):
        if self.dsn == "":
            return

        message = "Command \"%s\" failed" % (self.command,)

        client = Client(transport=HTTPTransport, dsn=self.dsn, string_max_length=self.string_max_length)

        # if this fails, it will log to stderr (including the original command that failed)
        client.captureMessage(
            message,
            data={
                'logger': 'cron',
            },
            extra={
                'command': self.command,
                'exit_status': exit_status,
                'last_lines_stdout': last_lines_stdout,
                'last_lines_stderr': last_lines_stderr,
            },
            time_spent=elapsed
        )

        return client.state.did_fail()

    def _get_last_lines(self, buf):
        buf.seek(0, SEEK_END)
        file_size = buf.tell()
        if file_size < self.string_max_length:
            buf.seek(0)
            last_lines = buf.read().decode('utf-8')
        else:
            buf.seek(-(self.string_max_length - 3), SEEK_END)
            last_lines = '...' + buf.read().decode('utf-8')
        return last_lines
