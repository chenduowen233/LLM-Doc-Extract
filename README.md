# LLM-Doc-Extract

基于 Python 的文档信息提取工具，支持从 URL 或本地文件获取文档内容，将其转换为 Markdown 格式，通过 LLM 提取结构化信息，并支持多模型投票以提高准确性。

## 功能特点

- 文档获取与预处理：
  - 支持从 URL 获取文档内容
  - 支持本地文档转换
  - 自动清理网页导航栏等无关内容
  - 支持多种文档切割方式：
    - 按标题级别切割
    - 按行数切割

- LLM 信息提取：
  - 支持多个 LLM 模型（如 Qwen、GPT、Claude 等）
  - 基于 Prompt 模板的信息提取
  - 支持示例学习
  - 结构化 JSON 输出

- 多模型投票机制：
  - 支持多数投票
  - 支持加权投票
  - 支持共识投票
  - 可配置投票字段和权重

- 结果处理：
  - JSON 格式输出
  - 支持文件合并
  - 灵活的输出路径配置

## 项目结构

```
.
├── config.yaml          # 配置文件
├── main.py             # 主程序入口
├── requirements.txt    # 项目依赖
├── src/                # 源代码目录
│   ├── get_url.py         # URL 内容获取
│   ├── convert.py         # 文档格式转换
│   ├── splitter.py        # 文档切割
│   ├── extractor.py       # 信息提取
│   ├── voter.py           # 投票处理
│   ├── json_combiner.py   # JSON 合并
│   └── prompt_contributor.py # Prompt 管理
├── docs/               # 文档目录
│   ├── original_md/       # 原始 Markdown
│   ├── splitted_md/       # 切割后的文档
│   ├── extracted_json/    # 提取的 JSON
│   ├── voted_json/        # 投票后的 JSON
│   └── json/             # 合并后的 JSON
├── prompt/             # Prompt 相关
│   ├── template/          # 提取模板
│   └── example/          # 示例文件
└── providers/          # LLM 提供商配置
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
# 文档处理配置
processing:
  # URL 爬取配置
  get_url:
    enable: true
    input_file: "url/input.json"

  # 文档转换配置
  convert:
    enable: true
    url_to_md:
      output_dir: "docs/original_md"

  # 文档切割配置
  split:
    enable: true
    method: heading    # heading 或 lines
    level: 3           # 标题级别

# 信息提取配置
extracting:
  # 输出路径配置
  output_paths:
    extracted_json_dir: "docs/extracted_json"
    voted_json_dir: "docs/voted_json"
    combined_json_dir: "docs/json"

  # LLM 配置
  LLM:
    model_name: ["model1", "model2"]
    default_model: model1

  # 投票配置
  Vote:
    enable: true
    vote_type: majority  # majority, weighted, consensus
    key_parameter: ["key1", "key2"]
```

## 使用方法

1. 配置 `config.yaml` 文件
2. 运行程序：
```bash
python main.py
```

程序将自动：
- 获取并转换文档内容
- 切割文档为合适大小
- 使用 LLM 提取信息
- 通过多模型投票优化结果
- 合并处理后的 JSON 文件

## 扩展性

该工具设计时考虑了扩展性：

1. 模块化设计：
   - 文档获取与预处理
   - LLM 信息提取
   - 投票机制
   - 结果处理

2. 易于扩展：
   - 支持新的 LLM 模型
   - 自定义投票策略
   - 自定义提取模板
   - 灵活的输出处理

## 注意事项

- 确保配置了正确的 LLM API 密钥
- 遵守目标网站的爬虫政策
- 合理设置文档切割参数
- 根据需要选择合适的投票策略
