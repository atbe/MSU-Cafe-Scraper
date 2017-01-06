from bs4 import BeautifulSoup
from urllib import request
from itertools import zip_longest

class Cafe(object):

    CAFE_BASE_URL = 'https://eatatstate.com'

    def __init__(self, name, endpoint):
        self.name = name
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
        output += 'Cafe: ' + self.name

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

class Restaurant(object):
    CAFE_BASE_URL = 'https://eatatstate.com'

    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
        self.lunch = []
        self.dinner = []
        self.late_night = []
        self.breakfast = []

        self._go_download_options()

    def _go_download_options(self):
        # lets do lunch only for now
        page_bytes = request.urlopen(self.CAFE_BASE_URL + self.endpoint)
        soup = BeautifulSoup(page_bytes, 'html.parser')

        # There are 4 meal time segments in a day (in this order)
        # breakfast - lunch - dinner - late-night
        # this mapps the collection for that segment to the unique class name that identifies it in the html
        time_segment_to_collection_dict = {'field-field-lunch-menu': self.lunch, 'field-field-dinner-menu': self.dinner,
        'field-field-late-night': self.late_night, 'field-field-breakfast-menu': self.breakfast}

        # this will collect all the food items for a given time segment and add them to the respective collection
        for time_segment_name_str in time_segment_to_collection_dict:
            menu_time_segment_div = soup.find('div', attrs={'class': time_segment_name_str})

            # this time segment (ex breakfast) is not being served today
            if menu_time_segment_div == None:
                #print('Could not find ', menu_tag)
                continue

            # loop over all the menu options and add them to their respective list
            for single_food_option_div in menu_time_segment_div.find_all('div', attrs={'class': 'field-item'}):
                single_food_name_str = single_food_option_div.text.strip()

                # skip these garbage entries
                # hours is mixed in the same section of the list of their websites
                if single_food_name_str.lower() == 'closed' or '\n' in single_food_name_str or 'hours' in single_food_name_str.lower():
                    continue

                #print(self.cafe.name, self.name, '----->', "'{}'".format(name))

                # append this food name to the list
                time_segment_to_collection_dict[time_segment_name_str].append(single_food_name_str)

    def is_closed(self):
        return len(self.lunch) == 0 and len(self.dinner) == 0 and len(self.late_night) == 0 \
               and len(self.breakfast) == 0

    def __str__(self):
        output = ""
        output += "{:^180}\n".format(self.name)

        # check if is closed first
        if self.is_closed():
            output += ' CLOSED'
            return output

        # print the menus
        output += "{:^50}{:^50}{:^50}{:^50}\n".format('Breakfast', 'Lunch', 'Dinner', 'Late-Night')
        output += "{:^50}{:^50}{:^50}{:^50}\n".format('-'*10, '-'*10, '-'*10, '-'*10)
        # each of these are strings of food names
        for breakfast,lunch,dinner,late_night in zip_longest(self.breakfast, self.lunch, self.dinner, self.late_night):
            output += "{:^50}{:^50}{:^50}{:^50}\n".format(str(breakfast), str(lunch), str(dinner), str(late_night))

        return output

    def __repr__(self):
        return self.__str__()