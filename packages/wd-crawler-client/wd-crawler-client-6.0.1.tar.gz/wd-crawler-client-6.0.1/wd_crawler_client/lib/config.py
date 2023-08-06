# -*- coding: utf-8 -*-
import os
import ConfigParser


class Config(object):

    def __init__(self, config_file):
        if not os.path.exists(config_file):
            raise Exception('config file not exists')
        self.config_file = config_file
        self.configs = {}
        self.load_config()

    def load_config(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.config_file)
        for section in cp.sections():
            config = {}
            for key, value in cp.items(section):
                config[key] = value
            self.configs[section] = config

    def get(self, section):
        return self.configs.get(section, None)

    def get_db_params(self, section, original=False):
        config = self.get(section)
        if config and 'host' in config and 'user' in config and 'password' in config and 'db' in config:
            if original:
                return {'host': config['host'], 'user': config['user'], 'passwd': config['password'], 'db': config['db']}
            return {'host': config['host'], 'user': config['user'], 'password': config['password'], 'db': config['db']}
        return None
