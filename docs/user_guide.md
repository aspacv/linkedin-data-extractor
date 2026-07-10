# User Guide – LinkedIn Data Extractor

## Overview
This tool extracts public LinkedIn profile data using Selenium and BeautifulSoup.

## Requirements
- Python 3.9+
- Chrome browser
- Internet connection

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Edit `config.json` as needed

## Running the Tool
- Single profile: `python scraper.py --url "https://linkedin.com/in/example"`
- Batch mode: `python scraper.py --file urls.txt`

## Output
Data is saved to `output/profile_data.csv` or `output/profile_data.json`.
