import os
import json
import requests
import os
from typing import Dict, Any
from bs4 import BeautifulSoup
from markdownify import markdownify as md

class ContentConverter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.url_to_md_config = config.get('url_to_md', {})
        self.local_to_md_config = config.get('local_to_md', {})

    def _fetch_and_convert_url_to_md(self, url: str, prefix: str, output_dir: str) -> None:
        """Fetch URL content and convert to markdown using Jina, then save."""
        try:
            # api_url = f"https://r.jina.ai/{url}"
            api_url = url
            response = requests.get(api_url, timeout=60)
            response.raise_for_status()
            
            # Clean HTML content using BeautifulSoup
            cleaned_soup = self._clean_content(response.text)
            # Convert cleaned HTML (BeautifulSoup object) to Markdown
            markdown_content = md(str(cleaned_soup))
            
            # Save the markdown content
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{prefix}.md"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Converted and saved: {filepath}")
            
        except requests.RequestException as e:
            print(f"Error fetching or converting URL {url}: {str(e)}")

    def _clean_content(self, content: str) -> BeautifulSoup:
        """Clean up the converted content by removing navigation and unnecessary elements based on config."""
        soup = BeautifulSoup(content, 'html.parser')

        only_main_content = self.url_to_md_config.get('onlyMainContent', True)
        include_tags = self.url_to_md_config.get('includeTags', [])
        exclude_tags = self.url_to_md_config.get('excludeTags', [])

        # Determine the content container based on onlyMainContent config
        if only_main_content:
            content_container = soup.find('main') or soup.find('article') or soup.find('body')
        else:
            content_container = soup.find('body')

        if not content_container:
            return soup # Fallback to original soup if no container found

        # Create a new soup with only the content_container's content
        cleaned_soup = BeautifulSoup(str(content_container), 'html.parser')

        # Apply excludeTags filtering (fuzzy matching for class/id)
        for tag_spec in exclude_tags:
            # Check if it's a tag name (e.g., 'footer', 'header')
            if tag_spec.isalpha():
                for tag in cleaned_soup.find_all(tag_spec):
                    tag.decompose()
            # Check if it's a class (e.g., '.sidebar')
            elif tag_spec.startswith('.'):
                class_name = tag_spec[1:]
                for element in cleaned_soup.find_all(class_=lambda x: x and class_name in x):
                    element.decompose()
            # Check if it's an ID (e.g., '#navigation')
            elif tag_spec.startswith('#'):
                id_name = tag_spec[1:]
                for element in cleaned_soup.find_all(id=lambda x: x and id_name in x):
                    element.decompose()
            # Fuzzy matching for any attribute containing the tag_spec
            else:
                for element in cleaned_soup.find_all(lambda tag: 
                    any(tag_spec in (tag.get(attr) or '') for attr in ['class', 'id']) or 
                    tag_spec == tag.name
                ):
                    element.decompose()

        # Apply includeTags filtering
        if include_tags:
            # If includeTags are specified, remove everything not in includeTags
            all_elements = cleaned_soup.find_all(True) # Get all elements
            for element in all_elements:
                should_keep = False
                for tag_spec in include_tags:
                    # Check if it's a tag name
                    if tag_spec.isalpha() and element.name == tag_spec:
                        should_keep = True
                        break
                    # Check if it's a class
                    elif tag_spec.startswith('.') and element.has_attr('class') and tag_spec[1:] in element['class']:
                        should_keep = True
                        break
                    # Check if it's an ID
                    elif tag_spec.startswith('#') and element.has_attr('id') and tag_spec[1:] == element['id']:
                        should_keep = True
                        break
                if not should_keep and element.parent: # Don't remove the root of cleaned_soup
                    element.decompose()

        # Remove script and style tags always
        for tag in cleaned_soup.find_all(['script', 'style']):
            tag.decompose()

        return cleaned_soup



    def run(self) -> None:
        """Process URLs from input file and convert to Markdown."""
        if not self.config.get('enable', False):
            print("Content conversion is disabled in configuration.")
            return

        if self.url_to_md_config.get('enable', False):
            input_file = self.url_to_md_config.get('input_file')
            output_dir = self.url_to_md_config.get('output_dir')

            if not input_file or not output_dir:
                print("URL to Markdown conversion is enabled but input_file or output_dir is not specified.")
                return

            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    url_data = json.load(f)
                
                for provider, categories in url_data.items():
                    for category, urls_or_dict in categories.items():
                        # Determine if urls_or_dict is a list of URLs or a dict of related URLs
                        if isinstance(urls_or_dict, dict):
                            # It's a dictionary of related URLs (from get_url output)
                            for text, url in urls_or_dict.items():
                                prefix = f"{provider.lower()}-{category}-{text.replace(' ', '_')}"
                                self._fetch_and_convert_url_to_md(url, prefix, output_dir)
                        elif isinstance(urls_or_dict, str):
                            # It's a single URL string
                            prefix = f"{provider.lower()}-{category}"
                            self._fetch_and_convert_url_to_md(urls_or_dict, prefix, output_dir)

            except Exception as e:
                print(f"Error in URL to Markdown conversion process: {str(e)}")

        if self.local_to_md_config.get('enable', False):
            # Implement local file conversion if needed
            print("Local file to Markdown conversion is not yet implemented.")