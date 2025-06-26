from langchain.text_splitter import MarkdownHeaderTextSplitter
from typing import List, Dict

def split_markdown_by_header(markdown_text: str) -> List[Dict[str, str]]:
    """
    按三级标题(###)切割Markdown文档
    
    Args:
        markdown_text: 要切割的Markdown文本
        
    Returns:
        包含标题和对应内容的字典列表
    """
    # 定义标题结构，这里指定按三级标题(###)切割
    headers_to_split_on = [
        ("###", "header")
    ]
    
    # 创建MarkdownHeaderTextSplitter实例
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    
    # 执行切割
    split_result = markdown_splitter.split_text(markdown_text)
    
    return split_result

# 示例Markdown文档
sample_markdown = """
You can convert and resize images by requesting them via a specially-formatted URL. This way you do not need to write any code, only change HTML markup of your website to use the new URLs. The format is:

```txt
https://<ZONE>/cdn-cgi/image/<OPTIONS>/<SOURCE-IMAGE>
```

Here is a breakdown of each part of the URL:

* `<ZONE>`

  * Your domain name on Cloudflare. Unlike other third-party image resizing services, image transformations do not use a separate domain name for an API. Every Cloudflare zone with image transformations enabled can handle resizing itself. In URLs used on your website this part can be omitted, so that URLs start with `/cdn-cgi/image/`.

* `/cdn-cgi/image/`

  * A fixed prefix that identifies that this is a special path handled by Cloudflare's built-in Worker.

* `<OPTIONS>`

  * A comma-separated list of options such as `width`, `height`, and `quality`.

* `<SOURCE-IMAGE>`

  * An absolute path on the origin server, or an absolute URL (starting with `https://` or `http://`), pointing to an image to resize. The path is not URL-encoded, so the resizing URL can be safely constructed by concatenating `/cdn-cgi/image/options` and the original image URL. For example: `/cdn-cgi/image/width=100/https://s3.example.com/bucket/image.png`.

Here is an example of an URL with `<OPTIONS>` set to `width=80,quality=75` and a `<SOURCE-IMAGE>` of `uploads/avatar1.jpg`:

```html
<img src="/cdn-cgi/image/width=80,quality=75/uploads/avatar1.jpg" />
```

Note

You can use image transformations to sanitize SVGs, but not to resize them. Refer to [Resize with Workers](https://developers.cloudflare.com/images/transform-images/transform-via-workers/) for more information.

## Options

You must specify at least one option. Options are comma-separated (spaces are not allowed anywhere). Names of options can be specified in full or abbreviated.

### `anim`

Whether to preserve animation frames from input files. Default is `true`. Setting it to `false` reduces animations to still images. This setting is recommended when enlarging images or processing arbitrary user content, because large GIF animations can weigh tens or even hundreds of megabytes. It is also useful to set `anim:false` when using `format:"json"` to get the response quicker without the number of frames.

* URL format

  ```js
  anim=false
  ```

* Workers

  ```js
  cf: {image: {anim: false}}
  ```

### `background`

Background color to add underneath the image. Applies to images with transparency (for example, PNG) and images resized with `fit=pad`. Accepts any CSS color using CSS4 modern syntax, such as `rgb(255 255 0)` and `rgba(255 255 0 100)`.

* URL format

  ```js
  background=%23RRGGBB


  OR


  background=red


  OR


  background=rgb%28240%2C40%2C145%29
  ```

* Workers

  ```js
  cf: {image: {background: "#RRGGBB"}}


  OR


  cf:{image: {background: "rgba(240,40,145,0)"}}
  ```
"""

# 执行切割
if __name__ == "__main__":
    # 切割Markdown文档
    split_result = split_markdown_by_header(sample_markdown)
    
    # 打印切割结果
    print(f"共切割出 {len(split_result)} 个部分：")
    for i, part in enumerate(split_result):
        print(f"\n第 {i+1} 部分:")
        
        # 调试：打印所有元数据键
        print(f"可用元数据键: {list(part.metadata.keys())}")
        
        # 正确访问标题的方式
        print(f"标题: {part.metadata.get('header', '未找到标题')}")
        
        # 访问内容
        print(f"内容: \n{part.page_content}")