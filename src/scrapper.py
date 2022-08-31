"""spider module"""
import os
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from urllib.parse import urlparse
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
        self.user_agent = class_config["user_agent"]
        self.links = []

    def run(self):
        """run main engine of webscrapper"""
        self.__check_and_create_directory__()
        self.logger.logger.info("Starting scrape to " + self.url)
        self.logger.logger.info("recursive level: " + str(self.level))
        self.logger.logger.info("path to store: " + self.path)
        urllib3.disable_warnings()
        try:
            self.find_links()
            self.find_images_and_docs()
        except Exception as exc:
            self.logger.logger.error(str(exc))
            return

    def find_links(self):
        """find links recursively"""
        self.links.append([])
        self.links[0].append(self.url)
        for i in range(1, self.level):
            self.links.append([])
            for link in self.links[i-1]:
                try:
                    soup = self._soupear(link)
                except Exception as exc:
                    raise exc
                links = soup.find_all('a')
                for soup_link in links:
                    try:
                        href = soup_link.attrs['href']
                        if href.startswith(self.url)\
                            and not any([href in list for list in self.links]):
                            self.logger.logger.info("found " + href)
                            self.links[i].append(href)
                    except KeyError:
                        continue

    def find_images_and_docs(self):
        """download images"""
        for link_list in self.links:
            for link in link_list:
                try:
                    soup = self._soupear(link)
                except Exception as exc:
                    raise exc
                images = soup.find_all('img')
                new_links = soup.find_all('a')
                self.download_files(images, 'src')
                self.download_files(new_links, 'href')

    def download_files(self, items, value):
        """find all images, word and pdf files at the given URL"""
        for item in items:
            file = ""
            if item.attrs:
                try:
                    file = item.attrs[value]
                except KeyError:
                    continue
            if file.split('.')[-1] in self.extensions:
                file_name = file.split('/')[-1]
                if not Spiderscrapper.validate_url(file):
                    url = urlparse(self.url)
                    file = url.scheme + '://' + url.netloc + file
                try:
                    self.logger.logger.info("downloading " + file_name + ' from ' + file)
                    urlretrieve(quote_plus(file, safe=':/'), self.path + '\\' + file_name)
                except Exception as exc:
                    self.logger.logger.error(str(exc) + '. Couldn\'t download ' + file_name)

    def _soupear(self, link):
        """function makes request and soup"""
        try:
            request = Spiderscrapper.download_html(link, self.user_agent)
            soup = Spiderscrapper.create_soup(request.text)
        except Exception as exc:
            raise exc
        return soup

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
    def download_html(url, user_agent):
        """get the html"""
        sesion = requests.Session()
        request = sesion.get(url, headers={"User-Agent": user_agent}, verify=False)
        return request

    @staticmethod
    def create_soup(request):
        """function returns a soup object"""
        soup = BeautifulSoup(request, 'lxml')
        return soup
