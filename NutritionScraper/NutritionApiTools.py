from bs4 import BeautifulSoup
from datetime import date
import time

def get_cafeteria_restaurant_numbers(html_page, only_today=False):

    soup = BeautifulSoup(html_page, 'html.parser')

    target_day_table_rows = []
    # sample from html: 'Friday, January 13, 2017'
    if only_today:
        today_str_match = date.today().strftime("%A, %B %d, %Y")
        today_str_match = "Monday, January 16, 2017"

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

def get_nutrition_metrics_from_label(soup):
    metric_to_value_nutrition_facts = {}

    # calories from fat is weird
    calories_from_fat_html_element = soup.find('td', attrs={'class': 'cbo_nn_SecondaryNutrient'})
    if calories_from_fat_html_element == None:
        calories_from_fat_html_element = soup.find('span', attrs={'class': 'cbo_nn_LabelPrimaryDetailIncomplete'})

    # still be careful
    if calories_from_fat_html_element != None:
        metric_to_value_nutrition_facts['calories_from_fat'] = \
            str(calories_from_fat_html_element.get_text())
    else:
        print('ERROR: Error finding nutrition label name. More info:\n', calories_from_fat_html_element)

    # handle all other metrics
    for label_detail_td in soup.find_all('td', attrs={'class': 'cbo_nn_LabelBorderedSubHeader'}):

        label_key = label_detail_td.find('td', attrs={'class': 'cbo_nn_LabelDetail'})
        if label_key == None:
            continue
        label_key = '_'.join(label_key.find('font').get_text().strip(':').lower().split())

        # print(label_detail_td)

        label_font_element = label_detail_td.find(attrs={'class': 'cbo_nn_SecondaryNutrient'})
        if label_font_element == None:
            # TODO: investigate detail incomplete
            label_font_element = label_detail_td.find(attrs={'class': 'cbo_nn_LabelPrimaryDetailIncomplete'})

        if label_font_element != None:
            label_value = ' '.join(label_font_element.get_text().strip().split())
        else:
            print('ERROR: Error finding nutrition label value. More info:\n', label_detail_td)
        # print(label_value)

        metric_to_value_nutrition_facts[label_key] = label_value

    return metric_to_value_nutrition_facts

def get_serving_size_from_label(soup):

    # serving size
    #
    serving_size_text_bar = soup.find('td', attrs={'class':'cbo_nn_LabelBottomBorderLabel'}).get_text()
    # sample split: "['Serving', 'Size:', '4oz', '(144g)']"
    return serving_size_text_bar.split()[2]

def get_ingredients_from_label(soup):
    ingredients_span = soup.find(attrs={'class':'cbo_nn_LabelIngredients'})
    if ingredients_span == None:
        return []

    ingredients_list = []
    temp_ingredient = ""
    ignore_commas = False
    for ch in ingredients_span.get_text().strip():
        # skip spaces between ingredients
        if ch == ' ' and len(temp_ingredient) == 0:
            continue

        temp_ingredient += ch
        if ch == '(':
            ignore_commas = True
        elif ch == ')':
            ignore_commas = False

        if ch == ',' and not ignore_commas:
            temp_ingredient = ' '.join(temp_ingredient.strip(',').split())
            ingredients_list.append(temp_ingredient)
            temp_ingredient = ""
    if len(temp_ingredient) > 0:
        ingredients_list.append(temp_ingredient)

    # for i in ingredients_list:
    #     print("'", i, "'")

    return ingredients_list

def get_allergens_from_label(soup):
    allergens_span = soup.find(attrs={'class':'cbo_nn_LabelAllergens'})

    # if food does not contain allergens
    if allergens_span == None:
        return []

    allergens_list = [a.strip(',') for a in allergens_span.get_text().split()]

    # for a in allergens_list:
    #     print("'", a, "'")

    return allergens_list

def build_keywords_from_name(name):
    keywords = []
    for word in name.split():
        keywords.append(
            str(''.join([ch for ch in word if ch.isalnum()])).lower())
    return keywords
