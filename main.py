from CafeScraper.Scraper import Scraper
import json

scraper = Scraper()
json_dump = json.dumps(scraper.cafes_dict, default=lambda c: c.__dict__, sort_keys=True)
print(json_dump)

# save to file
with open('menus.json', 'w') as fp:
    print(json_dump, file=fp)

#
#
# for cafe in scraper.cafes:
#     #print(cafe)
#     json_dump = json.dumps(cafe, default=lambda c: c.__dict__)
#     print(json_dump)