# -*- coding: utf-8 -*-
""" This is the pytest configuration file """

import optparse
import pytest
from seleniumbase import config as sb_config
from seleniumbase.core import log_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants


def pytest_addoption(parser):
    parser = parser.getgroup('SeleniumBase',
                             'SeleniumBase specific configuration options')
    parser.addoption('--browser', action="store",
                     dest='browser',
                     type=str.lower,
                     choices=constants.ValidBrowsers.valid_browsers,
                     default=constants.Browser.GOOGLE_CHROME,
                     help="""Specifies the web browser to use. Default: Chrome.
                          If you want to use Firefox, explicitly indicate that.
                          Example: (--browser=firefox)""")
    parser.addoption('--with-selenium', action="store_true",
                     dest='with_selenium',
                     default=True,
                     help="Use if tests need to be run with a web browser.")
    parser.addoption('--env', action='store',
                     dest='environment',
                     type=str.lower,
                     choices=(
                         constants.Environment.QA,
                         constants.Environment.STAGING,
                         constants.Environment.DEVELOP,
                         constants.Environment.PRODUCTION,
                         constants.Environment.MASTER,
                         constants.Environment.LOCAL,
                         constants.Environment.TEST
                     ),
                     default=constants.Environment.TEST,
                     help="The environment to run the tests in.")
    parser.addoption('--data', dest='data',
                     default=None,
                     help='Extra data to pass from the command line.')
    parser.addoption('--cap_file', dest='cap_file',
                     default=None,
                     help="""The file that stores browser desired capabilities
                          for BrowserStack or Sauce Labs web drivers.""")
    parser.addoption('--with-testing_base', action="store_true",
                     dest='with_testing_base',
                     default=True,
                     help="""Use to save logs and screenshots when tests fail.
                          The following options are now active by default
                          with --with-testing_base (which is on by default):
                          --with-screen_shots ,
                          --with-basic_test_info ,
                          --with-page_source
                          """)
    parser.addoption('--log_path', dest='log_path',
                     default='latest_logs/',
                     help='Where the log files are saved.')
    parser.addoption('--archive_logs', action="store_true",
                     dest='archive_logs',
                     default=False,
                     help="Archive old log files instead of deleting them.")
    parser.addoption('--with-db_reporting', action="store_true",
                     dest='with_db_reporting',
                     default=False,
                     help="Use to record test data in the MySQL database.")
    parser.addoption('--database_env', action='store',
                     dest='database_env',
                     choices=(
                         'production', 'qa', 'staging', 'develop',
                         'test', 'local', 'master'
                     ),
                     default='test',
                     help=optparse.SUPPRESS_HELP)
    parser.addoption('--with-s3_logging', action="store_true",
                     dest='with_s3_logging',
                     default=False,
                     help="Use to save test log files in Amazon S3.")
    parser.addoption('--with-screen_shots', action="store_true",
                     dest='with_screen_shots',
                     default=False,
                     help="""Use to save screenshots on test failure.
                          (Automatically on when using --with-testing_base)""")
    parser.addoption('--with-basic_test_info', action="store_true",
                     dest='with_basic_test_info',
                     default=False,
                     help="""Use to save basic test info on test failure.
                          (Automatically on when using --with-testing_base)""")
    parser.addoption('--with-page_source', action="store_true",
                     dest='with_page_source',
                     default=False,
                     help="""Use to save page source on test failure.
                          (Automatically on when using --with-testing_base)""")
    parser.addoption('--server', action='store',
                     dest='servername',
                     default='localhost',
                     help="""Designates the Selenium Grid server to use.
                          Default: localhost.""")
    parser.addoption('--port', action='store',
                     dest='port',
                     default='4444',
                     help="""Designates the Selenium Grid port to use.
                          Default: 4444.""")
    parser.addoption('--proxy', action='store',
                     dest='proxy_string',
                     default=None,
                     help="""Designates the proxy server:port to use.
                          Format: servername:port.  OR
                                  username:password@servername:port  OR
                                  A dict key from proxy_list.PROXY_LIST
                          Default: None.""")
    parser.addoption('--agent', action='store',
                     dest='user_agent',
                     default=None,
                     help="""Designates the User-Agent for the browser to use.
                          Format: A string.
                          Default: None.""")
    parser.addoption('--headless', action="store_true",
                     dest='headless',
                     default=False,
                     help="""Using this makes Webdriver run headlessly,
                          which is required on headless machines.""")
    parser.addoption('--is_pytest', action="store_true",
                     dest='is_pytest',
                     default=True,
                     help="""This is used by the BaseCase class to tell apart
                          pytest runs from nosetest runs. (Automatic)""")
    parser.addoption('--demo_mode', action="store_true",
                     dest='demo_mode',
                     default=False,
                     help="""Using this slows down the automation so that
                          you can see what it's actually doing.""")
    parser.addoption('--demo_sleep', action='store', dest='demo_sleep',
                     default=None,
                     help="""Setting this overrides the Demo Mode sleep
                          time that happens after browser actions.""")
    parser.addoption('--highlights', action='store', dest='highlights',
                     default=None,
                     help="""Setting this overrides the default number of
                          highlight animation loops to have per call.""")
    parser.addoption('--message_duration', action="store",
                     dest='message_duration',
                     default=None,
                     help="""Setting this overrides the default time that
                          messenger notifications remain visible when reaching
                          assert statements during Demo Mode.""")
    parser.addoption('--check_js', action="store_true",
                     dest='js_checking_on',
                     default=False,
                     help="""The option to check for JavaScript errors after
                          every page load.""")
    parser.addoption('--ad_block', action="store_true",
                     dest='ad_block_on',
                     default=False,
                     help="""Using this makes WebDriver block display ads
                          that are defined in ad_block_list.AD_BLOCK_LIST.""")
    parser.addoption('--verify_delay', action='store', dest='verify_delay',
                     default=None,
                     help="""Setting this overrides the default wait time
                          before each MasterQA verification pop-up.""")
    parser.addoption('--disable_csp', action="store_true",
                     dest='disable_csp',
                     default=False,
                     help="""Using this disables the Content Security Policy of
                          websites, which may interfere with some features of
                          SeleniumBase, such as loading custom JavaScript
                          libraries for various testing actions.
                          Setting this to True (--disable_csp) overrides the
                          value set in seleniumbase/config/settings.py""")
    parser.addoption('--save_screenshot', action='store_true',
                     dest='save_screenshot',
                     default=False,
                     help="""Take a screenshot on last page after the last step
                          of the test. (Added to the "latest_logs" folder.)""")
    parser.addoption('--visual_baseline', action='store_true',
                     dest='visual_baseline',
                     default=False,
                     help="""Setting this resets the visual baseline for
                          Automated Visual Testing with SeleniumBase.
                          When a test calls self.check_window(), it will
                          rebuild its files in the visual_baseline folder.""")
    parser.addoption('--timeout_multiplier', action='store',
                     dest='timeout_multiplier',
                     default=None,
                     help="""Setting this overrides the default timeout
                          by the multiplier when waiting for page elements.
                          Unused when tests overide the default value.""")


def pytest_configure(config):
    """ This runs after command line options have been parsed """
    sb_config.is_pytest = True
    sb_config.browser = config.getoption('browser')
    sb_config.data = config.getoption('data')
    sb_config.environment = config.getoption('environment')
    sb_config.with_selenium = config.getoption('with_selenium')
    sb_config.user_agent = config.getoption('user_agent')
    sb_config.headless = config.getoption('headless')
    sb_config.with_testing_base = config.getoption('with_testing_base')
    sb_config.with_db_reporting = config.getoption('with_db_reporting')
    sb_config.with_s3_logging = config.getoption('with_s3_logging')
    sb_config.with_screen_shots = config.getoption('with_screen_shots')
    sb_config.with_basic_test_info = config.getoption('with_basic_test_info')
    sb_config.with_page_source = config.getoption('with_page_source')
    sb_config.servername = config.getoption('servername')
    sb_config.port = config.getoption('port')
    sb_config.proxy_string = config.getoption('proxy_string')
    sb_config.cap_file = config.getoption('cap_file')
    sb_config.database_env = config.getoption('database_env')
    sb_config.log_path = config.getoption('log_path')
    sb_config.archive_logs = config.getoption('archive_logs')
    sb_config.demo_mode = config.getoption('demo_mode')
    sb_config.demo_sleep = config.getoption('demo_sleep')
    sb_config.highlights = config.getoption('highlights')
    sb_config.message_duration = config.getoption('message_duration')
    sb_config.js_checking_on = config.getoption('js_checking_on')
    sb_config.ad_block_on = config.getoption('ad_block_on')
    sb_config.verify_delay = config.getoption('verify_delay')
    sb_config.disable_csp = config.getoption('disable_csp')
    sb_config.save_screenshot = config.getoption('save_screenshot')
    sb_config.visual_baseline = config.getoption('visual_baseline')
    sb_config.timeout_multiplier = config.getoption('timeout_multiplier')
    sb_config.pytest_html_report = config.getoption("htmlpath")  # --html=FILE

    if sb_config.with_testing_base:
        log_helper.log_folder_setup(sb_config.log_path, sb_config.archive_logs)
    proxy_helper.remove_proxy_zip_if_present()


def pytest_unconfigure():
    """ This runs after all tests have completed with pytest. """
    proxy_helper.remove_proxy_zip_if_present()


def pytest_runtest_setup():
    """ This runs before every test with pytest """
    pass


def pytest_runtest_teardown(item):
    """ This runs after every test with pytest """

    # Make sure webdriver has exited properly and any headless display
    try:
        self = item._testcase
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except Exception:
            pass
        try:
            if hasattr(self, 'headless') and self.headless:
                if self.headless_active:
                    if hasattr(self, 'display') and self.display:
                        self.display.stop()
        except Exception:
            pass
    except Exception:
        pass


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    if pytest_html and report.when == 'call':
        try:
            extra_report = item._testcase._html_report_extra
            extra = getattr(report, 'extra', [])
            if extra_report[1]["content"]:
                report.extra = extra + extra_report
        except Exception:
            pass
