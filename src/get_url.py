import os
import json
import os
import requests
import yaml
from typing import Dict, Any, List
from bs4 import BeautifulSoup

class URLCrawler:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.input_file = config['input_file']
        self.output_file = config['output_file']
        self.crawl_related_urls_enabled = config.get('crawl_related_urls', False)
        self.only_main_content = config.get('onlyMainContent', True)
        self.include_tags = config.get('includeTags', [])
        self.exclude_tags = config.get('excludeTags', [])
        self.timeout = config.get('timeout', 30000) / 1000  # Convert ms to seconds

    def _crawl_related_urls(self, url: str) -> Dict[str, str]:
        """Crawl related URLs from the given page."""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if self.only_main_content:
                # Prioritize main content tags, then fall back to body
                content_container = soup.find('main') or soup.find('article') or soup.find('body')
            else:
                # If not only_main_content, always use the body
                content_container = soup.find('body')

            if not content_container:
                return {}

            # Filter elements based on includeTags and excludeTags
            def filter_element(element):
                if self.include_tags:
                    # Check if element matches any include tag/class/id
                    included = False
                    for tag_spec in self.include_tags:
                        if tag_spec.startswith('.'):
                            if tag_spec[1:] in element.get('class', []):
                                included = True
                                break
                        elif tag_spec.startswith('#'):
                            if tag_spec[1:] == element.get('id'):
                                included = True
                                break
                        else:
                            if element.name == tag_spec:
                                included = True
                                break
                    if not included:
                        return False

                if self.exclude_tags:
                    # Check if element matches any exclude tag/class/id
                    for tag_spec in self.exclude_tags:
                        if tag_spec.startswith('.'):
                            if tag_spec[1:] in element.get('class', []):
                                return False
                        elif tag_spec.startswith('#'):
                            if tag_spec[1:] == element.get('id'):
                                return False
                        else:
                            if element.name == tag_spec:
                                return False
                return True

            all_links = content_container.find_all('a')
            print(f"Found {len(all_links)} total links in content_container.")
            filtered_links = [link for link in all_links if filter_element(link)]
            print(f"Found {len(filtered_links)} filtered links after applying include/exclude tags.")
            
            related_urls = {}
            for link in filtered_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if not href or not text or href.startswith('#') or 'javascript:' in href:
                    continue
                
                if not href.startswith('http'):
                    if href.startswith('/'):
                        base_url = '/'.join(url.split('/')[:3])
                        href = base_url + href
                    else:
                        href = url.rsplit('/', 1)[0] + '/' + href
                
                if url.split('/')[2] in href:
                    related_urls[text] = href
            
            return related_urls
            
        except requests.RequestException as e:
            print(f"Error crawling related URLs from {url}: {str(e)}")
            return {}

    def run(self) -> None:
        """Reads URLs from input, crawls related URLs if enabled, and saves to output."""
        if not self.config.get('enable', False):
            print("URL crawling is disabled in configuration.")
            return

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                url_data = json.load(f)
            
            output_data = {}
            
            for provider, categories in url_data.items():
                output_data[provider] = {}
                for category, url in categories.items():
                    print(f"Processing URL for crawling: {url}")
                    if self.crawl_related_urls_enabled:
                        related_urls = self._crawl_related_urls(url)
                        if related_urls:
                            output_data[provider][category] = related_urls
                        else:
                            output_data[provider][category] = url # If no related URLs, just keep the original URL
                    else:
                        output_data[provider][category] = url # If crawling is disabled, just keep the original URL
            
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=4)
            print(f"Saved crawled URLs to: {self.output_file}")
            
        except Exception as e:
            print(f"Error in URL crawling process: {str(e)}")