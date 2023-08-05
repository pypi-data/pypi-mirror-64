=======
History
=======

0.4.8 (2020-03-20)
-------------------

* Fix #96 passive host check results seem to processed as service check results
* Update requirements.


0.4.7 (2019-10-26)
-------------------

* Security update: Bump pyyaml from 3.12 to 5.1
* Update requirements.
* No tests for python 3.4


0.4.6 (2018-11-30)
-------------------

* Better logging for invalid perf data.
* Update dev requirements.


0.4.5 (2018-11-16)
-------------------

* Pypi metadata fix


0.4.3 (2018-11-16)
-------------------

* Real Fix bug in logging.warning: wrong placeholder.


0.4.2 (2018-11-12)
-------------------

* Fix bug in logging.warning.
* Update Python package metadata.


0.4.1 (2018-11-03)
-------------------

* Have (result) data for urllib `urlencode` utf-8 encoded before (PY2) and
  after (PY3).
* Warn when performance data not validates (and gets removed).


0.4.0 (2018-11-03)
-------------------

* Legitimately, truly and undoubtedly fixed issue #94 (we assume™, for now).
* Unicode all the way (like we never unicode before).
* No hopes on Python < 2.7 compatibility


0.3.11 (2018-10-12)
-------------------

* Fix issue #94 Performance data 'sanitized' NSCAweb won't hang.


0.3.10 (2018-07-17)
-------------------

* Fix RHEL 6 RPM build (make initrddir).


0.3.10 (2018-07-17)
-------------------

* Fix RHEL 6 RPM build (make initrddir).


0.3.9 (2018-07-14)
------------------

* Added systemd service file for Fedora >=18 Centos >=7

0.3.8 (2018-02-09)
------------------

* Fix: issue #83

0.3.7 (2017-11-17)
------------------

* Fix: quotes in commands.txt and commands.txt seem to get ignored #82


0.3.6 (2017-11-17)
------------------

* dev requirements updates


0.3.5 (2016-12-09)
------------------

* dev requirements updates
* docs usage


0.3.4 (2016-11-18)
------------------

* dev requirements updates


0.3.3 (2016-11-11)
------------------

* dev requirements updates
* docs: download from `GitHub`


0.3.2 (2016-10-14)
------------------

* dev requirements updates


0.3.1 (2016-09-30)
------------------

* dev requirements updates


0.3.0 (2016-09-09)
------------------

* Added `--no-daemon` option for starting pcrunner's run loop in foreground.
* dev requirements updates


0.2.10 (2016-08-26)
-------------------

* tox.ini updated
* removed specific version for package requirements from setup.py.
* readthedocs theme for local docs build.
* OS-X and vim files in .gitignore
* Update requirements: pytest -> 3.0.1


0.2.8 (2016-08-20)
------------------

* Updated docs

0.2.7 (2016-08-20)
------------------

* Updated project links.


0.2.6 (2016-08-20)
------------------

* Fixed ISSUE#4: commands file with extra white lines.


0.2.5 (2016-08-20)
------------------

* Updated Python installation documentation with new versions.


0.2.4 (2016-08-13)
------------------

* xrange -> range for python3 compatibility.


0.2.3 (2016-08-13)
------------------

* Travis/tox fix


0.2.2 (2016-08-13)
------------------

*  ISC License


0.2.1 (2016-08-13)
------------------

* Documentation RPM build updated.


0.2.0 (2016-08-12)
------------------

* First release on PyPI.
