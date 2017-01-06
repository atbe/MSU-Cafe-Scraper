from bs4 import BeautifulSoup
from urllib import request
from CafeScraper.Cafe import Cafe

class Scraper(object):
    """
    The Scraper object will contain all the cafe
    objects already built at construction time.

    This class allows the user to interact with all the cafes

    """
    CAFE_BASE_URL = 'https://eatatstate.com'

    def __init__(self):
        self.cafes = self._go_download_cafes()

    def _go_download_cafes(self):
        cafes = []
        page_bytes = request.urlopen(self.CAFE_BASE_URL + '/menus')
        soup = BeautifulSoup(page_bytes, 'html.parser')

        """
         here we will get all the cafeterias
        """
        #
        # The div of the cafeterias is contained in a day named
        # 'node-inner' and is named 'content'
        node_inner_div = soup.find_all('div', attrs={'class': 'node-inner'})[0]
        cafe_list_div = node_inner_div.find_all('div', attrs={'class': 'content'})[0]

        # all the cafeterias are in a list in this div
        for li in cafe_list_div.find_all('li'):
            caf_anchor = li.find('a')
            caf_name = caf_anchor.text
            caf_endpoint = caf_anchor.get('href')

            #print(caf_name, caf_endpoint)

            cafes.append(Cafe(caf_name, caf_endpoint))

        return cafes