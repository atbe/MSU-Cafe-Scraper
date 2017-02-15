from NutritionScraper import db
import unittest
import json

class NutritionDatabaseTests(unittest.TestCase):
	def testKeywordBuilderFromName(self):
		col = db.MSUCafeDB('foods')

		json_data = ""
		with open('menus.json') as fp:
			json_data = json.loads(fp.read())

		all_foods = []
		for caf in json_data:
			for rest in caf['restaurants']:
				all_foods.extend(rest['breakfast'])
				all_foods.extend(rest['lunch'])
				all_foods.extend(rest['dinner'])
				all_foods.extend(rest['late_night'])

		results = []
		found,not_found = 0,0
		for food_name in all_foods:
			result = col.SearchForFoodItem(food_name, same_keyword_length=False)
			if result != None:
				results.append((food_name, result['name']))
				found += 1
			else:
				results.append((food_name, None))
				not_found += 1

		for result in results:
			print(result)

		print('Found: ', found, 'Not found ', not_found)


