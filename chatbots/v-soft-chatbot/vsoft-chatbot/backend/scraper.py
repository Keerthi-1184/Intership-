# import os
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import time

# class VSoftScraper:
#     def __init__(self, base_url="https://www.vsoftconsulting.com/"):
#         self.base_url = base_url
#         self.domain = urlparse(base_url).netloc
#         self.visited_urls = set()
#         self.data_dir = "vsoft_data"
#         os.makedirs(self.data_dir, exist_ok=True)

#     def is_valid_url(self, url):
#         parsed = urlparse(url)
#         return parsed.netloc == self.domain and not parsed.path.startswith('/wp-')

#     def save_page(self, url, content):
#         path = urlparse(url).path
#         if not path or path == '/':
#             path = '/index'
        
#         filename = os.path.join(self.data_dir, path[1:].replace('/', '_') + '.html')
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
        
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(content)
#         return filename

#     def scrape_page(self, url):
#         if url in self.visited_urls:
#             return []
        
#         self.visited_urls.add(url)
#         print(f"Scraping: {url}")
        
#         try:
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()
            
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Remove unwanted elements
#             for element in soup(['script', 'style', 'nav', 'footer', 'form']):
#                 element.decompose()
            
#             # Save cleaned content
#             self.save_page(url, str(soup))
            
#             # Find all links on page
#             links = set()
#             for link in soup.find_all('a', href=True):
#                 absolute_url = urljoin(url, link['href'])
#                 if self.is_valid_url(absolute_url):
#                     links.add(absolute_url)
            
#             return list(links)
        
#         except Exception as e:
#             print(f"Error scraping {url}: {e}")
#             return []

#     def scrape_site(self, max_pages=20):
#         to_visit = {self.base_url}
#         scraped_count = 0
        
#         while to_visit and scraped_count < max_pages:
#             url = to_visit.pop()
#             new_links = self.scrape_page(url)
            
#             if new_links:
#                 scraped_count += 1
#                 to_visit.update(set(new_links) - self.visited_urls)
            
#             time.sleep(1)  # Be polite with delay between requests

#         print(f"Scraping complete. Saved {scraped_count} pages.")

# if __name__ == "__main__":
#     scraper = VSoftScraper()
#     scraper.scrape_site()


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VSoftScraper:
    def __init__(self, base_url="https://www.vsoftconsulting.com/"):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.data_dir = "vsoft_data"
        os.makedirs(self.data_dir, exist_ok=True)

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain and not parsed.path.startswith('/wp-')

    def save_page(self, url, content):
        path = urlparse(url).path
        if not path or path == '/':
            path = '/index'
        
        filename = os.path.join(self.data_dir, path[1:].replace('/', '_') + '.html')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Saved page: {filename}")
        return filename

    def scrape_page(self, url):
        if url in self.visited_urls:
            return []
        
        self.visited_urls.add(url)
        logger.info(f"Scraping: {url}")
        
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'form']):
                element.decompose()
            
            # Check if content is meaningful
            content = str(soup)
            if len(content.strip()) < 100:
                logger.warning(f"Page {url} has insufficient content")
                return []
            
            # Save cleaned content
            self.save_page(url, content)
            
            # Find all links on page
            links = set()
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                if self.is_valid_url(absolute_url):
                    links.add(absolute_url)
            
            return list(links)
        
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []

    def scrape_site(self, max_pages=20):
        to_visit = {self.base_url}
        scraped_count = 0
        
        while to_visit and scraped_count < max_pages:
            url = to_visit.pop()
            new_links = self.scrape_page(url)
            
            if new_links:
                scraped_count += 1
                to_visit.update(set(new_links) - self.visited_urls)
            
            time.sleep(1)  # Be polite with delay

        logger.info(f"Scraping complete. Saved {scraped_count} pages.")

if __name__ == "__main__":
    scraper = VSoftScraper()
    scraper.scrape_site()