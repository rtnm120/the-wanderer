#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def scrape():
    card_list = [
        "Kharmine",
        "Delain Armen",
        "Wei",
        "Azena and Inanna",
        "Balthorr",
        "Vairgrys",
        "Varkan",
    ]

    driver = webdriver.Firefox()
    driver.get("https://lostmerchants.com")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "future-merchants-grid__title"))
    )

    server_region = driver.find_element(By.ID, "severRegion")
    region_select = Select(server_region)
    region_select.select_by_index(2)

    server = driver.find_element(By.ID, "server")
    server_select = Select(server)
    server_select.select_by_index(2)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "item"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    legendary_items = soup.find_all(class_="rarity--Legendary")

    available_cards = []

    for item in legendary_items:
        if item.text in card_list:
            available_cards.append(item.text)

    if len(available_cards) > 0:
        print("Available Cards:")
        for card in available_cards:
            print(card)

    driver.close()


if __name__ == "__main__":
    scrape()