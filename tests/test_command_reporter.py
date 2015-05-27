import mock
import sys
from raven_cron.runner import CommandReporter, MAX_MESSAGE_SIZE


@mock.patch('raven_cron.runner.Client')
def test_command_reporter_accepts_parameters(ClientMock):
    reporter = CommandReporter(['date', '--invalid-option'], 'http://testdsn')

    reporter.run()

    client = ClientMock()
    assert client.captureMessage.called


@mock.patch('raven_cron.runner.Client')
def test_command_reporter_works_with_no_params_commands(ClientMock):
    reporter = CommandReporter(['date'], 'http://testdsn')

    reporter.run()

    client = ClientMock()
    assert not client.captureMessage.called


@mock.patch('raven_cron.runner.sys')
@mock.patch('raven_cron.runner.Client')
def test_command_reporter_keeps_stdout_and_stderr(ClientMock, sys_mock):
    command = [sys.executable, '-c', """
import sys
sys.stdout.write("test-out")
sys.stderr.write("test-err")
sys.exit(2)
"""]
    reporter = CommandReporter(command, 'http://testdsn')
    client = ClientMock()

    reporter.run()

    sys_mock.stdout.write.assert_called_with('test-out')
    sys_mock.stderr.write.assert_called_with('test-err')
    client.captureMessage.assert_called_with(
        mock.ANY,
        time_spent=mock.ANY,
        data=mock.ANY,
        extra={
            'command': command,
            'exit_status': 2,
            "last_lines_stdout": "test-out",
            "last_lines_stderr": "test-err",
    })


@mock.patch('raven_cron.runner.sys')
@mock.patch('raven_cron.runner.Client')
def test_reports_correctly_to_with_long_messages_but_trims_stdout_and_stderr(ClientMock, sys_mock):
    command = [sys.executable, '-c', """
import sys
sys.stdout.write("a" * 2000)
sys.stderr.write("b" * 2000)
sys.exit(2)
"""]
    reporter = CommandReporter(command, 'http://testdsn')
    client = ClientMock()

    reporter.run()
    expected_stdout = u'...{}'.format('a' * (MAX_MESSAGE_SIZE - 3))
    expected_stderr = u'...{}'.format('b' * (MAX_MESSAGE_SIZE - 3))

    sys_mock.stdout.write.assert_called_with(expected_stdout)
    sys_mock.stderr.write.assert_called_with(expected_stderr)
    client.captureMessage.assert_called_with(
        mock.ANY,
        time_spent=mock.ANY,
        data=mock.ANY,
        extra={
            'command': command,
            'exit_status': 2,
            "last_lines_stdout": expected_stdout,
            "last_lines_stderr": expected_stderr,
    })
