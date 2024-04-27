#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common import options, service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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
        "Seria",
        "Thar",
        "Krause",
        "Varut",
    ]

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

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

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item"))
        )
    except:
        driver.close()
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")

    legendary_items = soup.find_all(class_="rarity--Legendary")
    epic_items = soup.find_all(class_="rarity--Epic")
    rare_items = soup.find_all(class_="rarity--Rare")

    available_cards = {
        "Legendary": [],
        "Epic": [],
        "Rare": [],
    }

    for item in legendary_items:
        if item.text in card_list:
            available_cards["Legendary"].append(item.text)

    for item in epic_items:
        if item.text in card_list:
            available_cards["Epic"].append(item.text)

    for item in rare_items:
        if item.text in card_list:
            available_cards["Rare"].append(item.text)

    driver.close()

    return available_cards


if __name__ == "__main__":
    available_cards = scrape()
    if (
        len(available_cards["Legendary"])
        or len(available_cards["Epic"])
        or len(available_cards["Rare"])
    ):
        print("Available Cards:")
        for card in available_cards["Legendary"]:
            print(card)
        for card in available_cards["Epic"]:
            print(card)
        for card in available_cards["Rare"]:
            print(card)
    else:
        print("No Cards Available")
