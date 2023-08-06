import os
import os_tools.LoggerHandler as lh
import os_tools.Tools as tools
import os_tools.FileHandler as fh
import time
import pyautogui

# generate random integer values
from random import seed
from random import randint
from pynput import mouse
from pynput.mouse import Button, Controller

dirs = fh.get_dir_content('/Users/home/Desktop/stock_exchange/icons', False, True, False)
for _dir in dirs:
    if fh.is_dir_empty(_dir):
        fh.remove_dir(_dir)

#
# file_list = [
#     # 'https://www.flaticon.com/free-icon/chart_2361820',
#     #          'https://www.flaticon.com/free-icon/statistics_2058302',
#     #          'https://www.flaticon.com/premium-icon/stock-market_1992042',
#     #          'https://www.flaticon.com/free-icon/dollar_2078717',
#     #          'https://www.flaticon.com/premium-icon/stock_788718?term=stock&page=4&position=15',
#     #          'https://www.flaticon.com/free-icon/stable_2168150?term=stock&page=4&position=71',
#              # 'https://www.flaticon.com/free-icon/stock_2329531',
#              # 'https://www.flaticon.com/premium-icon/graph_2207339?term=stock&page=3&position=46',
#              # 'https://www.flaticon.com/free-icon/capital_2390229',
#              'https://www.flaticon.com/free-icon/trends_2720839?term=stock&page=5&position=23',
#              'https://www.flaticon.com/free-icon/analytic_1870237?term=stock&page=5&position=39',
#              'https://www.flaticon.com/premium-icon/data-analytics_2018981',
#              'https://www.flaticon.com/free-icon/buy_1753641?term=stock&page=5&position=81',
#              'https://www.flaticon.com/free-icon/trends_2720799?term=stock&page=5&position=73',
#              'https://www.flaticon.com/free-icon/stocks_2058175',
#              'https://www.flaticon.com/premium-icon/stock_788750?term=stock&page=6&position=79',
#              'https://www.flaticon.com/free-icon/coffee_2146048',
#              'https://www.flaticon.com/free-icon/business_2078738?term=stock&page=6&position=60',
#              'https://www.flaticon.com/free-icon/stock-market_1753665?term=stock&page=7&position=14',
#              'https://www.flaticon.com/premium-icon/stock-market_1992032?term=stock&page=7&position=18',
#              'https://www.flaticon.com/free-icon/business_2078731?term=stock&page=7&position=20',
#              'https://www.flaticon.com/premium-icon/stock_2153297?term=stock&page=7&position=42',
#              'https://www.flaticon.com/free-icon/bar-chart_1735340?term=stock&page=7&position=63',
#              'https://www.flaticon.com/premium-icon/analysis_2207189',
#              'https://www.flaticon.com/premium-icon/analysis_2207350?term=stock&page=7&position=90',
#              'https://www.flaticon.com/premium-icon/candlestick_2207110?term=stock&page=7&position=80',
#              'https://www.flaticon.com/premium-icon/forex_2723295',
#              'https://www.flaticon.com/premium-icon/research_2723281',
#              'https://www.flaticon.com/premium-icon/money-growth_2723284',
#              'https://www.flaticon.com/premium-icon/stocks_2712109?term=stock&page=8&position=58',
#              'https://www.flaticon.com/premium-icon/coins-stack_2175514',
#              'https://www.flaticon.com/premium-icon/bull-market_2386643?term=stock&page=10&position=77',
#              'https://www.flaticon.com/free-icon/bull-market_2329408',
#              'https://www.flaticon.com/free-icon/bars_1762493?term=stock&page=12&position=6',
#              'https://www.flaticon.com/free-icon/stock-market_2641120?term=stock&page=12&position=64',
#              'https://www.flaticon.com/free-icon/statistics_426483',
#              'https://www.flaticon.com/free-icon/bull_1753552?term=stock&page=13&position=49',
#              'https://www.flaticon.com/free-icon/boxed-line-stocks-graphic_38835?term=stock&page=15&position=66',
#              'https://www.flaticon.com/premium-icon/analytics_998331',
#              'https://www.flaticon.com/free-icon/bull_1606534?term=stock&page=16&position=44',
#              'https://www.flaticon.com/free-icon/bear_1606533',
#              'https://www.flaticon.com/free-icon/stocks_1606566?term=stock&page=17&position=16',
#              'https://www.flaticon.com/premium-icon/stock-market_2202996?term=stock&page=18&position=62',
#              'https://www.flaticon.com/premium-icon/financial-presentation_2272966?term=stock&page=19&position=36',
#              'https://www.flaticon.com/premium-icon/data-analytics_2655831?term=stock&page=23&position=63',
#              'https://www.flaticon.com/premium-icon/data-report_2655724',
#              'https://www.flaticon.com/free-icon/stock_1465936',
#              'https://www.flaticon.com/free-icon/presentation_2695369',
#              'https://www.flaticon.com/premium-icon/analytics_1151312?term=stock&page=24&position=80',
#              'https://www.flaticon.com/premium-icon/hand_1151291',
#              'https://www.flaticon.com/free-icon/buy_1616019?term=stock&page=24&position=76',
#              'https://www.flaticon.com/premium-icon/man-improving-business-graphic-arrow-holding-it-up-for-ascendant-stock_46601?term=stock&page=27&position=34',
#              'https://www.flaticon.com/premium-icon/upstairs_2641951',
#              'https://www.flaticon.com/premium-icon/stocks_1468177?term=stock&page=35&position=3',
#              'https://www.flaticon.com/premium-icon/stock_1662581?term=stock&page=35&position=22',
#              'https://www.flaticon.com/premium-icon/bitcoin_1662577',
#              'https://www.flaticon.com/premium-icon/bear-market_2386689?term=stock%20market&page=1&position=29',
#              'https://www.flaticon.com/premium-icon/trading_2498326?term=stock%20market&page=1&position=78',
#              'https://www.flaticon.com/free-icon/increase_1293045']
#
#
# def hot_key(btn_list):
#     pyautogui.keyDown(btn_list[0])
#
#     time.sleep(1)
#     for i in range(1, len(btn_list)):
#         print("down" + btn_list[i])
#         pyautogui.keyDown(btn_list[i])
#
#     time.sleep(1)
#     for i in range(1, len(btn_list)):
#         print("up" + btn_list[i])
#         pyautogui.keyUp(btn_list[i])
#
#     time.sleep(1)
#     pyautogui.keyUp(btn_list[0])
#
#
# tools.ask_for_input('tell me when u ready: ')
# m = mouse.Controller()
#
#
# time.sleep(2.5)
# counter = 0
# for file in file_list:
#     hot_key(['command', 'l'])
#     pyautogui.write(file)
#     pyautogui.press('enter')
#     time.sleep(4)
#     m.click(Button.left, 1)
#     time.sleep(5)
#     pyautogui.press('left')
#     time.sleep(1)
#     pyautogui.write(str(randint(0, 10000000)) + '_')
#     pyautogui.press('enter')
#     time.sleep(1)
#     # pyautogui.press('enter')
#     # time.sleep(1)
#     counter += 1
#     print("downloaded " + str(counter))
