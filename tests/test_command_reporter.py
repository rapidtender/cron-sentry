import mock
from raven_cron.runner import CommandReporter


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
