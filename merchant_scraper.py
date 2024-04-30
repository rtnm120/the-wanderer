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
        "legendary": [],
        "epic": [],
        "rare": [],
        "legendary_rapport": [],
        "epic_rapport": [],
    }

    for item in legendary_items:
        if item.text in card_list:
            available_cards["legendary"].append(item.text)

        if item.text not in card_list and item.text != "Squid":
            available_cards["legendary_rapport"].append(item.text)

    for item in epic_items:
        if item.text in card_list:
            available_cards["epic"].append(item.text)

        if item.text not in card_list:
            available_cards["epic_rapport"].append(item.text)

    for item in rare_items:
        if item.text in card_list:
            available_cards["rare"].append(item.text)

    driver.close()

    return available_cards


if __name__ == "__main__":
    available_cards = scrape()
    if (
        len(available_cards["legendary"])
        or len(available_cards["epic"])
        or len(available_cards["rare"])
    ):
        print("Available Cards:")
        for card in available_cards["legendary"]:
            print(card)
        for card in available_cards["epic"]:
            print(card)
        for card in available_cards["rare"]:
            print(card)
    else:
        print("No Cards Available")