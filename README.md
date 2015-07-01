Raven-cron : error reporting for cron commands
================================================

This is a fork of https://github.com/mediacore/raven-cron. Why the fork?
-------------------------------------------

The original raven-cron doesn't preserve stdout neither stderr; it means that if a program outputs anything and exits sucessfully, original raven-cron ignores *all* output.

Another problem is that it doesn't work with commands that accept options, definitively a bug. A [pull request was sent to them](https://github.com/mediacore/raven-cron/pull/4) to support options, but they never said anything, so this fork is currently being maintained by Yipit.


This fork has the following patches:

* Add support to command options (commit 75ade6d920cbb9f0e84575ca3ed8b568f945727d).
* Preserve stdout and stderr (commit a604f3e0a104ab018fd1c9b35fe989fdd0834a4b).
* Python 3 support, added by @Ian-Foote (commit a0b74c504e748a821fd07236204c52439cc1b1e9).


----


Raven-cron is a small command-line wrapper that reports errors to
[Sentry](http://getsentry.com) if the script exits with an exit status other
than zero.

Install
-------

`pip install raven-cron`

Usage
-----

```
usage: raven-cron [-h] [--dsn SENTRY_DSN] [--version] cmd [cmd ...]

Wraps commands and reports failing ones to sentry.

positional arguments:
  cmd               The command to run

optional arguments:
  -h, --help        show this help message and exit
  --dsn SENTRY_DSN  Sentry server address
  --version         show program's version number and exit

SENTRY_DSN can also be passed as an environment variable.
```

Example
-------

`crontab -e`
```
SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
@reboot raven-cron ./my-process
```

Misc
----

Copyright 2013 to MediaCore Technologies and licensed under the MIT license.

