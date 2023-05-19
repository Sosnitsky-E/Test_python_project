import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as OptionsFirefox
from selenium.webdriver.support.wait import WebDriverWait


# for correct display of Cyrillic in parameterizers
def pytest_make_parametrize_id(config, val): return repr(val)


# add a test launch option on the command line (than run, chrome or firefox) By default chrome
def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action="store", default='en',
                     help='Choose language: en/ru/fr...(etc)')


@pytest.fixture(scope="function")
def browser(request):
    user_language = request.config.getoption("language")
    browser_name = request.config.getoption("browser_name")
    driver = None
    if browser_name == "chrome":
        print("\n install Chrome driver for test...")
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        driver = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        print("\n install Firefox for trest...")
        options_firefox = OptionsFirefox()
        options_firefox.set_preference("intl.accept_languages", user_language)
        driver = webdriver.Firefox(options=options_firefox)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield driver
    print("\n quit browser")
    driver.quit()
