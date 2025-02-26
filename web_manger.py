import os
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def download_webpage(url_or_doi, save_folder):
    """
    Downloads a webpage or DOI and saves it to a folder using Selenium for dynamic content.

    Args:
        url_or_doi (str): The URL or DOI to download.
        save_folder (str): The folder to save the downloaded files.

    Returns:
        tuple: (html_path, html_assets)
    """
    # Convert DOI to URL if needed
    if url_or_doi.startswith("10."):
        url_or_doi = f"https://doi.org/{url_or_doi}"

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run without GUI
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Fetch the page
    driver.get(url_or_doi)
    html_source = driver.page_source
    driver.quit()

    # Parse URL to create filenames
    parsed_url = urlparse(url_or_doi)
    page_name = parsed_url.path.strip("/").replace("/", "_") or "index"
    page_name = page_name[:50]  # Limit filename length
    html_filename = f"{page_name}.html"
    assets_folder = os.path.join(save_folder, f"{page_name}_files")

    # Ensure directories exist
    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(assets_folder, exist_ok=True)

    # Save HTML file
    html_path = os.path.join(save_folder, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_source)

    # Extract and save assets
    soup = BeautifulSoup(html_source, "html.parser")
    for tag in soup.find_all(["img", "script", "link"]):
        attr = "src" if tag.name in ["img", "script"] else "href"
        if tag.has_attr(attr):
            asset_url = tag[attr]
            asset_name = os.path.basename(urlparse(asset_url).path)

            if asset_name:
                asset_path = os.path.join(assets_folder, asset_name)
                try:
                    asset_resp = requests.get(asset_url)
                    if asset_resp.status_code == 200:
                        with open(asset_path, "wb") as f:
                            f.write(asset_resp.content)
                except:
                    pass  # Ignore failed assets

    return html_path, assets_folder

if __name__ == "__main__":
    # Example usage
    save_dir = "C:\\Trondheim conference\\papers\\papers_aerodynamic"
    url = "https://medium.com/@jerryjliu98/how-unstructured-and-llamaindex-can-help-bring-the-power-of-llms-to-your-own-data-3657d063e30d"  # Replace with your URL or DOI
    doi = "10.1016/j.jweia.2017.02.011"
    html_path, html_assets = download_webpage(url, save_dir)

    print(f"HTML file saved at: {html_path}")
    print(f"Assets folder: {html_assets}")