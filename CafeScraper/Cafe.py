from bs4 import BeautifulSoup
from urllib import request

class Cafe(object):

    CAFE_BASE_URL = 'https://eatatstate.com'

    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
        self.restaurants = []
        self._go_download_restaurants()

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

            rest = Restaurant(rest_name, caf_rest_endpoint, self)
            self.restaurants.append(rest)

    def is_closed(self):
        closed = True
        for r in self.restaurants:
            if not r.is_closed():
                closed = False
        return closed

    def __str__(self):
        output = ""
        output += 'Cafe: ' + self.name

        # each restaurant
        output += str(self.restaurants)
        for r in self.restaurants:
            if not r.is_closed():
                output += str(r)
        return output

    def __repr__(self):
        return self.__str__()

class Restaurant(object):
    CAFE_BASE_URL = 'https://eatatstate.com'

    def __init__(self, name, endpoint, cafe):
        self.name = name
        self.endpoint = endpoint
        self.cafe = cafe
        self.lunch = []
        self.dinner = []
        self.late_night = []
        self.breakfast = []

        self._go_download_options()

    def _go_download_options(self):
        # lets do lunch only for now
        page_bytes = request.urlopen(self.CAFE_BASE_URL + self.endpoint)
        soup = BeautifulSoup(page_bytes, 'html.parser')

        # map the tags to their lists
        menu_list_tags = {'field-field-lunch-menu': self.lunch, 'field-field-dinner-menu': self.dinner,
        'field-field-late-night': self.late_night, 'field-field-breakfast-menu': self.breakfast}

        # this will collect all the menu items
        for menu_tag in menu_list_tags:
            menu = soup.find('div', attrs={'class': menu_tag})

            # not being served
            if menu == None:
                print('Could not find ', menu_tag)
                continue

            # loop over all the menu options and add them to their respective list
            for div in menu.find_all('div', attrs={'class': 'field-item'}):
                name = div.text.strip()
                print(self.cafe.name, self.name, '----->', "'{}'".format(name))

                menu_list_tags[menu_tag].append(name)

    def is_closed(self):
        return len(self.lunch) == 0 and len(self.dinner) == 0 and len(self.late_night) == 0 \
               and len(self.breakfast) == 0

    def __str__(self):
        output = ""
        output += self.name + '\n'

        if self.is_closed():
            output += ' CLOSED'
            return output

        # lunch only for now
        if self.lunch != None:
            output += 'Lunch:\n'
            for item in self.lunch:
                output += item + '\n'

        return output

    def __repr__(self):
        return self.__str__()