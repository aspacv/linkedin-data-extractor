# ============================================================
# LinkedIn Data Extractor
# ============================================================
# A Python tool to extract public LinkedIn profile data.
# Built with Selenium, BeautifulSoup, and Pandas.
# ============================================================

import time
import json
import csv
import argparse
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd

class LinkedInScraper:
    def __init__(self, config):
        self.config = config
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        if self.config.get("headless", True):
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def _human_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    def scrape_profile(self, url):
        self.driver.get(url)
        self._human_delay(2, 4)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "top-card-layout"))
            )
        except:
            return None

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        name = soup.find("h1", class_="top-card-layout__title")
        headline = soup.find("div", class_="top-card-layout__headline")
        location = soup.find("span", class_="top-card-layout__second-subline")

        experience_section = soup.find("section", id="experience-section")
        experiences = []
        if experience_section:
            for item in experience_section.find_all("li"):
                title = item.find("span", class_="mr1")
                company = item.find("span", class_="t-14")
                if title:
                    experiences.append({
                        "title": title.text.strip(),
                        "company": company.text.strip() if company else ""
                    })

        education_section = soup.find("section", id="education-section")
        education = []
        if education_section:
            for item in education_section.find_all("li"):
                school = item.find("span", class_="mr1")
                if school:
                    education.append(school.text.strip())

        return {
            "name": name.text.strip() if name else "",
            "headline": headline.text.strip() if headline else "",
            "location": location.text.strip() if location else "",
            "experience": experiences,
            "education": education
        }

    def close(self):
        self.driver.quit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="LinkedIn profile URL")
    parser.add_argument("--file", help="File containing list of URLs")
    args = parser.parse_args()

    config = json.load(open("config.json"))
    scraper = LinkedInScraper(config)

    if args.url:
        data = scraper.scrape_profile(args.url)
        if data:
            df = pd.DataFrame([data])
            df.to_csv("output/profile_data.csv", index=False)
            print("[+] Data saved to output/profile_data.csv")
        else:
            print("[!] Failed to scrape profile")

    scraper.close()

if __name__ == "__main__":
    main()
