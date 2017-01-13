# MSU-Cafe-Scraper
Fun little model which will help build a voting system for my universities cafeteria menu.

# Summary

This project provides a simple Python web scraper that collects data from [eatatstate.com](https://eatatstate.com/menus) and provides a clean Python object oriented model to represent the Cafeterias and Restaurants here at MSUs dining halls.

Also provided is a tiny [Golang](https://golang.org/) web-server that can serve up the content that was scraped. It isn't the most idiomatic REST api but it gives you a starting point if you wanted to write something fun.

So essentially you have a scraper and a server all in one package that you can clone and run right away and have the MSU cafeteria data served up for you on a platter. Now you can reuse that data however you like or extend the scraper to include even more data about the cafeteria!

# How the data is structured

So the scraper has 3 very important data structures which assist it in the collection:

- [Scraper](https://github.com/atbe/MSU-Cafe-Scraper/blob/master/CafeScraper/Scraper.py): The Scraper class represents the entry point for the collection. Instantiation a scraper will begin the scraping process. 
- [Cafeteria](https://github.com/atbe/MSU-Cafe-Scraper/blob/master/CafeScraper/Cafe.py): This represents a [single cafeteria](https://eatatstate.com/menus/brody) here on campus. A cafeteria holds any number of restaurants and is either open or closed. The scraper will return all the cafeterias it can find. An example of a cafeteria is the Snyder Phillips Dining Hall Cafeteria.
- [Restaurant](https://github.com/atbe/MSU-Cafe-Scraper/blob/master/CafeScraper/Restaurant.py): A restaurant is a [station in the cafeteria](https://eatatstate.com/menus/brody/brody-dining-boiling-pointfriday-january-13-2017) that serves some food. Each restaurant serves four meals: breakfast, lunch, dinner, and late-night. These may or may not be available on certain days. The restaurant object has a list of items being offered during each meal.

# 3rd party libraries used

- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Used for the data collection and scraping.

# Sample Cafeteria JSON Output

```
{
    "cover_name": "The Gallery at Snyder/Phillips Menus",
    "endpoint": "/menus/gallery",
    "is_closed": false,
    "restaurants": [
      {
        "breakfast": [
          "Continental Breakfast"
        ],
        "dinner": [
          "Chocolate Blasters",
          "Cheesecake",
          "Assorted Cookies"
        ],
        "endpoint": "/menus/gallery/gallery-dining-blissfriday-january-13-2017",
        "is_closed": false,
        "late_night": [
          "Assorted Cookies"
        ],
        "lunch": [
          "Chili Chocolate Cake",
          "Assorted Cookies"
        ],
        "name": "Bliss"
      },
      {
        "breakfast": [],
        "dinner": [
          "Cheeseburgers",
          "Grilled Chicken Breasts",
          "Fried Chicken Patties",
          "Buffalo Chicken",
          "Fried Fish",
          "Fries"
        ],
        "endpoint": "/menus/gallery/gallery-dining-brimstone-grillemonday-january-9-2017",
        "is_closed": false,
        "late_night": [],
        "lunch": [
          "Cheeseburgers",
          "Grilled Chicken Breasts",
          "Fried Chicken Patties",
          "Buffalo Chicken",
          "Fried Fish",
          "Fries"
        ],
        "name": "Brimstone Grille"
      },
      {
        "breakfast": [],
        "dinner": [
          "Caprese Pizza",
          "Pepperoni Pizza",
          "Cheese Breadsticks",
          "Deli Bar"
        ],
        "endpoint": "/menus/gallery/gallery-dining-ciaofriday-january-13-2017",
        "is_closed": false,
        "late_night": [
          "Pepperoni Pizza",
          "Cheese Pizza",
          "Deli Bar"
        ],
        "lunch": [
          "Cheesy Bacon Pizza",
          "Pepperoni Pizza",
          "Cheese Pizza",
          "Deli Bar"
        ],
        "name": "Ciao"
      },
      {
        "breakfast": [
          "Hard Boiled Eggs",
          "Waffles",
          "Breakfast Sausage Quiche",
          "Cheesy Ranch Hash Browns",
          "Cheddar Sausage Links",
          "Vegetarian Sausage",
          ".",
          "Made to Order Omelets & Fried Eggs"
        ],
        "dinner": [
          "Seared Fresh Fish w/ Ginger Butter",
          "Brown Rice Pilaf w/ Pecans",
          "Asian Vegetable Blend"
        ],
        "endpoint": "/menus/gallery/gallery-dining-latitudesfriday-january-13-2017",
        "is_closed": false,
        "late_night": [],
        "lunch": [
          "Aromatic Rice",
          "Green Beans & Tomatoes"
        ],
        "name": "Latitudes"
      },
      {
        "breakfast": [],
        "dinner": [
          "Meatballs & Pomodoro",
          "Garlic Breadsticks",
          "Garden",
          "Black Bean & Corn Quesadilla"
        ],
        "endpoint": "/menus/gallery/gallery-dining-new-traditionsfriday-january-13-2017",
        "is_closed": false,
        "late_night": [],
        "lunch": [
          "Chicken Noodle Stroganoff",
          "Garlic Cheddar Biscuits",
          "Garden",
          "3 Sisters Casserole",
          "Mexican Rice"
        ],
        "name": "New Traditions"
      },
      {
        "breakfast": [
          "Continental Breakfast"
        ],
        "dinner": [

          "Hearty Grain Soup"
        ],
        "endpoint": "/menus/gallery/gallery-dining-bergfriday-january-13-2017",
        "is_closed": false,
        "late_night": [
          "House Salad Bar"
        ],
        "lunch": [
          "Hearty Grain Soup"
        ],
        "name": "The Berg"
      }
    ],
    "unique_name": "gallery"
}
```