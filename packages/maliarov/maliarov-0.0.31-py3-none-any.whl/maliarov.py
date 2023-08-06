#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import datetime

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

class CommonActions():

    def __init__(self):
        pass

    def file_to_list(self, path_to_file, encryption = 'utf-8', duplicates = True):
        handle = open(path_to_file, "r", encoding = encryption)
        if duplicates:
            data = [line.replace("\n", "") for line in handle.readlines()]
        else:
            data = list(dict.fromkeys([line.replace("\n", "") for line in handle.readlines()]))
        handle.close()
        return data

    def divide_list(self, lst, parts):
        medium_number = int(len(lst)) // parts
        divided_list = list()
        for i in range(0, parts):
            divided_list.append(lst[(medium_number * i):(medium_number * (i + 1))])
        if int(len(lst)) % parts != 0:
            divided_list[-1].extend(lst[(medium_number * parts):])
        return divided_list

    def write_list_as_line(self, path_to_file, info, delimiter = ',', encryption = 'utf-8', headers = False):
        if headers:
            mode = 'w'
        else:
            mode = 'a'

        handle = open(path_to_file, mode = mode, encoding = encryption)
        handle.write(delimiter.join(info) + '\n')
        handle.close()

    def create_dates_list(self, start_date, end_date, input_format = "%m/%d/%Y", output_format = "%m/%d/%Y"):
        sdate = datetime.datetime.strptime(start_date, input_format)
        edate = datetime.datetime.strptime(end_date, input_format)
        date_list = list(reversed([(edate - datetime.timedelta(days=x)).strftime(output_format) for x in range((edate - sdate).days + 1)]))
        return date_list

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
