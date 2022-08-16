"""spider module"""
import os
from urllib.request import urlretrieve
from urllib.parse import quote_plus
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
        self.find_links()
        self.find_images()

    def find_links(self):
        """find links recursively"""
        request = Spiderscrapper.download_html(self.url)
        soup = Spiderscrapper.create_soup(request.text)
        links = soup.find_all('a')
        for link in links:
            href = link.attrs['href']
            if href.startswith(self.url) and href not in self.links:
                self.links.append(href)
            if len(self.links) == self.level:
                return

    def find_images(self):
        """download images"""
        for link in self.links:
            request = Spiderscrapper.download_html(link)
            soup = Spiderscrapper.create_soup(request.text)
            images = soup.find_all('img')
            self.download_images(images)

    def download_images(self, images):
        """find all images in web"""
        for image in images:
            src = image.attrs['src']
            if src.split('.')[-1] in self.extensions:
                image_name = src.split('/')[-1]
                urlretrieve(quote_plus(src, safe=':/'), self.path + '\\' + image_name)

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
