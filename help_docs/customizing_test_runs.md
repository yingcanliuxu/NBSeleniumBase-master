### Customizing test runs with **pytest** (or nosetests)

In addition to [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) (which lets you customize SeleniumBase global properties) you can customize test runs from the command line:

* Choose the browser for tests to use (Default: Chrome)
* Choose betweeen pytest & nose unittest runners
* Choose whether to enter Debug Mode on failures
* Choose additional variables to pass into tests
* Choose the User-Agent for the browser to use
* Change the automation speed (with Demo Mode)
* Choose whether to run tests multi-threaded
* Choose whether to retry failing tests
* Choose a BrowserStack server to run on
* Choose a Sauce Labs server to run on
* Choose a TestingBot server to run on
* Choose a CrossBrowserTesting server
* Choose a Selenium Grid to connect to
* Choose a database to save results to
* Choose a proxy server to connect to

...and more!

#### **Examples:**

(These are run from the **[examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)** folder.)

```bash
pytest my_first_test.py

pytest my_first_test.py --demo_mode --browser=chrome

pytest my_first_test.py --browser=firefox

pytest test_suite.py --html=report.html

nosetests test_suite.py --report --show_report

pytest test_suite.py --headless -n 4

pytest test_suite.py --reruns 1 --reruns-delay 2

pytest test_suite.py --server=IP_ADDRESS --port=4444

pytest proxy_test.py --proxy=IP_ADDRESS:PORT

pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT

pytest user_agent_test.py --agent="USER-AGENT STRING"

pytest test_fail.py --pdb -s
```

You can interchange **pytest** with **nosetests**, but using pytest is strongly recommended because developers stopped supporting nosetests. Chrome is the default browser if not specified.

(NOTE: If you're using **pytest** for running tests outside of the SeleniumBase repo, **you'll want a copy of [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini) at the base of the new folder structure**. If using **nosetests**, the same applies for [setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg).)

#### **Running tests on [BrowserStack](https://www.browserstack.com/automate#)'s Selenium Grid, the [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium) Selenium Grid, the [TestingBot](https://testingbot.com/features) Selenium Grid, (or your own):**

Here's how to connect to a BrowserStack Selenium Grid server for running tests:

```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

Here's how to connect to a Sauce Labs Selenium Grid server for running tests:

```bash
pytest my_first_test.py --server=USERNAME:KEY@ondemand.saucelabs.com --port=80
```

Here's how to connect to a TestingBot Selenium Grid server for running tests:

```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.testingbot.com --port=80
```
Here's how to connect to a CrossBrowserTesting Selenium Grid server for running tests:

```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.crossbrowsertesting.com --port=80
```

Or you can create your own Selenium Grid for test distribution. ([See this ReadMe for details](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md))

#### **Example tests using Logging:**

```bash
pytest test_suite.py --browser=chrome
```
(During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), otherwise log files with be cleaned up at the start of the next test run.)

#### **Demo Mode:**

If any test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo_mode`` on the command line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:

```bash
pytest my_first_test.py --browser=chrome --demo_mode
```

You can override the default wait time by either updating [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) or by using ``--demo_sleep={NUM}`` when using Demo Mode. (NOTE: If you use ``--demo_sleep={NUM}`` without using ``--demo_mode``, nothing will happen.)

```bash
pytest my_first_test.py --browser=chrome --demo_mode --demo_sleep=1.2
```

#### **Passing additional data to tests:**

If you want to pass additional data from the command line to your tests, you can use ``--data=STRING``. Now inside your tests, you can use ``self.data`` to access that.

#### **Running tests multithreaded:**

To run Pytest multithreaded on multiple CPUs at the same time, add ``-n=NUM`` or ``-n NUM`` on the command line, where NUM is the number of CPUs you want to use.

#### **Retrying failing tests automatically:**

You can use ``--reruns NUM`` to retry failing tests that many times. Use ``--reruns-delay SECONDS`` to wait that many seconds between retries. Example:
```
pytest --reruns 5 --reruns-delay 1
```

#### **Debugging tests:**

**You can use the following code snippets in your scripts to help you debug issues:**
```python
import time; time.sleep(5)  # sleep for 5 seconds (add this after the line you want to pause on)
import ipdb; ipdb.set_trace()  # waits for your command. n = next line of current method, c = continue, s = step / next executed line (will jump)
import pytest; pytest.set_trace()  # similar to ipdb, but specific to pytest
```

**To pause an active test that throws an exception or error, add ``--pdb -s``:**

```bash
pytest my_first_test.py --browser=chrome --pdb -s
```

The code above will leave your browser window open in case there's a failure. (ipdb commands: 'c', 's', 'n' => continue, step, next).

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes.

```bash
nosetests test_suite.py --report
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)

Here are some other useful **nosetest**-specific arguments:

```bash
--logging-level=INFO  # Hide DEBUG messages, which can be overwhelming.
-x  # Stop running the tests after the first failure is reached.
-v  # Prints the full test name rather than a dot for each test.
--with-id  # If -v is also used, will number the tests for easy counting.
```

#### **Using a Proxy Server:**

If you wish to use a proxy server for your browser tests (Chrome and Firefox only), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command line.

```bash
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

If the proxy server that you wish to use requires authentication, you can do the following (Chrome only):

```bash
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

To make things easier, you can add your frequently-used proxies to PROXY_LIST in [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), and then use ``--proxy=KEY_FROM_PROXY_LIST`` to use the IP_ADDRESS:PORT of that key.

```bash
pytest proxy_test.py --proxy=proxy1
```

#### **Changing the User-Agent:**

If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER-AGENT STRING"`` as an argument on the command line.

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```
