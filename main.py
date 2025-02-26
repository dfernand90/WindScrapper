import os
from llm_web_scrapper import llm_web_scraper

# Define root folder path
root_folder = "C:\\Trondheim conference\\papers\\papers_aerodynamic\\"

# Get all subfolders in the root folder (except for the 'raw' folder)
subfolders_in_root_folder = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f)) and f != 'raw']

# Query to use in the scraper
query = "what are the aerodynamic force coefficients?"

# Iterate through each subfolder in the root folder
for subfolder in subfolders_in_root_folder:
    subfolder_path = os.path.join(root_folder, subfolder)
    
    # Find the HTML file and its corresponding "_files" folder in each subfolder
    html_file_path = None
    html_assets_path = None
    
    # Search for the HTML file and its assets folder within the subfolder
    for item in os.listdir(subfolder_path):
        item_path = os.path.join(subfolder_path, item)
        if item.endswith(".html"):
            html_file_path = item_path
            html_assets_path = os.path.join(subfolder_path, item.replace(".html", "_files"))
            break

    # Check if both the HTML file and assets folder exist
    if html_file_path and os.path.exists(html_assets_path):
        print(f"Processing: {html_file_path}")
        # Call the web scraper with the found paths and the query
        llm_web_scraper("llama3:8b", subfolder_path, html_assets_path, query)
    else:
        print(f"Skipping {subfolder}: HTML file or assets folder not found.")