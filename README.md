Raven-cron : error reporting for cron commands
================================================

Raven-cron is a small command-line wrapper that reports errors to
[Sentry](http://getsentry.com) if the script exits with an exit status other
than zero.

Install
-------

(NOT YET)

`pip install raven-cron`

Usage
-----

```
usage: raven-cron [-h] [--dsn SENTRY_DSN] [--version] [cmd [cmd ...]]

Wraps commands and reports failing ones to sentry

positional arguments:
  cmd               The command to run

optional arguments:
  -h, --help        show this help message and exit
  --dsn SENTRY_DSN  Sentry server address
  --version         show program's version number and exit
```
