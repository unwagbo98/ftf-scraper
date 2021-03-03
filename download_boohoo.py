import time
import json
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='/Users/ugonwagbo/env/ftfScrapper/chromedriver', options=chrome_options)


def click_through_item(url):
    # save main_window
    main_window = driver.current_window_handle
    # open new blank tab
    driver.execute_script("window.open('','_blank');")
    # switch to the new window which is second in window_handles array
    driver.switch_to.window(driver.window_handles[2])
    # open successfully and close
    driver.get(url)

    images = driver.find_elements_by_css_selector('img.productthumbnail')
    for image in images:
        xx = image.get_attribute("data-lgimg")
        y = json.loads(xx)
        print(y["url"])

    # close tab
    driver.close()
    # back to the main window
    driver.switch_to.window(main_window)


def process_item(item):
    colors = item.find_elements_by_css_selector('div.product-swatches > ul > li.product-swatch-item a')
    single_item = item.find_element_by_css_selector('div.product-tile-name > a.name-link')
    num_colors = len(colors)
    if num_colors < 2:
        click_through_item(single_item.get_attribute("href"))
    else:
        for color in colors:
            click_through_item(color.get_attribute("href"))


def click_through_subtitle(url):
    # save main_window
    main_window = driver.current_window_handle
    # open new blank tab
    # driver.execute_script("window.open();")
    driver.execute_script("window.open('','_blank');")
    # switch to the new window which is second in window_handles array
    driver.switch_to.window(driver.window_handles[1])
    # open successfully 
    driver.get(url)
    # scrape items in page        
    # clothing_items = driver.find_elements_by_class_name("name-link")
    clothing_items = driver.find_elements_by_css_selector('#search-result-items > li.grid-tile')
    count = 0
    num_items = 3
    for item in clothing_items:
        if count > num_items - 1:
            break
        process_item(item)
        count += 1
    if count > num_items - 1:
        # close tab
        driver.close()
        # back to the main window
        driver.switch_to.window(main_window)
        return
    # go to next page 
    next_page_link = driver.find_elements_by_css_selector('li.pagination-item.pagination-item-next > a')
    next_page = len(next_page_link) > 0
    while next_page:
        driver.get(next_page_link[0].get_attribute("href"))
        # scrape items in page        
        clothing_items = driver.find_elements_by_class_name("name-link")
        for item in clothing_items:
            if count > num_items - 1:
                break
            process_item(item)
            count += 1
        # go to next page 
        next_page_link = driver.find_elements_by_css_selector('li.pagination-item.pagination-item-next > a')
        next_page = len(next_page_link) > 0

    # close tab
    driver.close()
    # back to the main window
    driver.switch_to.window(main_window)


def main():
    driver.get('https://us.boohoo.com/sitemap')
    accept_btn = driver.find_elements_by_class_name("js-accept-all-button")[0]
    accept_btn.click()
    sitemap = driver.find_elements_by_class_name("primary-content")[0]
    subtitles = driver.find_elements_by_xpath('//*[@id="primary"]/div/div/ul/li/div/h3/a')
    clothes = []

    for subtitle in subtitles:
        print("--------------------" + subtitle.get_attribute("title") + "--------------------")
        click_through_subtitle(subtitle.get_attribute("href"))
    driver.quit()


if __name__ == "__main__":
    main()
