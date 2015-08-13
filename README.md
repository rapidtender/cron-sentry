Cron-Sentry: error reporting to [Sentry](https://getsentry.com/) of commands run via cron
================================================

Cron-Sentry is a python command-line wrapper that reports errors to [Sentry](http://getsentry.com) (using [raven](https://github.com/getsentry/raven-python)) if the called script exits with a status other than zero.

Install
-------

`pip install cron-sentry`

Usage
-----

```
$ cron-sentry --help
usage: cron-sentry [-h] [--dsn SENTRY_DSN] [-M MAX_MESSAGE_LENGTH] [--version] cmd [arg ...]

Wraps commands and reports those that fail to Sentry.

positional arguments:
  cmd                   The command to run

optional arguments:
  -h, --help            show this help message and exit
  --dsn SENTRY_DSN      Sentry server address
  -M MAX_MESSAGE_LENGTH, --max-message-length MAX_MESSAGE_LENGTH
                        The maximum characters of a string that should be sent
                        to Sentry (defaults to 4094)
  --version             show program's version number and exit

The Sentry server address can also be specified through the SENTRY_DSN
environment variable (and the --dsn option can be omitted).
```

Example
-------

`crontab -e`
```
SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
0 4 * * * cron-sentry my-process --arg arg2
```


License
-------

This project started life as [raven-cron](https://github.com/mediacore/raven-cron) by MediaCore Technologies.

Original copyright 2013 to MediaCore Technologies (MIT license).
Copyright 2015 to Yipit Inc. (MIT license).
