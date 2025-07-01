import yaml
from src.get_url import URLCrawler
from src.convert import ContentConverter
from src.splitter import DocumentSplitter
from src.prompt_contributor import PromptContributor
from src.extractor import DocumentExtractor
from src.json_combiner import JSONCombiner

def main():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # URL爬取模块
    get_url_config = config.get('processing', {}).get('get_url', {})
    if get_url_config.get('enable'):
        print("Running URLCrawler...")
        crawler = URLCrawler(get_url_config)
        crawler.run()

    # 内容转换模块
    convert_config = config.get('processing', {}).get('convert', {})
    if convert_config.get('enable'):
        print("Running ContentConverter...")
        converter = ContentConverter(convert_config)
        converter.run()

    # 文档切割模块
    split_config = config.get('processing', {}).get('split', {})
    if split_config.get('enable'):
        print("Running DocumentSplitter...")
        splitter = DocumentSplitter(split_config)
        splitter.run()

    # 文档信息提取模块
    extracting_config = config.get('extracting', {})
    if extracting_config.get('prompt', {}).get('enable'):
        print("Running DocumentExtractor...")
        extractor = DocumentExtractor(config)
        extractor.run()

        # JSON文件合并模块
        print("Running JSONCombiner...")
        combiner = JSONCombiner()
        combiner.combine_jsons()

if __name__ == "__main__":
    main()
