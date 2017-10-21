import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time  # used for sleeping
import datetime
import random
import re

# mute the driver in driver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

# Adds ublock to driver to prevent their bitcoin miner from eating all your CPU
# make sure the file is in your local directory
chrome_options.add_extension('uBlock-Origin_v1.14.12.crx')

# used for keeping track of time
countdown = 3600*48  # 24 hours. Will end when time runs to 0
countdown_start = countdown

running_time = 0 # time in seconds that the bot has run
schedules = (3600,1820)  # determines next time to schedule bot operation
rates = (3600,1820)  # determines rate of bot operations
hour_count = 0

# increase this amount when you rank up
bet_current = 0;

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

    #Go to webzone.
    driver.get(webzone)
    driver.maximize_window()
    time.sleep(2)

    # click on wheel of winnings link
    xp = "//a[@href='/wheel']"
    driver.find_element_by_xpath(xp).click()
    time.sleep(5)

    # get balance
    if current_balance == 0:
        xp = '//a[@href="/account"]/span[@class="userCredits"]'
        current_balance = int(driver.find_element_by_xpath(xp).text)

    # get bet amount
    webelements = driver.find_elements_by_class_name('mt5')
    bet_current = webelements[-1].text
    bet_current = int(re.sub("\D", "", bet_current)) - 1

    while countdown > 0:
        # close ads if found
        if (len(driver.window_handles) > 1):
            print('\tad detected; closing')
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


        button = driver.find_elements_by_class_name('spinButton')
        if len(button) == 1:
            try:
                button[0].click()
            except:
                driver.quit()
                print("\tcaptcha? Closing and restarting")
                time.sleep(30)
                break

        else:
            print("\tnothing there")


        # wait for the spinner to turn, plus a random delay
        fuzz = random.randint(0, 3)  # fuzz the re-presses up a bit
        time.sleep(8+fuzz)
        countdown -= 8+fuzz
        running_time += 8+fuzz

        if running_time >= schedules[0]:
            # print hourly income
            schedules[0] += rates[0] # update next schedule
            hour_count += 1
            print("it's been an hour; ", hour_count, " operational")

            # obtain and print current balance
            print(driver.find_element_by_xpath('//a[@href="/account"]/span[@class="userCredits"]').text)
            new_balance = int(driver.find_element_by_xpath('//a[@href="/account"]/span[@class="userCredits"]').text)

            # calculate and print profit
            profit = new_balance - current_balance
            print("profit = ",profit)

            # write to log file
            profit_logfile = open(profit_fname, "a")
            profit_logfile.write(str(time.ctime(time.time()))+",\t"+str(new_balance)+",\t"+str(profit)+'\n')
            profit_logfile.close()

            #update current balance
            current_balance = new_balance

        # close ads if found
        if (len(driver.window_handles) > 1):
            print('\tad detected; closing')
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


        if bet_current > 0:
            time.sleep(2)
            print('\tupping bet')
            # click up the bet
            xp = '//*[@id="betSpinUp"]'
            driver.find_element_by_xpath(xp).click()# increase bet
            bet_current -= 1

        # every now and then, wait a few minutes
        if(random.randint(0,100)) == 0:
            fuzz = random.randint(60,180)
            print("\tsleeping for ",fuzz," seconds...")
            time.sleep(fuzz)



        # every once in a while wait a couple hours
        if (random.randint(0, 1500)) == 0:
            fuzz = random.randint(3600*.5, 3600*2) # 1-2 hours
            if (random.randint(0, 3)) == 0:
                fuzz += random.uniform(3600* 5, 3600*7) # 1-2 hours
            print("Taking break for ", fuzz / 3600, " hours...")
            driver.quit()
            time.sleep(fuzz)
            print("Resuming")
            break


