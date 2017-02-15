from NutritionScraper import NutritionApiTools

import unittest

class NutritionApiToolsTests(unittest.TestCase):

    def testKeywordBuilderFromName(self):
        # input, expected output
        tests = \
            [
                ('Grilled Cheese', {'grilled', 'cheese'}),
                ("Some Food's $outh", {'some', 'foods', 'outh'})
            ]

        for test_input, test_expected_output in tests:
            self.assertSetEqual(test_expected_output,
                                NutritionApiTools.build_keywords_from_name(test_input))
