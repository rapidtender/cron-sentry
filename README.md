Cron-Sentry: error reporting to [Sentry](https://getsentry.com/) of commands run via cron
================================================

Cron-Sentry is a python command-line wrapper that reports errors to [Sentry](http://getsentry.com) (using [raven](https://github.com/getsentry/raven-python)) if the called script exits with a status other than zero.

Note: I've made updates to try to get this to behave in a more cron friendly way. Specifically, the old versions seemed to swallow all your errors if something was wrong with Sentry. The behaviour is now:

- try to run the command
- if it fails for any reason try to log that to sentry
- if logging to senty fails write the issues to the logger on stderr (along the the outputs of the failed command)
- this allows `MAIL_TO` in cron to pick it up in the usual way

Install
-------

`pip install cron-sentry`

Usage
-----

```
$ cron-sentry --help
usage: cron-sentry [-h] [--dsn SENTRY_DSN] [-M STRING_MAX_LENGTH] [--version] cmd [arg ...]

Wraps commands and reports those that fail to Sentry.

positional arguments:
  cmd                   The command to run

optional arguments:
  -h, --help            show this help message and exit
  --dsn SENTRY_DSN      Sentry server address
  -M STRING_MAX_LENGTH, --string-max-length STRING_MAX_LENGTH, --max-message-length STRING_MAX_LENGTH
                        The maximum characters of a string that should be sent
                        to Sentry (defaults to 4096)
  --version             show program's version number and exit

The Sentry server address can also be specified through the SENTRY_DSN
environment variable (and the --dsn option can be omitted).
```

Example
-------

`crontab -e`
```
MAIL_TO="failover_for_broken_sentry@example.com"

# SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
# ^-- doesn't work for me, add dsn to /etc/cron-sentry.conf

0 4 * * * /usr/local/bin/cron-sentry my-process --arg arg2
```


License
-------

This project started life as [raven-cron](https://github.com/mediacore/raven-cron) by MediaCore Technologies.

Original copyright 2013 to MediaCore Technologies (MIT license).
Copyright 2015 to Yipit Inc. (MIT license).
