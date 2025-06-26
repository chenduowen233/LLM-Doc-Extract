import os
import yaml
from src.document_processor import DocumentProcessor

def main():
    try:
        # 加载配置文件
        with open("config.yaml", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        # 初始化文档处理器
        processor = DocumentProcessor(config)
        
        # 处理所有文档
        processor.process_documents()
        
        print("文档处理完成！")
        
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")

if __name__ == "__main__":
    main()
