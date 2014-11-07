'''
config.py
Description#   Configuration of the system
Developer#     Thada Wangthammang
'''
import os

# global variable
db_name = 'r2alsdb'
db_name_test = 'r2alsdb_test'
host = 'localhost'
is_reset = True
root_path = os.path.dirname(os.path.dirname(__file__))+'/'
data_path = root_path + 'data/'


import configparser


class Configurator:
    settings = dict()

    def __init__(self, config_file):
        self.config_file = config_file
        self.__parse()

    def __parse(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_file)

        sections = ['r2als']

        boolean_conf = ['is_reset']
        integer_conf = ['']


        for key in boolean_conf:
            self.settings[key] = False

        for section in sections:
            if not config_parser.has_section(section):
                continue

            for k, v in config_parser.items(section):
                if k in boolean_conf:
                    self.settings[k] = config_parser.getboolean(section, k)
                elif k in integer_conf:
                    self.settings[k] = config_parser.getint(section, k)
                else:
                    self.settings[k] = v

    def get(self, key):
        if key not in self.settings:
            return None

        return self.settings[key]

    def keys(self):
        return self.settings.keys()

    def items(self):
        return self.settings.items()

    def set(self, key, value):
        self.settings[key] = value
