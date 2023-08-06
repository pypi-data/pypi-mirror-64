from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ChromeCapabilities(object):

    default = {
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY',

        'goog:chromeOptions': {

            'prefs': {},

            'extensions': [],

            'args': [
                'disable-auto-reload',
                'log-level=2',
                'disable-notifications',
                'start-maximized',
                'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"'
            ]

        },

        'proxy': {
            'httpProxy': None,
            'ftpProxy': None,
            'sslProxy': None,
            'noProxy': None,
            'proxyType': 'MANUAL',
            'class': 'org.openqa.selenium.Proxy',
            'autodetect': False
        }
    }

    def __init__(self):
        self.desired = self.default.copy()

    def add_argument(self, argument):
        arguments = self.desired['goog:chromeOptions']['args']
        duplicate_argument = [arg for arg in arguments if arg.split("=")[0] == argument.split("=")[0]]

        if not duplicate_argument:
            arguments.append(argument)

        elif (argument.startswith('window-size')) and ('start-maximized' in arguments):
            arguments.remove('start-maximized')
            arguments.append(argument)

        else:
            arguments.remove(duplicate_argument[0])
            arguments.append(argument)

    def add_extension(self, argument):
        extensions = self.desired['goog:chromeOptions']['extensions']

        if extension not in extensions:
            extensions.append(extension)

    def add_experimental_option(self, experimental_option):
        self.desired['goog:chromeOptions']['prefs'] = experimental_option

    def set_user_agent(self, user_agent):
        self.add_argument('user-agent={}'.format(user_agent))

    def set_proxy(self, proxy):
        proxy_types_list = ['httpProxy', 'ftpProxy', 'sslProxy']

        for type in proxy_types_list:
            self.desired['proxy'][type] = proxy

    def set_download_folder(self, folder_path):
        self.desired['goog:chromeOptions']['prefs']['download.default_directory'] = folder_path

    def set_window_size(self, window_size):
        self.add_argument('window-size={}'.format(window_size.replace("x", ",")))

    @classmethod
    def from_selenium_options(cls, selenium_options):
        current_options = selenium_options.to_capabilities()
        cls.default['goog:chromeOptions'] = current_options['goog:chromeOptions']
        return cls()
