LLM Web Scraper

Overview

This repository provides a web scraper that processes locally stored HTML files and extracts relevant information using a Large Language Model (LLM). The extracted content includes textual data, images, and tables, which are analyzed to answer specific queries.

Features

Scans subfolders containing HTML documents.

Extracts text from specified HTML tags.

Utilizes a vector-based search to find the most relevant text segments.

Queries an LLM for insights based on extracted content.

Extracts images and tables from the best-matching HTML sections.

Prerequisites

Python 3.10+

Ollama must be installed (Ollama installation guide)

Installation

Clone the repository:

git clone https://github.com/yourusername/llm-web-scraper.git
cd llm-web-scraper

Install the required dependencies:

pip install -r requirements.txt

Usage

Prepare a folder structure with subdirectories containing HTML files and their corresponding asset folders (e.g., example.html and example_files/).

Modify root_folder in the script to point to your HTML data directory.

Adjust the query variable to specify the question you want to ask the LLM.

Run the script:

python main.py

File Structure

llm-web-scraper/
│── llm_web_scraper.py      # Core web scraping logic
│── main.py                 # Entry point for running the scraper
│── image_and_table_retriever.py # Extracts images and tables
│── requirements.txt        # List of dependencies
│── README.md               # Documentation
└── data/                   # Folder containing HTML files and assets

Dependencies

The required dependencies are listed in requirements.txt and can be installed using pip.

License

This project is licensed under the MIT License.

Author

Dario Castellon