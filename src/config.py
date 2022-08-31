"""Library to interact with configfile"""
import configparser
import argparse

class Configlibrary:
    """Class where it's stored the configuration of the program"""
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('configuration/arachnida.config')
        self.argparse = argparse
        self.parser = argparse.ArgumentParser(
            description="""ARACHNIDA WEB SCRAPPER:\n
                        This program downloads all the images and metadata from given URL""")

    def set_parser_description(self, text):
        """function sets argparse description"""
        self.parser = argparse.ArgumentParser(description=text)

    def get_default_level(self):
        """function returns default recursive level"""
        return self.config['program']['level']

    def get_recursive_level(self):
        """function returns configured recursive level"""
        return self.config['recursive']['level']

    def get_extensions(self):
        """function returns the target extensions"""
        extensions_list = []
        with open(self.config['program']['extensions'], 'rb') as extensions_file:
            extensions_str = extensions_file.read().decode("utf-8")
        extensions_list = extensions_str.split('\r\n')
        return extensions_list

    def get_default_path(self):
        """function returns default path"""
        return self.config['program']['path']

    def get_log_level(self):
        """function returns log level"""
        return self.config['log']['level']

    def get_user_agent(self):
        """function returns user agent"""
        return self.config['program']['user-agent']
