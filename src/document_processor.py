import os
import os
from typing import Dict, Any

from .get_url import URLCrawler
from .convert import ContentConverter
from .splitter import DocumentSplitter

class DocumentProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def process_documents(self) -> None:
        """Process all documents according to configuration."""
        # 1. URL爬取
        if self.config['processing']['get_url']['enable']:
            print("Step 1: Getting URLs...")
            url_crawler = URLCrawler(self.config['processing']['get_url'])
            url_crawler.run()

        # 2. URL转Markdown
        if self.config['processing']['convert']['enable']:
            print("Step 2: Converting URLs to Markdown...")
            converter = ContentConverter(self.config['processing']['convert'])
            converter.run()

        # 3. Markdown分割
        if self.config['processing']['split']['enable']:
            print("Step 3: Splitting Markdown documents...")
            splitter = DocumentSplitter(self.config['processing']['split'])
            splitter.run()