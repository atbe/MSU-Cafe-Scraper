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
        self.cafes_dict = { 'shaw': None, 'gallery': None, 'landon': None, 'case': None,
            'brody': None, 'akers': None, 'holmes': None, 'holden': None, 'wilson': None }

        self._go_download_cafes()

    def _go_download_cafes(self):
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

            cafe_dict_key = ""
            try:
                cafe_dict_key = caf_endpoint.split('/')[2].strip().lower()
            except IndexError:
                #print("Not a desired cafeteria menu.")
                continue
            # skipping non-cafeteria menus. Cafe menus have 'menus' in their endpoint
            if 'menus' not in caf_endpoint or cafe_dict_key not in self.cafes_dict:
                continue

            # index two is the name of the cafe
            self.cafes_dict[cafe_dict_key] = Cafe(caf_name, caf_endpoint)

