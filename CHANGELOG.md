current
=======

* Change argparse to use REMAINDER instead of '+' for `cmd`. More details at https://github.com/Yipit/cron-sentry/pull/6
* Make cron-sentry compatible with old and new way of specifying arguments in the command line
* Change usage message to have `cmd [arg ...]` rather than only `...`


0.4.1
=====

* Upload right files to PyPI


0.4.0
=====

* Renamed fork from raven-cron to cron-sentry


0.3.x
=====
* Yipit forks the project and keep it under the same name
* Add support to command options (commit 75ade6d920cbb9f0e84575ca3ed8b568f945727d)
* Preserve stdout and stderr (commit a604f3e0a104ab018fd1c9b35fe989fdd0834a4b)
* Python 3 support, added by @Ian-Foote (commit a0b74c504e748a821fd07236204c52439cc1b1e9)


0.2.0 / 2013-12-18 
==================

 * Update RELEASE.md
 * How to make a release


0.1.0 / 2013-10-22 
==================

 * Fixes .gitignore
 * Don't load the raven dependency in `__init__.py`. Fixes #1
 * Project moved
 * Add LICENSE file

