# This module uses BeautifulSoup and requests to scrape 
# supplementary web statistics (such as detailed match stats 
# or player metrics) directly from public sports sites.

import json
import logging
import requests
from bs4 import BeautifulSoup
from config.settings import RAW_DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SportsWebScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }     
    def scrape_sample_match_stats(self, target_url: str) -> list[dict]:
        """Example Web Scraper fetching html tabular data."""
        logging.info(f"Scraping web statistics from {target_url}")
        results = []
        try:
            response = requests.get(target_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract table rows example
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cols = [ele.text.strip() for ele in row.find_all(["td", "th"])]
                    if cols:
                        results.append(cols)
        
        except Exception as e:
            logging.error(f"Error scraping web page {target_url}: {e}")

        return results

    def save_raw_scrape(self, data: list, filename: str):
        """Save raw scraped data as JSON."""
        output_path = RAW_DATA_DIR / filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved scraped data to {output_path}")


if __name__ == "__main__":
    scraper = SportsWebScraper()
    # Scrape target web source
    scraped_data = scraper.scrape_sample_match_stats("https://news.ycombinator.com")
    scraper.save_raw_scrape(scraped_data, "raw_web_scraped_stats.json")
