# Copyright (C) 2019 Shiela Buitizon | Joshua Kim Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from collections import namedtuple

from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys

from AppiumLibrary import VERSION
from AppiumLibrary import (
    _LoggingKeywords,
    _RunOnFailureKeywords,
    _ElementKeywords,
    _ScreenshotKeywords,
    _ApplicationManagementKeywords,
    _WaitingKeywords,
    _TouchKeywords,
    _KeyeventKeywords,
    _AndroidUtilsKeywords,
)

__version__ = '0.6a1'


class _ApplicationManagementExtendedKeywords(
    _ApplicationManagementKeywords,
    _WaitingKeywords,
    _ElementKeywords
):

    js_marker = 'JAVASCRIPT'
    arg_marker = 'ARGUMENTS'

    def __init__(self):
        super().__init__()

    @staticmethod
    def _log(*args, **kwargs):
        BuiltIn().log(*args, **kwargs)

    def switch_window(self, window):
        """ Change focus to another window (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().switch_to.window(window)

    def close_window(self):
        """ Closes the current window (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().close()

    def get_current_window_handle(self):
        """ Retrieves the current window handle (Web context only).
            Returns the window handle as string.

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().current_window_handle

    def get_window_handles(self):
        """ Retrieves the list of all window handles available to \
            the session (Web context only).
            Returns a list if there are more than one window active.

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().window_handles

    def get_title(self):
        """ Get the current page title (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().title

    def get_location(self):
        """ Retrieve the URL of the current page (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().current_url()

    def reload_page(self):
        """ Refreshes the current page. (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().refresh()

    def get_cookies(self):
        """ Retrieves all cookies visible to the current page \
            (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().get_cookies

    def add_cookie(self, **kwargs):
        """Set a cookie (Web context only).
           Arguments should be given like the example:
           NOTE: ``name`` and ``value`` arguments are required, \
               ``path``, ``domain``, ``expiry`` and ``secure`` \
                   are optional.
           | Set Cookie   | name=_cookieName   | value=someValue |
           | Set Cookie   | name=_cookieName   | value=someValue \
               | path=some/path | domain=.cookie.com |

           *AppiumExtensionLibrary Only Keyword*.
        """
        try:
            self._current_application().add_cookie(kwargs)
        except Exception as err:
            raise err

    def delete_cookie(self, cookieName):
        """ Delete the cookie with the given name (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        try:
            self._current_application().delete_cookie(cookieName)
        except Exception as err:
            raise err

    def delete_all_cookies(self):
        """ Delete the cookie with the given name (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().delete_all_cookies()

    def go_to(self, url):
        """ Opens URL in default web browser.

            Example:
            | Open Application  | http://localhost:4755/wd/hub | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | browserName=Safari |
            | Go To URL         | http://m.webapp.com          |
        """
        self.go_to_url(url)

    def execute_javascript(self, *code):
        """Executes the given JavaScript code with possible arguments.

        ``code`` may be divided into multiple cells in the test data and
        ``code`` may contain multiple lines of code and arguments. In that case,
        the JavaScript code parts are concatenated together without adding
        spaces and optional arguments are separated from ``code``.

        If ``code`` is a path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

        The JavaScript executes in the context of the currently selected
        frame or window as the body of an anonymous function. Use ``window``
        to refer to the window of your application and ``document`` to refer
        to the document object of the current frame or window, e.g.
        ``document.getElementById('example')``.

        This keyword returns whatever the executed JavaScript code returns.
        Return values are converted to the appropriate Python types.

        Starting from SeleniumLibrary 3.2 it is possible to provide JavaScript
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_script|
        arguments] as part of ``code`` argument. The JavaScript code and
        arguments must be separated with `JAVASCRIPT` and `ARGUMENTS` markers
        and must be used exactly with this format. If the Javascript code is
        first, then the `JAVASCRIPT` marker is optional. The order of
        `JAVASCRIPT` and `ARGUMENTS` markers can be swapped, but if `ARGUMENTS`
        is the first marker, then `JAVASCRIPT` marker is mandatory. It is only
        allowed to use `JAVASCRIPT` and `ARGUMENTS` markers only one time in the
        ``code`` argument.

        Examples:
        | `Execute JavaScript` | window.myFunc('arg1', 'arg2') |
        | `Execute JavaScript` | ${CURDIR}/js_to_execute.js    |
        | `Execute JavaScript` | alert(arguments[0]); | ARGUMENTS | 123 |
        | `Execute JavaScript` | ARGUMENTS | 123 | JAVASCRIPT | alert(arguments[0]); |

        *AppiumExtensionLibrary Only Keyword*.
        """
        js_code, js_args = self._get_javascript_to_execute(code)
        return self._current_application().execute_script(js_code, *js_args)

    def element_execute_javascript(self, locator, *code):
        """Executes the given JavaScript code given using locator element

        Similar to `Execute Javascript` except that keyword accepts locator parameter
        and can use locator element in javascript command.

        ``code`` may be divided into multiple cells in the test data and
        ``code`` may contain multiple lines of code and arguments. In that case,
        the JavaScript code parts are concatenated together without adding
        spaces and optional arguments are separated from ``code``.

        If ``code`` is a path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

        The JavaScript executes in the context of the currently selected
        frame or window as the body of an anonymous function. Use ``window``
        to refer to the window of your application and ``document`` to refer
        to the document object of the current frame or window, e.g.
        ``document.getElementById('example')``.

        This keyword returns whatever the executed JavaScript code returns.
        Return values are converted to the appropriate Python types.

        Starting from SeleniumLibrary 3.2 it is possible to provide JavaScript
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_script|
        arguments] as part of ``code`` argument. The JavaScript code and
        arguments must be separated with `JAVASCRIPT` and `ARGUMENTS` markers
        and must be used exactly with this format. If the Javascript code is
        first, then the `JAVASCRIPT` marker is optional. The order of
        `JAVASCRIPT` and `ARGUMENTS` markers can be swapped, but if `ARGUMENTS`
        is the first marker, then `JAVASCRIPT` marker is mandatory. It is only
        allowed to use `JAVASCRIPT` and `ARGUMENTS` markers only one time in the
        ``code`` argument.

        Examples:
        | `Execute JavaScript` | css=#id | | ${CURDIR}/js_to_execute.js | ARGUMENTS | 123 |

        Sample ${CURDIR}/js_to_execute.js file:

        ``arguments[0].value=arguments[1]``

        *AppiumExtensionLibrary Only Keyword*.
        """

        element = self._element_find(locator, True, True)
        self._log("Element " + str(element))

        js_code, js_args = self._get_javascript_to_execute(code)
        actual_js_args = list()
        actual_js_args.append(element)
        actual_js_args += js_args
        return self._current_application().execute_script(js_code, *actual_js_args)

    def input_text(self, locator, text, clear=True, events=False):
        """Types the given ``text`` into the text field identified by ``locator``.

        When ``clear`` is true, the input element is cleared before
        the text is typed into the element. When false, the previous text
        is not cleared from the element. Use `Input Password` if you
        do not want the given ``text`` to be logged.

        When ``events`` is true, ``focus`` is triggered before and ``blur`` is triggered after input on field.
        Also, if ``event`` is true, text deletion is via send keys (CRTL+a,DELETE)

        If [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid]
        is used and the ``text`` argument points to a file in the file system,
        then this keyword prevents the Selenium to transfer the file to the
        Selenium Grid hub. Instead, this keyword will send the ``text`` string
        as is to the element. If a file should be transferred to the hub and
        upload should be performed, please use `Choose File` keyword.

        See the `Locating elements` section for details about the locator
        syntax. See the `Boolean arguments` section how Boolean values are
        handled.

        Disabling the file upload the Selenium Grid node and the `clear`
        argument are new in SeleniumLibrary 4.0

        *AppiumExtensionLibrary Only Keyword*.
        """
        self._input_text_into_text_field(locator, text, clear, events)

    def wait_until_element_is_enabled(self, locator, timeout='3s'):
        """Waits until the element ``locator`` is enabled.

        Element is considered enabled if it is not disabled nor read-only.

        Fails if ``timeout`` expires before the element is enabled. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        Considering read-only elements to be disabled is a new feature
        in SeleniumLibrary 3.0.
        """
        self._wait_until(
            timeout,  "Element '%s' was not enabled in <TIMEOUT>." % locator,
            lambda: self._element_find(locator, True, True).is_enabled()
        )

    def _input_text_into_text_field(self, locator, text, clear, events):
        element = self._element_find(locator, True, True)
        self._log("Element " + str(element))

        if events:
            self._log("Element focus")
            self._current_application().execute_script("arguments[0].focus();", element)

        if events and clear:
            self._log("Element clear by send keys")
            element.send_keys(Keys.CONTROL, 'a')
            element.send_keys(Keys.DELETE)
        elif clear:
            self._log("Element cleared by js")
            self._current_application().execute_script("arguments[0].value='';", element)

        if text:
            self._log(f"Element sendkeys *{text}*")
            element.send_keys(str(text))
        if events:
            self._log("Element onblur")
            self._current_application().execute_script("arguments[0].blur();", element)

    def _get_javascript_to_execute(self, code):
        js_code, js_args = self._separate_code_and_args(code)
        if not js_code:
            raise ValueError('JavaScript code was not found from code argument.')
        js_code = ''.join(js_code)
        path = js_code.replace('/', os.sep)
        if os.path.isfile(path):
            js_code = self._read_javascript_from_file(path)
        return js_code, js_args

    def _separate_code_and_args(self, code):
        code = list(code)
        self._check_marker_error(code)
        index = self._get_marker_index(code)
        if self.arg_marker not in code:
            return code[index.js + 1:], []
        if self.js_marker not in code:
            return code[0:index.arg], code[index.arg + 1:]
        else:
            if index.js == 0:
                return code[index.js + 1:index.arg], code[index.arg + 1:]
            else:
                return code[index.js + 1:], code[index.arg + 1:index.js]

    def _check_marker_error(self, code):
        if not code:
            raise ValueError('There must be at least one argument defined.')
        message = None
        template = '%s marker was found two times in the code.'
        if code.count(self.js_marker) > 1:
            message = template % self.js_marker
        if code.count(self.arg_marker) > 1:
            message = template % self.arg_marker
        index = self._get_marker_index(code)
        if index.js > 0 and index.arg != 0:
            message = template % self.js_marker
        if message:
            raise ValueError(message)

    def _get_marker_index(self, code):
        Index = namedtuple('Index', 'js arg')
        if self.js_marker in code:
            js = code.index(self.js_marker)
        else:
            js = -1
        if self.arg_marker in code:
            arg = code.index(self.arg_marker)
        else:
            arg = -1
        return Index(js=js, arg=arg)

    def _read_javascript_from_file(self, path):
        self._log('Reading JavaScript from file %s.' % path.replace(os.sep, '/'))
        with open(path) as file:
            return file.read().strip()


class AppiumExtensionLibrary(
    _LoggingKeywords,
    _RunOnFailureKeywords,
    _ScreenshotKeywords,
    _ApplicationManagementExtendedKeywords,
    _TouchKeywords,
    _KeyeventKeywords,
    _AndroidUtilsKeywords
):
    """AppiumExtensionLibrary is a Mobile App testing \
        library for Robot Framework.

    = Locating or specifying elements =

    All keywords in AppiumLibrary that need to find an \
        element on the page
    take an argument, either a ``locator`` or a \
        ``webelement``. ``locator``
    is a string that describes how to locate an element \
        using a syntax
    specifying different location strategies. \
        ``webelement`` is a variable that
    holds a WebElement instance, which is a representation \
        of the element.

    == Using locators ==

    By default, when a locator is provided, it is matched \
        against the key attributes
    of the particular element type. For iOS and Android, \
        key attribute is ``id`` for
    all elements and locating elements is easy using just \
        the ``id``. For example:

    | Click Element    id=my_element

    New in AppiumLibrary 1.4, ``id`` and ``xpath`` are not \
        required to be specified,
    however ``xpath`` should start with ``//`` else just use ``xpath`` locator as explained below.

    For example:

    | Click Element    my_element
    | Wait Until Page Contains Element    //*[@type="android.widget.EditText"]


    Appium additionally supports some of the [https://w3c.github.io/webdriver/webdriver-spec.html|Mobile JSON Wire Protocol] locator strategies.
    It is also possible to specify the approach AppiumLibrary should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy*        | *Example*                                                      | *Description*                     | *Note*                      |
    | identifier        | Click Element `|` identifier=my_element                        | Matches by @id attribute          |                             |
    | id                | Click Element `|` id=my_element                                | Matches by @resource-id attribute |                             |
    | accessibility_id  | Click Element `|` accessibility_id=button3                     | Accessibility options utilize.    |                             |
    | xpath             | Click Element `|` xpath=//UIATableView/UIATableCell/UIAButton  | Matches with arbitrary XPath      |                             |
    | class             | Click Element `|` class=UIAPickerWheel                         | Matches by class                  |                             |
    | android           | Click Element `|` android=UiSelector().description('Apps')     | Matches by Android UI Automator   |                             |
    | ios               | Click Element `|` ios=.buttons().withName('Apps')              | Matches by iOS UI Automation      |                             |
    | nsp               | Click Element `|` nsp=name=="login"                            | Matches by iOSNsPredicate         | Check PR: #196              |
    | css               | Click Element `|` css=.green_button                            | Matches by css in webview         |                             |
    | name              | Click Element `|` name=my_element                              | Matches by @name attribute        | *Only valid* for Selendroid |

    == Using webelements ==

    Starting with version 1.4 of the AppiumLibrary, one can pass an argument
    that contains a WebElement instead of a string locator. To get a WebElement,
    use the new `Get WebElements` or `Get WebElement` keyword.

    For example:
    | @{elements}    Get Webelements    class=UIAButton
    | Click Element    @{elements}[2]

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        """AppiumExtensionLibrary can be imported with optional arguments.

        ``timeout`` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.

        ``run_on_failure`` specifies the name of a keyword (from any available
        libraries) to execute when a AppiumLibrary keyword fails.

        By default `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        Examples:
        | Library | AppiumExtensionLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | AppiumExtensionLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        super().__init__()
        for base in AppiumExtensionLibrary.__bases__:
            base.__init__(self)
        self.set_appium_timeout(timeout)
        self.register_keyword_to_run_on_failure(run_on_failure)
