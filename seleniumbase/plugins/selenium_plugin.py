"""
This plugin gives the power of Selenium to nosetests
by providing a WebDriver object for the tests to use.
"""

from nose.plugins import Plugin
from pyvirtualdisplay import Display
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants


class SeleniumBrowser(Plugin):
    """
    The plugin for Selenium tests. Takes in key arguments and then
    creates a WebDriver object. All arguments are passed to the tests.

    The following command line options are available to the tests:
    self.options.browser -- the browser to use (--browser)
    self.options.server -- the server used by the test (--server)
    self.options.port -- the port used by the test (--port)
    self.options.proxy -- designates the proxy server:port to use. (--proxy)
    self.options.agent -- designates the User Agent for the browser. (--agent)
    self.options.headless -- the option to run headlessly (--headless)
    self.options.demo_mode -- the option to slow down Selenium (--demo_mode)
    self.options.demo_sleep -- Selenium action delay in DemoMode (--demo_sleep)
    self.options.highlights -- # of highlight animations shown (--highlights)
    self.options.message_duration -- Messenger alert time (--message_duration)
    self.options.js_checking_on -- option to check for js errors (--check_js)
    self.options.ad_block -- the option to block some display ads (--ad_block)
    self.options.verify_delay -- delay before MasterQA checks (--verify_delay)
    self.options.disable_csp -- disable Content Security Policy (--disable_csp)
    self.options.save_screenshot -- save screen after test (--save_screenshot)
    self.options.visual_baseline -- set the visual baseline (--visual_baseline)
    self.options.timeout_multiplier -- increase defaults (--timeout_multiplier)
    """
    name = 'selenium'  # Usage: --with-selenium

    def options(self, parser, env):
        super(SeleniumBrowser, self).options(parser, env=env)

        parser.add_option(
            '--browser', action='store',
            dest='browser',
            choices=constants.ValidBrowsers.valid_browsers,
            default=constants.Browser.GOOGLE_CHROME,
            help="""Specifies the web browser to use. Default: Chrome.
                    If you want to use Firefox, explicitly indicate that.
                    Example: (--browser=firefox)""")
        parser.add_option(
            '--browser_version', action='store',
            dest='browser_version',
            default="latest",
            help="""The browser version to use. Explicitly select
                    a version number or use "latest".""")
        parser.add_option(
            '--cap_file', action='store',
            dest='cap_file',
            default=None,
            help="""The file that stores browser desired capabilities
                    for BrowserStack or Sauce Labs web drivers.""")
        parser.add_option(
            '--server', action='store', dest='servername',
            default='localhost',
            help="""Designates the Selenium Grid server to use.
                    Default: localhost.""")
        parser.add_option(
            '--port', action='store', dest='port',
            default='4444',
            help="""Designates the Selenium Grid port to use.
                    Default: 4444.""")
        parser.add_option(
            '--proxy', action='store',
            dest='proxy_string',
            default=None,
            help="""Designates the proxy server:port to use.
                    Format: servername:port.  OR
                            username:password@servername:port  OR
                            A dict key from proxy_list.PROXY_LIST
                    Default: None.""")
        parser.add_option(
            '--agent', action='store',
            dest='user_agent',
            default=None,
            help="""Designates the User-Agent for the browser to use.
                    Format: A string.
                    Default: None.""")
        parser.add_option(
            '--headless', action="store_true",
            dest='headless',
            default=False,
            help="""Using this makes Webdriver run headlessly,
                    which is required on headless machines.""")
        parser.add_option(
            '--demo_mode', action="store_true",
            dest='demo_mode',
            default=False,
            help="""Using this slows down the automation so that
                    you can see what it's actually doing.""")
        parser.add_option(
            '--demo_sleep', action='store', dest='demo_sleep',
            default=None,
            help="""Setting this overrides the Demo Mode sleep
                    time that happens after browser actions.""")
        parser.add_option(
            '--highlights', action='store',
            dest='highlights', default=None,
            help="""Setting this overrides the default number of
                    highlight animation loops to have per call.""")
        parser.add_option(
            '--message_duration', action="store",
            dest='message_duration', default=None,
            help="""Setting this overrides the default time that
                    messenger notifications remain visible when reaching
                    assert statements during Demo Mode.""")
        parser.add_option(
            '--check_js', action="store_true",
            dest='js_checking_on',
            default=False,
            help="""The option to check for JavaScript errors after
                    every page load.""")
        parser.add_option(
            '--ad_block', action="store_true",
            dest='ad_block_on',
            default=False,
            help="""Using this makes WebDriver block display ads
                    that are defined in ad_block_list.AD_BLOCK_LIST.""")
        parser.add_option(
            '--verify_delay', action='store',
            dest='verify_delay', default=None,
            help="""Setting this overrides the default wait time
                    before each MasterQA verification pop-up.""")
        parser.add_option(
            '--disable_csp', action="store_true",
            dest='disable_csp',
            default=False,
            help="""Using this disables the Content Security Policy of
                    websites, which may interfere with some features of
                    SeleniumBase, such as loading custom JavaScript
                    libraries for various testing actions.
                    Setting this to True (--disable_csp) overrides the
                    value set in seleniumbase/config/settings.py""")
        parser.add_option(
            '--save_screenshot', action="store_true",
            dest='save_screenshot',
            default=False,
            help="""Take a screenshot on last page after the last step
                    of the test. (Added to the "latest_logs" folder.)""")
        parser.add_option(
            '--visual_baseline', action='store_true',
            dest='visual_baseline',
            default=False,
            help="""Setting this resets the visual baseline for
                    Automated Visual Testing with SeleniumBase.
                    When a test calls self.check_window(), it will
                    rebuild its files in the visual_baseline folder.""")
        parser.add_option(
            '--timeout_multiplier', action='store',
            dest='timeout_multiplier',
            default=None,
            help="""Setting this overrides the default timeout
                    by the multiplier when waiting for page elements.
                    Unused when tests overide the default value.""")

    def configure(self, options, conf):
        super(SeleniumBrowser, self).configure(options, conf)
        self.enabled = True  # Used if test class inherits BaseCase
        self.options = options
        self.headless_active = False  # Default setting
        proxy_helper.remove_proxy_zip_if_present()

    def beforeTest(self, test):
        test.test.browser = self.options.browser
        test.test.cap_file = self.options.cap_file
        test.test.headless = self.options.headless
        test.test.servername = self.options.servername
        test.test.port = self.options.port
        test.test.proxy_string = self.options.proxy_string
        test.test.user_agent = self.options.user_agent
        test.test.demo_mode = self.options.demo_mode
        test.test.demo_sleep = self.options.demo_sleep
        test.test.highlights = self.options.highlights
        test.test.message_duration = self.options.message_duration
        test.test.js_checking_on = self.options.js_checking_on
        test.test.ad_block_on = self.options.ad_block_on
        test.test.verify_delay = self.options.verify_delay  # MasterQA
        test.test.disable_csp = self.options.disable_csp
        test.test.save_screenshot_after_test = self.options.save_screenshot
        test.test.visual_baseline = self.options.visual_baseline
        test.test.timeout_multiplier = self.options.timeout_multiplier
        test.test.use_grid = False
        if test.test.servername != "localhost":
            # Use Selenium Grid (Use --server=127.0.0.1 for localhost Grid)
            test.test.use_grid = True
        if self.options.headless:
            self.display = Display(visible=0, size=(1920, 1200))
            self.display.start()
            self.headless_active = True
        # The driver will be received later
        self.driver = None
        test.test.driver = self.driver

    def finalize(self, result):
        """ This runs after all tests have completed with nosetests. """
        proxy_helper.remove_proxy_zip_if_present()

    def afterTest(self, test):
        try:
            # If the browser window is still open, close it now.
            self.driver.quit()
        except AttributeError:
            pass
        except Exception:
            pass
        if self.options.headless:
            if self.headless_active:
                self.display.stop()
