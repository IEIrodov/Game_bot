from selenium import webdriver
import time

chrome_driver_path = "C:\Development\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

#Get cookie click on
cookie = driver.find_element_by_id("cookie")

items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]


timeout = time.time() + 5
five_min = time.time() + 60*5 #5 minutes

while True:
    cookie.click()

    if time.time() > timeout:

        #Get all upgrade <b> tags
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []


        #Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",",""))
                item_prices.append(cost)


        # Dictionary of store items and their prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]


        #Current Cookie Count

        money_element = driver.find_element_by_id("money").text
        if "," in money_element:
            money_element = money_element.replace(",","")
        cookie_count = int(money_element)


        #Upgrades
        affordable_upgrades = {}
        for cost,id in cookie_upgrades.items():
            if cookie_count>cost:
                affordable_upgrades[cost] = id


        #Most expensive afford purchase

        heighest_price_affordable_upgrade = max(affordable_upgrades)
        print(heighest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[heighest_price_affordable_upgrade]

        driver.find_element_by_id(to_purchase_id).click()

        #Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 min stop the bot and check the cookies/second ratio

    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break