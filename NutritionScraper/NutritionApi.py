import requests
from string import punctuation
from NutritionScraper.NutritionApiHtmlParser import get_allergens_from_label
from NutritionScraper.NutritionApiHtmlParser import get_serving_size_from_label
from NutritionScraper.NutritionApiHtmlParser import get_ingredients_from_label
from NutritionScraper.NutritionApiHtmlParser import get_nutrition_metrics_from_label
from NutritionScraper.NutritionApiHtmlParser import get_cafeteria_restaurant_numbers
from NutritionScraper.NutritionApiHtmlParser import get_restaurant_food_numbers
from bs4 import BeautifulSoup

class FoodItem(object):

    def __init__(self, name, number, nutrition_facts_html):
        self.name = name
        self.number = number
        self.nutrition_html = nutrition_facts_html
        self.unique_name = self.get_food_unique_name()

        # build label_detail elements
        self.metric_to_value_nutrition_facts = {
            'calories': None,
            'calories_from_fat': None,
            'total_fat': None,
            'saturated_fat': None,
            'cholesterol': None,
            'sodium': None,
            'total_carbohydrate': None,
            'dietary_fiber': None,
            'sugars': None,
            'protein': None
        }

        self.serving_size = None
        self.ingredients = []
        self.allergens = []

        # scrape the label
        self.go_build_food_facts()

    def go_build_food_facts(self):
        # print(self.name, ': ', self.number)
        # print(self.nutrition_html)

        soup = BeautifulSoup(self.nutrition_html, 'html.parser')
        print(self.name)

        self.metric_to_value_nutrition_facts = get_nutrition_metrics_from_label(soup)
        self.serving_size = get_serving_size_from_label(soup)
        self.ingredients = get_ingredients_from_label(soup)
        self.allergens = get_allergens_from_label(soup)

    def get_food_unique_name(self):
        name_no_punctuation = ''.join([ch for ch in self.name if ch not in punctuation])
        name_lowered_split = name_no_punctuation.lower().split()
        name_unique = '_'.join(name_lowered_split)

        # print(name_unique)
        return name_unique

class Cafeteria(object):

    def __init__(self, number, name, restaurant_numbers):
        self.number = number
        self.unique_name = name
        self.restaurant_numbers = restaurant_numbers

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ASP.NET_SessionId=nqdimwgxpqlmflhzjw04mob0; '
                  'CBORD.netnutrition2=NNexternalID=12; '
                  '_ga=GA1.2.935769128.1484451329; _gat=1',
        'Host': 'msutrition.rhs.msu.edu',
        'Referer': 'http://msutrition.rhs.msu.edu/NetNutrition/12',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:43.0) '
                      'Gecko/20100101 Firefox/43.0',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def _go_build_restaurant(self, api):
        # http://msutrition.rhs.msu.edu/NetNutrition/12/Menu/SelectMenu
        CAFETERIA_MENU_FOR_STATION_ENDPOINT_POST = '/Menu/SelectMenu'

        # print(self.restaurant_numbers)

        for rest_number in self.restaurant_numbers:
            rest_menu_page_response = requests.post(
                url=NutritionApi.NUTRITION_API_BASE_URL + CAFETERIA_MENU_FOR_STATION_ENDPOINT_POST,
                data={'menuOid': rest_number},
                headers=NutritionApi.headers)

            json_html_item_key = 'panels'
            page_html_to_scrape = [d for d in rest_menu_page_response.json().get(json_html_item_key)
                            if d['id'] == 'itemPanel'].pop()['html']

            # print(page_html_to_scrape)

            # print(rest_number)
            food_number_and_name_tups = get_restaurant_food_numbers(page_html_to_scrape)

            if rest_number not in api.restaurants:
                restaurant = Restaurant(rest_number)
                restaurant.go_build_fooditems(api, food_number_and_name_tups)
                api.restaurants.append(restaurant)

            # input('Press enter to process the next Restaurant')


class Restaurant(object):

    def __init__(self, number):
        self.number = number
        self.food_numbers = []

    def go_build_fooditems(self, api, food_number_and_name_tups):
        FOOD_ITEM_NUTRITION_FACTS_ENDPOINT_POST = "/NutritionDetail/ShowItemNutritionLabel"
        print('Building food items in restaurant #', self.number)

        for food_number, food_name in food_number_and_name_tups:

            rest_menu_page_response = requests.post(
                url=NutritionApi.NUTRITION_API_BASE_URL + FOOD_ITEM_NUTRITION_FACTS_ENDPOINT_POST,
                data={'detailOid': food_number},
                headers=NutritionApi.headers)

            label_html = rest_menu_page_response.content.decode(rest_menu_page_response.apparent_encoding)

            # use this as a way of reducing the number of calls to the api
            if food_number not in api.food_items:
                api.food_items.append(FoodItem(food_name, food_number, label_html))

            self.food_numbers.append(food_number)

            # input("Press enter to view the next food item")


class NutritionApi(object):

    # TODO: Change this from being hardcoded to being
    # srcaped in-case they change

    '''
    shaw': None, 'gallery': None, 'landon': None, 'case': None,
            'brody': None, 'akers': None, 'holmes': None, 'holden': None, 'wilson':
    '''

    cafe_number_to_name = {
        1: ('Heritage Commons', 'landon'),
        2: ('Brody Square', 'brody'),
        3: ('South Pointe', 'case'),
        4: ('Holden Dining', 'holden'),
        5: ('Wilson Dining', 'wilson'),
        6: ('The Gallery', 'gallery'),
        # 7: 'Riverwalk Market',
        8: ('The Vista', 'shaw'),
        9: ('Holmes Dining', 'holmes'),
        10: ('The Edge', 'akers')
        # 11: "Sparty's",
        # 12: 'Daily Deli',
        # 13: 'Daily Salad Bar',
        # 14: 'Daily Baked Goods'
    }

    REAL_HOST = 'http://msutrition.rhs.msu.edu/NetNutrition/12'
    MOCK_HOST = 'http://localhost:8080/NetNutrition/12'
    NUTRITION_API_BASE_URL = MOCK_HOST

    # TODO: change from hardcode to replicating dryscrape session
    # headers to prevent from outdated values
    # headers = dict([item.strip().split(': ') for item in headers.replace("'", '').split('-H ')[1:]]) # firefox header parse
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5',
     'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'Cookie': 'ASP.NET_SessionId=nqdimwgxpqlmflhzjw04mob0; CBORD.netnutrition2=NNexternalID=12; _ga=GA1.2.935769128.1484451329',
     'Host': 'msutrition.rhs.msu.edu', 'Referer': 'http://msutrition.rhs.msu.edu/NetNutrition/12',
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:43.0) Gecko/20100101 Firefox/43.0',
     'X-Requested-With': 'XMLHttpRequest'}

    def __init__(self):
        self.cafeterias = []
        self.food_items = []
        self.restaurants = []

    def get_cafeteria_restaurant_nutrition(self):
        CAFETERIA_OPEN_RESTAURANTS_ENDPOINT_POST = '/Unit/SelectUnitFromChildUnitsList'
        json_html_item_key = 'panels'

        for cafe_number in NutritionApi.cafe_number_to_name:

            print('Working on cafe number', cafe_number, ' Name = ', NutritionApi.cafe_number_to_name[cafe_number])
            # crawl each cafeteria
            req_cafeteria_station_page = requests.post(
                NutritionApi.NUTRITION_API_BASE_URL + CAFETERIA_OPEN_RESTAURANTS_ENDPOINT_POST,
                data = {'unitOid': cafe_number},
                headers=NutritionApi.headers)

            page_html_to_scrape = [d for d in req_cafeteria_station_page.json().get(json_html_item_key)
                            if d['id'] == 'menuPanel'].pop()['html']

            restaurant_numbers = get_cafeteria_restaurant_numbers(page_html_to_scrape, only_today=True)

            cafe = Cafeteria(cafe_number, NutritionApi.cafe_number_to_name[cafe_number][1], restaurant_numbers)
            cafe._go_build_restaurant(self)

            self.cafeterias.append(cafe)
