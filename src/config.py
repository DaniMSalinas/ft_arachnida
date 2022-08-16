"""Library to interact with configfile"""
import configparser
import argparse

class Configlibrary:
    """Class where it's stored the configuration of the program"""
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('configuration/arachnida.config')
        self.parser = argparse.ArgumentParser(
            description="""ARACHNIDA WEB SCRAPPER:\n
                        This program downloads all the images and metadata from given URL""")
        self.set_arguments()

    def set_arguments(self):
        """function to set arguments of main program"""
        self.parser.add_argument('url', metavar='<URL>', type=str)
        self.parser.add_argument('-r', '--recursive', action='store_true',
                                help="recursive images download")
        self.parser.add_argument('-l', '--level', metavar='<N>',
                                type=int, help="sets the downloading recursive-level")
        self.parser.add_argument('-p', '--path', metavar='<PATH>', type=str,
                                help="sets the path where the info downloaded is going to be saved")
        self.parser.add_argument('-rl', '--recursive-level', metavar='<URL> <N>',
                                type=str, help=argparse.SUPPRESS)
        self.parser.add_argument('-rp', '--recursive-path', metavar='<URL> <PATH>', type=str,
                                help=argparse.SUPPRESS)

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

    def _validate_level(self):
        """function validates level given as argument"""
