from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os
import pandas as pd

# Set up Selenium WebDriver (update with your ChromeDriver path)
chrome_driver_path = "C:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Update this path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the ScienceDirect article
url = "https://www.sciencedirect.com/science/article/pii/S0141029622010628"
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

# Get the full page source after rendering
html = driver.page_source

# Close Selenium (not needed after fetching HTML)
driver.quit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Create a directory to store images
os.makedirs("force_coefficient_data", exist_ok=True)

# Extract all text content
all_text = soup.get_text()

# Find paragraphs mentioning "force coefficient"
relevant_text = []
for paragraph in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5"]):  # Include headers too
    if "force coefficient" in paragraph.get_text().lower():
        relevant_text.append(paragraph.get_text())

# Extract table data related to force coefficients
tables = soup.find_all("table")
table_data = []
for table in tables:
    if "force coefficient" in table.get_text().lower():
        rows = []
        for row in table.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            rows.append(cells)
        table_data.append(rows)

# Extract and download relevant images
images = soup.find_all("img")
for img in images:
    img_url = img.get("src")
    caption = img.get("alt") or img.get("title")  # Check for captions or alternative text

    if img_url: #and caption and "force coefficient" in caption.lower():
        img_name = img_url.split("/")[-1]
        img_data = requests.get(img_url).content

        with open(f"force_coefficient_data/{img_name}", "wb") as f:
            f.write(img_data)
        
        print(f"Downloaded image: {img_name}")

# Save extracted text to a file
with open("force_coefficient_data/force_coefficient_text.txt", "w", encoding="utf-8") as f:
    for text in relevant_text:
        f.write(text + "\n\n")

# Save table data to CSV
if table_data:
    for idx, table in enumerate(table_data):
        df = pd.DataFrame(table)
        df.to_csv(f"force_coefficient_data/force_coefficient_table_{idx+1}.csv", index=False)

print("Scraping complete! Extracted text, tables, and images related to 'force coefficient'.")
