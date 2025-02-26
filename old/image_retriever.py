from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
import os
import re
import pandas as pd
# Parse the HTML using BeautifulSoup
from bs4 import BeautifulSoup

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


soup = BeautifulSoup(html, "html.parser")

# Create a directory to store images
os.makedirs("downloaded_images", exist_ok=True)

# Create a directory to store images
os.makedirs("downloaded_tables", exist_ok=True)
# Extract all images
images = soup.find_all("img")
for img in images:
    img_url = img.get("src")
    
    # Skip if image URL is not available
    if not img_url:
        continue

    # If the image URL is relative, form the full URL
    if img_url.startswith("/"):
        img_url = "https://www.sciencedirect.com" + img_url

    # Get the image name from URL
    img_name = img_url.split("/")[-1]
    img_name = re.sub(r'[<>:"/\\|?*]', '_', img_name)  # Replace invalid character
    # Download the image
    img_data = requests.get(img_url).content
    with open(f"downloaded_images/{img_name}", "wb") as f:
        f.write(img_data)
    
    print(f"Downloaded image: {img_name}")

### **Extract all tables**
tables = soup.find_all("table")
for i, table in enumerate(tables):
    table_html = str(table)  # Store table as HTML string
    
    # Convert table to a Pandas DataFrame if possible
    try:
        df = pd.read_html(table_html)[0]  # Extract the first table from the list
        table_name = f"table_{i+1}.csv"
        df.to_csv(f"downloaded_tables/{table_name}", index=False)
        print(f"Downloaded table: {table_name}")
    except Exception as e:
        print(f"Could not parse table {i+1}: {e}")

print("All images have been downloaded!")
