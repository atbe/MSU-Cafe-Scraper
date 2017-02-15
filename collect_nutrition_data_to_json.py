from NutritionScraper.NutritionApi import NutritionApi
from NutritionScraper.NutritionApi import FoodItem
import json
import pickle
import pdb
import traceback

def collect_backup_and_dump():

    '''
    Get the new json
    '''
    try:
        api = NutritionApi()
        api.get_cafeteria_restaurant_nutrition()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        pdb.set_trace()

    # with open('pickle_save.pickle', 'wb') as fd:
    #     pickle.dump(api, fd)
    #     print('Pickled!')

    '''
    Get the new json
    '''


    json_dump = json.dumps(api, default=lambda c: c.__dict__, sort_keys=True)

    '''
    Distribute the new json
    '''
    with open('food_menus.json', 'w') as fp:
        print(json_dump, file=fp)

#     sample = \
# """
# <div id="nutritionLabel" class="cbo_nn_NutritionLabelDiv">
# <table class='cbo_nn_NutritionLabelTable' cellpadding='0' cellspacing='0' style='width:100%;'><tr><td><table width='100%'><tr><td class='cbo_nn_LabelHeader'>Scrambled Eggs</td><td style='text-align:right;'><button id='close' name='close' type='button' class='cbo_nn_closeButton'  onclick="javascript:closeNutritionDetailPanel();" title='Close this panel'><img src='../../images/buttons/close.png' alt='Close'/></button></td></tr></table></td></tr><tr><td class='cbo_nn_LargeLabelHeader'>Nutrition Information</td></tr><tr><td class='cbo_nn_LabelBottomBorderLabel'>Serving Size:&nbsp;4oz&nbsp;(144g)</td></tr><tr><td class='cbo_nn_LabelAmountServed'>Amount Per Serving</td></tr><tr><td class='cbo_nn_LabelBorderedSubHeader' style='white-space:nowrap;'><table style='width:100%;' cellpadding='0' cellspacing='0'><tr><td class='cbo_nn_LabelDetail'><font style='font-weight: bold;'>Calories:</font>&nbsp;&nbsp;<span class='cbo_nn_SecondaryNutrient'>235</span></td><td class='cbo_nn_SecondaryNutrient'>Calories from Fat:&nbsp;&nbsp;<span class='cbo_nn_SecondaryNutrient'>153</span></td></tr></table></td></tr><tr><td align='right' class='cbo_nn_LabelDailyValue'>% Daily Value</td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td colspan='2' class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:bold;'>Total Fat:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;17&nbsp;Gram</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>26%</td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td width='10px'>&nbsp;</td><td class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:normal;'>Saturated Fat:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;5&nbsp;Gram</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>24%</td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td colspan='2' class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:bold;'>Cholesterol:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;580&nbsp;MG</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>193%</td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td colspan='2' class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:bold;'>Sodium:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;700&nbsp;MG</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>29%</td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td colspan='2' class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:bold;'>Total Carbohydrate:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;3&nbsp;Gram</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>1%</td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td width='10px'>&nbsp;</td><td class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:normal;'>Dietary Fiber:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;0&nbsp;Gram</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>0%</td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td width='10px'>&nbsp;</td><td class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:normal;'>Sugars:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;0&nbsp;Gram</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'></td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' cellpadding='0' cellspacing='0'><tr><td colspan='2' class='cbo_nn_LabelBorderedSubHeader'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td style='width:70%; padding-left: 20px'><table cellpadding='0' cellspacing='0' style='width:100%;'><tr><td class='cbo_nn_LabelDetail' style='width:*'><font style='font-weight:bold;'>Protein:</font></td><td><font class='cbo_nn_SecondaryNutrient'>&nbsp;17&nbsp;Gram</font></td></tr></table></td><td style='width:30%;' align='right' class='cbo_nn_LabelLeftPaddedDetail'>33%</td></tr></table></td></tr></table></td></tr><tr><td><table style='width:100%;' cellpadding='0' cellspacing='0' class='cbo_nn_LabelSecondaryTable'><tr><td class='cbo_nn_SecondaryNutrientLabel'>Vitamin A:<span class='cbo_nn_SecondaryNutrient'>&nbsp;8%</span></td><td class='cbo_nn_SecondaryNutrientSpacer'><img src='../../images/bullet_gray.gif' alt=''/></td><td class='cbo_nn_SecondaryNutrientLabel'>Vitamin C:<span class='cbo_nn_SecondaryNutrient'>&nbsp;0%</span></td></tr><tr><td class='cbo_nn_SecondaryNutrientLabel'>Calcium:<span class='cbo_nn_SecondaryNutrient'>&nbsp;4%</span></td><td class='cbo_nn_SecondaryNutrientSpacer'><img src='../../images/bullet_gray.gif' alt=''/></td><td class='cbo_nn_SecondaryNutrientLabel'>Iron:<span class='cbo_nn_SecondaryNutrient'>&nbsp;6%</span></td></tr></table></td></tr><tr><td><table cellpadding='0' cellspacing='0'><tr><td><span class='cbo_nn_LabelIngredientsBold'>Ingredients:</span><span class='cbo_nn_LabelIngredients'>Whole Liquid Eggs(Whole Eggs, Citric Acid, 0.15% Water),&nbsp;Vegetable and Olive Oil Blend(Soybean, Canola, And Olive Oils),&nbsp;Coarse Sea Salt</span></td></tr></table></td></tr><tr><td><table cellpadding='0' cellspacing='0'><tr><td><span class='cbo_nn_LabelAllergensBold'>Contains:</span><span class='cbo_nn_LabelAllergens'>Eggs</span></td></tr></table></td></tr></table>
# </div>"""
#
#     f = FoodItem('cake', 1, sample)


if __name__ == '__main__':
    collect_backup_and_dump()
