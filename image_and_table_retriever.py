import os
import re
import io
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_images_and_tables(response, html_chunk, html_directory, paper_short_name, output_dir="retrieved_content"):
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/tables", exist_ok=True)
    os.makedirs(f"{output_dir}/answers", exist_ok=True)

    soup = BeautifulSoup(html_chunk, "html.parser")
    base_url = "https://www.sciencedirect.com"

    # Extract and save images
    images = soup.find_all("img")
    for i, img in enumerate(images, start=1):
        img_url = img.get("src")
        if not img_url:
            continue

        img_url = urljoin(base_url, img_url)
        img_extension = os.path.splitext(img_url)[-1]  # Preserve original extension
        img_name = f"{paper_short_name}_im{i}{img_extension}"

        try:
            img_path = os.path.join(html_directory, os.path.basename(img_url))
            if os.path.exists(img_path):
                with open(img_path, "rb") as file:
                    img_data = file.read()
                
                with open(f"{output_dir}/images/{img_name}", "wb") as f:
                    f.write(img_data)
                print(f"Saved image: {img_name}")
            else:
                print(f"Image not found locally: {img_url}")
        except Exception as e:
            print(f"Failed to save image {img_name}: {str(e)}")

    # Extract and save tables
    tables = soup.find_all("table")
    for i, table in enumerate(tables, start=1):
        table_html = str(table)
        try:
            df = pd.read_html(io.StringIO(table_html), flavor='lxml')[0]
            table_name = f"{paper_short_name}_table_{i}.csv"
            df.to_csv(f"{output_dir}/tables/{table_name}", index=False)
            print(f"Saved table: {table_name}")
        except Exception as e:
            print(f"Could not parse table {i}: {e}")
    
    
    text_name = f"{paper_short_name}_query_response.txt"
    response_file_path = os.path.join(output_dir, "answers", text_name)
    with open(response_file_path, 'w', encoding='utf-8') as f:
        f.write(response)
    # store the test in the folder:  os.makedirs(f"{output_dir}/answers", exist_ok=True)
    #with the name text_name = paper_short_name


