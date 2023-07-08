import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

webdriver_path = "path/to/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--headless")  

service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

years = [2015, 2014, 2013, 2012, 2011, 2010]
data = []

for year in years:
    url = f"https://www.scrapethissite.com/pages/ajax-javascript/#{year}"
    driver.get(url)

    time.sleep(5)

    table_body = driver.find_element(By.ID, "table-body")
    films = table_body.find_elements(By.CLASS_NAME, "film")

    for film in films:
        title = film.find_element(By.CLASS_NAME, "film-title").text.strip()
        nominations = int(film.find_element(By.CLASS_NAME, "film-nominations").text.strip())
        awards = int(film.find_element(By.CLASS_NAME, "film-awards").text.strip())
        best_picture_element = film.find_element(By.CLASS_NAME, "film-best-picture")
        best_picture = bool(best_picture_element.find_elements(By.TAG_NAME, "i")) 
        film_data = {
            "year": year,
            "title": title,
            "nominations": nominations,
            "awards": awards,
            "best_picture": best_picture
        }
        data.append(film_data)

# Export the scraped data to a CSV file
csv_filename = "scraped_data.csv"
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["Year", "Title", "Nominations", "Awards", "Best Picture"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([
        {
            "Year": film["year"],
            "Title": film["title"],
            "Nominations": film["nominations"],
            "Awards": film["awards"],
            "Best Picture": film["best_picture"]
        }
        for film in data
    ])

print(f"Data exported to {csv_filename}")

# Quit the WebDriver
driver.quit()
