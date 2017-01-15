from bs4 import BeautifulSoup
from datetime import date
import time

def get_cafeteria_restaurant_numbers(html_page, only_today=False):

    soup = BeautifulSoup(html_page, 'html.parser')

    target_day_table_rows = []
    # sample from html: 'Friday, January 13, 2017'
    if only_today:
        today_str_match = date.today().strftime("%A, %B %d, %Y")

        for td in soup.find_all('td', attrs={'class':'cbo_nn_menuCell'}):
            if today_str_match in str(td):
                target_day_table_rows.append(td)
                break

        if len(target_day_table_rows) == 0:
            # TODO Make the 'no data this day' exception
            return []
            raise ValueError
    else:
        target_day_table_rows = list(soup.find_all('td', attrs={'class':'cbo_nn_menuCell'}))

    restaurant_numbers = []
    for td in target_day_table_rows:
        #print(td)
        for anchor in td.find_all('a'):
            # sample onclick value 'javascript:menuListSelectMenu(2724240);' we want 2724240
            onclick_text = anchor.get('onclick')

            left_paran = onclick_text.find('(') + 1
            right_paran = onclick_text.find(')')

            station_id = onclick_text[left_paran : right_paran]
            # print(onclick_text, station_id)

            restaurant_numbers.append(int(station_id))

    # input('Press enter to continue')

    return restaurant_numbers



def get_restaurant_food_numbers(html_page):
    # print(html_page)

    soup = BeautifulSoup(html_page, 'html.parser')

    all_menu_item_td = soup.find_all('td', attrs={'class':'cbo_nn_itemHover'})

    # print(html_page)

    if len(all_menu_item_td) < 1:
        # TODO: Handle when no food available
        print('DEBUG: No food td were found')
        # input('Press enter to continue')
        return []

    food_number_name_tups= []
    for td in all_menu_item_td:
        # sample: 'javascript:t=setTimeout('getItemNutritionLabel(65443088)', 500);' want 65443088
        onhover_text = td.get('onmouseover')
        # print(onhover_text)

        left_paran = onhover_text.rfind('(') + 1
        right_paran = onhover_text.find(')')
        food_number = onhover_text[left_paran : right_paran]

        food_name = td.get_text()

        food_number_name_tups.append( (int(food_number), food_name) )

    # input('Press enter to return the found food numbers')

    return food_number_name_tups



