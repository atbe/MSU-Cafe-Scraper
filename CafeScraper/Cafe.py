from bs4 import BeautifulSoup
from urllib import request
from CafeScraper.Restaurant import Restaurant

class Cafe(object):

    CAFE_BASE_URL = 'https://eatatstate.com'

    def __init__(self, unique_name, cover_name, endpoint):
        self.unique_name = unique_name
        self.cover_name = cover_name
        self.endpoint = endpoint
        self.restaurants = []
        self._go_download_restaurants()

        # assume cafe is closed and check if it indeed is by checking the restaurants
        # TODO: Scrape site for hours instead
        self.is_closed = True
        for r in self.restaurants:
            # if there is at least 1 restaurant that is not closed,
            # the caf is not closed
            if not r.is_closed():
                self.is_closed = False

    def _go_download_restaurants(self):
        page_bytes = request.urlopen(self.CAFE_BASE_URL + self.endpoint)
        soup = BeautifulSoup(page_bytes, 'html.parser')

        """
         here we will get all the cafeterias
        """
        #
        # The target div path:
        # view-content -> views-table
        tables = soup.find_all('table')

        for table in tables:
            rest_anchor = table.find('caption').find('a')
            rest_name = rest_anchor.text
            caf_rest_endpoint = rest_anchor.get('href')

            rest = Restaurant(rest_name, caf_rest_endpoint)
            self.restaurants.append(rest)

    def __str__(self):
        output = ""
        output += 'Cafe: ' + self.cover_name

        if self.is_closed:
            output += ' CLOSED\n'
            return output

        # each restaurant
        for r in self.restaurants:
            if not r.is_closed():
                output += '\n' + str(r)

        return output

    def __repr__(self):
        return self.__str__()
