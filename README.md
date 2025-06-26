# LLM-Doc-Extract

基于Python的文档预处理工具，可以从指定的URL获取文档内容，将其转换为Markdown格式，并根据配置规则进行文档切割。

## 功能特点

- 支持从URL获取文档内容
- 使用Jina AI进行文档格式转换
- 自动清理网页导航栏等无关内容
- 支持多种文档切割方式：
  - 按标题级别切割
  - 按行数切割
- 支持批量处理多个URL
- 可配置的输出格式和命名规则

## 项目结构

```
.
├── config.yaml          # 配置文件
├── main.py             # 主程序入口
├── requirements.txt    # 项目依赖
├── src/
│   ├── config_loader.py    # 配置加载器
│   └── document_processor.py # 文档处理器
└── output/            # 输出目录
```

## 安装

1. 克隆项目：
```bash
git clone [项目地址]
cd LLM-Doc-Extract
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

在 `config.yaml` 文件中配置：

```yaml
# URLs to process
urls:
  - https://example.com/doc1
  - https://example.com/doc2

# Document splitting configuration
splitting:
  method: heading  # 'heading' or 'line_count'
  max_heading_level: 2  # 如果按标题切割
  lines_per_split: 100  # 如果按行数切割

# Output configuration
output:
  output_dir: ./output
  file_prefix: doc_
  file_extension: md
```

## 使用方法

1. 配置 `config.yaml` 文件
2. 运行程序：
```bash
python main.py
```

程序将自动：
- 读取配置的URL列表
- 获取并转换文档内容
- 根据配置规则切割文档
- 将结果保存到输出目录

## 扩展性

该工具设计时考虑了扩展性：

1. 文档处理模块化：
   - 配置加载
   - 文档获取
   - 内容转换
   - 文档切割
   - 输出处理

2. 易于添加新功能：
   - 新的文档切割策略
   - 其他文档格式支持
   - 自定义处理规则

## 注意事项

- 确保有足够的网络访问权限
- 遵守目标网站的爬虫政策
- 建议对重要文档进行备份
