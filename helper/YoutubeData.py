import logging
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import json

class YoutubeCrawler:
    """
    This class provides data retrievel methods from youtube
    """

    # initialize url
    def __init__(self, youtube_url):
        self._url = youtube_url
        self._logger = logging.getLogger("YoutubeCrawler")

    # Get webpage data
    def get_webpage(self):

        try:

            self._logger.debug("Getting Webpage...")
            uclient = uReq(self._url)
            self._logger.debug("Done")

        except Exception as e:
            self._logger.error(e)
        else:
            return uclient

    # read web page
    def read_webpage(self, uclient):

        try:
            self._logger.debug("Reading Webpage...")
            yt_page = uclient.read()
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return yt_page

    # convert page data to html
    def convert_webpage_to_html(self, yt_page):

        try:
            self._logger.debug("Converting Webpage to HTML...")

            yt_html = bs(yt_page, "html.parser")

            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return yt_html

    def convert_to_json(self, box):
        try:
            self._logger.debug("Converting to JSON...")
            print(box.getText())
            json_object = json.loads(box.getText())
            self._logger.debug("Done")
        except Exception as e:
            self._logger.error(e)
        else:
            return json_object
