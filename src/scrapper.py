"""spider module"""
import os
from urllib.request import urlretrieve
from urllib.parse import quote_plus
import urllib3
import validators
import requests
from bs4 import BeautifulSoup

class Spiderscrapper():
    """spider class"""
    def __init__(self, url, class_config, logger=None):
        self.logger = logger
        if url.endswith('/'):
            self.url = url
        else:
            self.url = url + '/'
        self.extensions = class_config["extensions"]
        self.path = class_config["path"]
        self.level = int(class_config["level"])
        self.links = []

    def run(self):
        """run main engine of webscrapper"""
        self.__check_and_create_directory__()
        self.logger.logger.info("Starting scrape to " + self.url)
        self.logger.logger.info("recursive level: " + str(self.level))
        self.logger.logger.info("path to store: " + self.path)
        urllib3.disable_warnings()
        self.find_links()
        self.find_images_and_docs()

    def find_links(self):
        """find links recursively"""
        self.links.append(self.url)
        request = Spiderscrapper.download_html(self.url)
        soup = Spiderscrapper.create_soup(request.text)
        links = soup.find_all('a')
        for link in links:
            href = link.attrs['href']
            if href.startswith(self.url) and href not in self.links:
                self.logger.logger.info("found " + href)
                self.links.append(href)
            if len(self.links) == self.level:
                return

    def find_images_and_docs(self):
        """download images"""
        for link in self.links:
            request = Spiderscrapper.download_html(link)
            soup = Spiderscrapper.create_soup(request.text)
            images = soup.find_all('img')
            new_links = soup.find_all('a')
            iframes = soup.find_all('iframe')
            self.download_files(images, 'src')
            self.download_files(new_links, 'href')
            self.download_files(iframes, 'src')

    def download_files(self, items, value):
        """find all images, word and pdf files at the given URL"""
        for item in items:
            file = item.attrs[value]
            if file.split('.')[-1] in self.extensions:
                file_name = file.split('/')[-1]
                self.logger.logger.info("downloading " + file_name + ' from ' + file)
                try:
                    urlretrieve(quote_plus(file, safe=':/'), self.path + '\\' + file_name)
                except Exception as exc:
                    self.logger.logger.error(exc)

    def __check_and_create_directory__(self):
        """function checks and create if it's necesary a directory"""
        if os.path.isdir(self.path):
            return
        paths = self.path.split('\\')
        absolute_path = os.getcwd()
        for path in paths:
            absolute_path += '\\' + path
            os.mkdir(absolute_path)

    @staticmethod
    def validate_url(url):
        """Functions validates that a url is a truly url"""
        if validators.url(url):
            return True
        return False

    @staticmethod
    def download_html(url):
        """get the html"""
        request = requests.get(url, verify=False)
        return request

    @staticmethod
    def create_soup(request):
        """function returns a soup object"""
        soup = BeautifulSoup(request, 'lxml')
        return soup
