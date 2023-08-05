# tests/test_pcrunner.py
# vim: ai et ts=4 sw=4 sts=4 ft=python fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

import pytest

from pcrunner.main import Check
from pcrunner.main import parse_pcrunner_args


@pytest.fixture()
def service_check():
    return Check(
        'PROCESS_SERVICE_CHECK_RESULT',
        'dummy check',
        '/usr/local/bin/check_dummy 0 -s 3',
        'localhost',
    )


@pytest.fixture()
def host_check():
    return Check(
        'PROCESS_HOST_CHECK_RESULT',
        'dummy check',
        '/usr/local/bin/check_dummy 0 -s 3',
        'localhost',
    )


def test_Check_attributes(service_check):
    assert service_check.result_type == 'PROCESS_SERVICE_CHECK_RESULT'
    assert service_check.name == 'dummy check'
    assert service_check.command == '/usr/local/bin/check_dummy 0 -s 3'
    assert service_check.hostname == 'localhost'
    assert service_check.pid is None
    assert service_check.process is None
    assert service_check.status_code == 3
    assert service_check.terminated is False
    assert service_check.stdout == ''
    assert service_check.stderr == ''
    assert service_check.performance_data == ''
    assert service_check.starttime == 0
    assert service_check.endtime == 0


def test_Service_Check_str_repr(service_check):
    assert '{0}'.format(service_check) == \
        '[0] PROCESS_SERVICE_CHECK_RESULT;localhost;dummy check;3;'


def test_Host_Check_str_repr(host_check):
    assert '{0}'.format(host_check) == \
        '[0] PROCESS_HOST_CHECK_RESULT;localhost;3;'


def test_parse_pcrunners_args_short():
    '''
    Test the short command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args(
        [
            '-c', '/etc/config.yml',
            '-n', 'http://nagios.example.com:5668/queue',
            '-u', 'john',
            '-p', 'secret03',
            '-o', '/etc/commandfile.yml',
            '-H', 'server.example.com',
            '-i', '300',
            '-m', '4',
            '-e', '500',
            '-r', '/var/spool/pcrunner.res',
            '-d', '/var/spool/pcrunner/resultstuf',
            '-f', '/var/run/pidfile.pid',
            '-t', '5',
            '-s', '442',
            '-l', '/var/log/logfile.log',
            '-v',
            'stop',
        ]
    )
    assert vars(args) == {
        'config_file': '/etc/config.yml',
        'nsca_web_url': 'http://nagios.example.com:5668/queue',
        'nsca_web_username': 'john',
        'nsca_web_password': 'secret03',
        'command_file': '/etc/commandfile.yml',
        'hostname': 'server.example.com',
        'interval': 300,
        'max_procs': 4,
        'lines_per_post': 500,
        'result_file': '/var/spool/pcrunner.res',
        'result_dir': '/var/spool/pcrunner/resultstuf',
        'pid_file': '/var/run/pidfile.pid',
        'http_timeout': 5,
        'max_line_size': 442,
        'log_file': '/var/log/logfile.log',
        'verbose': True,
        'runloop': 'stop',
        'no_daemon': False,
        'version': False,
    }


def test_parse_pcrunners_args_long():
    '''
    Test the long command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args(
        [
            '--config-file', '/etc/config.yml',
            '--nsca_web_url', 'http://nagios.example.com:5668/queue',
            '--nsca-web-username', 'john',
            '--nsca-web-password', 'secret03',
            '--command-file', '/etc/commandfile.yml',
            '--hostname', 'server.example.com',
            '--interval', '300',
            '--max-procs', '4',
            '--lines-per-post', '500',
            '--result-file', '/var/spool/pcrunner.res',
            '--result-dir', '/var/spool/pcrunner/resultstuf',
            '--pid-file', '/var/run/pidfile.pid',
            '--http-timeout', '5',
            '--max-line-size', '442',
            '--log-file', '/var/log/logfile.log',
            '--verbose',
            'start',
        ]
    )
    assert vars(args) == {
        'config_file': '/etc/config.yml',
        'nsca_web_url': 'http://nagios.example.com:5668/queue',
        'nsca_web_username': 'john',
        'nsca_web_password': 'secret03',
        'command_file': '/etc/commandfile.yml',
        'hostname': 'server.example.com',
        'interval': 300,
        'max_procs': 4,
        'lines_per_post': 500,
        'result_file': '/var/spool/pcrunner.res',
        'result_dir': '/var/spool/pcrunner/resultstuf',
        'pid_file': '/var/run/pidfile.pid',
        'http_timeout': 5,
        'max_line_size': 442,
        'log_file': '/var/log/logfile.log',
        'verbose': True,
        'runloop': 'start',
        'no_daemon': False,
        'version': False,
    }


def test_parse_pcrunners_args_no_daemon():
    '''
    Test the long command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args(
        [
            '--config-file', '/etc/config.yml',
            '--nsca_web_url', 'http://nagios.example.com:5668/queue',
            '--nsca-web-username', 'john',
            '--nsca-web-password', 'secret03',
            '--command-file', '/etc/commandfile.yml',
            '--hostname', 'server.example.com',
            '--interval', '300',
            '--max-procs', '4',
            '--lines-per-post', '500',
            '--result-file', '/var/spool/pcrunner.res',
            '--result-dir', '/var/spool/pcrunner/resultstuf',
            '--pid-file', '/var/run/pidfile.pid',
            '--http-timeout', '5',
            '--max-line-size', '442',
            '--log-file', '/var/log/logfile.log',
            '--verbose',
            '--no-daemon',
        ]
    )
    assert vars(args) == {
        'config_file': '/etc/config.yml',
        'nsca_web_url': 'http://nagios.example.com:5668/queue',
        'nsca_web_username': 'john',
        'nsca_web_password': 'secret03',
        'command_file': '/etc/commandfile.yml',
        'hostname': 'server.example.com',
        'interval': 300,
        'max_procs': 4,
        'lines_per_post': 500,
        'result_file': '/var/spool/pcrunner.res',
        'result_dir': '/var/spool/pcrunner/resultstuf',
        'pid_file': '/var/run/pidfile.pid',
        'http_timeout': 5,
        'max_line_size': 442,
        'log_file': '/var/log/logfile.log',
        'verbose': True,
        'runloop': None,
        'no_daemon': True,
        'version': False,
    }


def test_parse_pcrunners_args_empty():
    '''
    Test the long command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args([])
    assert vars(args) == {
        'command_file': None,
        'config_file': None,
        'runloop': None,
        'hostname': None,
        'http_timeout': None,
        'interval': None,
        'lines_per_post': None,
        'log_file': None,
        'max_line_size': None,
        'max_procs': None,
        'nsca_web_password': None,
        'nsca_web_url': None,
        'nsca_web_username': None,
        'pid_file': None,
        'result_dir': None,
        'result_file': None,
        'verbose': False,
        'version': False,
        'no_daemon': False,
    }
