from bs4 import BeautifulSoup
from urllib import request
from itertools import zip_longest

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

        self.is_closed = self.check_if_closed()

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
                if single_food_name_str.lower() == 'closed' or '\n' in single_food_name_str or \
				                'hours' in single_food_name_str.lower():
                    continue

                #print(self.cafe.name, self.name, '----->', "'{}'".format(name))

                # append this food name to the list
                time_segment_to_collection_dict[time_segment_name_str].append(single_food_name_str)

    def check_if_closed(self):
        return len(self.lunch) == 0 and len(self.dinner) == 0 and len(self.late_night) == 0 \
               and len(self.breakfast) == 0

    def __str__(self):
        output = ""
        output += "{:^180}\n".format(self.name)

        # check if is closed first
        if self.check_if_closed():
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