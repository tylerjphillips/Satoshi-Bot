import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time  # used for sleeping
import datetime


# mute the driver in driver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

# Adds ublock to driver to prevent their bitcoin miner from eating all your CPU
# make sure the file is in your local directory
chrome_options.add_extension('uBlock-Origin_v1.14.12.crx')

# used for keeping track of time
countdown = 86000  # 24 hours. Will end when time runs to 0
countdown_start = countdown
hour_time = 3550 #3600 # counts up to an hour to give reports
hour_count = -1

# increase this amount when you rank up
bet_amount = 0; # how many times to up the bet
bet_current = bet_amount

current_balance = 0 # amount of balance

# Replace this URL with the unique one they give you
webzone = 'https://faucetgame.com'

while countdown > 0:

    # initialize driver
    driver= webdriver.Chrome(chrome_options=chrome_options)

    # Throttles network just in case
    driver.set_network_conditions(
        offline=False,
        latency=0,  # additional latency (ms)
        download_throughput=60 * 1024,  # maximal throughput
        upload_throughput=30 * 1024)  # maximal throughput

    bet_current = bet_amount #reset the bet

    #Go to webzone.
    driver.get(webzone)
    time.sleep(2)

    # click on wheel of winnings link
    xp = "//a[@href='/wheel']"
    driver.find_element_by_xpath(xp).click()
    time.sleep(5)

    while countdown > 0:
        # close ads if found
        if (len(driver.window_handles) > 1):
            print('ad detected; closing')
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


        button = driver.find_elements_by_class_name('spinButton')
        if len(button) == 1:
            try:
                button[0].click()
            except:
                driver.quit()
                print("captcha? Closing and restarting")
                time.sleep(60)
                break

        else:
            print("nothing there")

        time.sleep(8)
        countdown -= 8
        hour_time += 8
        if(hour_time >= 3600):
            # print hourly income
            hour_time = 0
            hour_count += 1
            print("it's been an hour; ", hour_count, " operational")
            driver.get('https://faucetgame.com/account')
            time.sleep(5)

            xp = '/html/body/div[1]/div[2]/div/div/header/div[1]/div[2]/div/div/div[2]/h5'
            account = driver.find_elements_by_class_name('mt5')

            new_balance = int(account[0].text)
            print("profit = ",new_balance - current_balance)
            current_balance = new_balance

            driver.get('https://faucetgame.com/wheel')
            time.sleep(2)
            # new_balance = int(driver.find_element_by_xpath(xp).text)  # amount of balance
            # print("current balance: ", new_balance)
            # print("profit: ",new_balance - current_balance)
            # current_balance = new_balance

        # close ads if found
        if (len(driver.window_handles) > 1):
            print('ad detected; closing')
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


        if bet_current > 0:
            time.sleep(2)
            print('upping bet')
            # click up the bet
            xp = '//*[@id="betSpinUp"]'
            driver.find_element_by_xpath(xp).click()# increase bet
            bet_current -= 1