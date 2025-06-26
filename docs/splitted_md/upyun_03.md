### 水印

**图片水印**

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/watermark/url/<url>` | Base64 编码字符串 | 水印相对路径的 Base64 编码，相对路径包含 `/`，比如 `/path/to/watermark.png`。水印需要上传到待处理图片的服务下。详见[注] |
| `/align/<align>` | 位置，如 north | 水印图片放置方位，默认 `northwest`，详见[方位说明](#align_gravity) |
| `/margin/<x>x<y>` | 横偏移x纵偏移，如 15×10 | 水印图片横纵相对偏移，默认 `20x20` |
| `/opacity/<opacity>` | 透明度，如 90 | 水印图片透明度，默认 `100`，取值范围 `[0-100]`，值越大越不透明，`0` 完全透明，`100` 完全不透明 |
| `/percent/<integer>` | 百分比值，如 50 | 水印图片自适应原图短边的比例，默认 `0`，表示不设置该参数，详见[注] |
| `/repeat/<boolean>` | true | 水印图片是否重复铺满原图，默认 `false` |
| `/animate/<boolean>` | true | 允许对动态图片加水印，默认 `false` |

**文字水印**

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/watermark/text/<text>` | 文字内容，如 `5L2g5aW977yB` | 文字内容的 Base64 编码字符串，示例为 `你好！` |
| `/size/<size>` | 大小，如 16 | 文字大小，单位 px，默认 `32` |
| `/font/<font>` | 字体，如 simsun（宋体） | 文字字体，默认 `simsun`。字体使用时，需要用参数名。参数名见[字体列表](#font_list) |
| `/color/<color>` | RRGGBB，如 FF0000（红色） | 字体颜色，默认 `000000（黑色）` |
| `/border/<border>` | RRGGBBAA，如 FF000000（不透明红色） | 文字描边，默认 `FFFFFFFF（透明白色）`，详见 [border 说明](#border) |
| `/align/<align>` | 位置，如 north | 文字放置方位，默认 `northwest`，详见[方位说明](#align_gravity) |
| `/margin/<x>x<y>` | 横偏移x纵偏移，如 15×10 | 文字横纵相对偏移，默认 `20x20` |
| `/opacity/<opacity>` | 透明度，如 90 | 文字透明度，默认 `100`，取值范围 `[0-100]`，值越大越不透明，`0` 完全透明，`100` 完全不透明 |
| `/animate/<boolean>` | true | 允许对动态图片加水印，默认 `false` |

**多个水印**

把图片水印或文字水印参数重复。例如，一个文字水印 + 一个图片水印：

```
/watermark/text/5L2g5aW977yB/font/simhei/watermark/url/L2RvY3MvY2xvdWQvdXB5dW4tbG9nby5wbmc=/align/southeast

```

特别地，水印个数越多，处理耗时越长，建议不要超过 3 个。

**注**

* 文字水印最长支持 1024 字节
* 水印需要上传到待处理图片的服务下，水印 URL 使用的是相对路径，不包含 Domain（域名）。
* 水印的 `url` 需要 base64 编码，编码后的字符串中如果包含 `/`（斜杠），需要替换成 `|`（竖线）。
* `align` 或 `gravity` 的 9 个方位：

![方位图](https://upyun-assets.b0.upaiyun.com/docs/process/wmgravity.png)

* 图片水印的 `percent` 取值范围 `[0-100]`。当水印没有出现时，可以尝试设置 `/margin/0x0`。
* 文字水印的 `text` 需要 base64 编码，并把编码后的字符串中的 `/`（斜杠）替换成 `|`（竖线）。
* 文字水印的中含中文内容（`text`）时，字体（`font`）请使用中文字体，否则会乱码。
* 字体列表：

  | 名称 | 类型 | 参数名 |
  | --- | --- | --- |
  | 宋体 | 中文字体 | simsun |
  | 黑体 | 中文字体 | simhei |
  | 楷体 | 中文字体 | simkai |
  | 隶书 | 中文字体 | simli |
  | 幼圆 | 中文字体 | simyou |
  | 仿宋 | 中文字体 | simfang |
  | 简体中文 | 中文字体 | sc |
  | 繁体中文 | 中文字体 | tc |
  | Arial | 英文字体 | arial |
  | Georgia | 英文字体 | georgia |
  | Helvetica | 英文字体 | helvetica |
  | Times-New-Roman | 英文字体 | roman |
* `border` 的值 `RRGGBBAA`，`RRGGBB` 表示边框颜色；`AA` 表示不透明度，取值 `[0-255]`，值越大越透明，`00` 表示完全不透明，`FF` 表示完全透明。
* `<x>x<y>` 中，连接 `<x>`与`<y>`是小写字母 x，不是乘号。

### 旋转

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/rotate/<固定值>` | auto | 自动扶正 |
| `/rotate/<angle>` | `(0, 360]`，如 90° | 按角度旋转 |

**翻转**

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/flip/<orientation>` | 方向，如 `left,right` | 翻转方向，可选值：`left,right`、`top,down` |

**注**

* `left,right` 表示从左向右翻转，`top,down` 表示从上向下翻转。

### 锐化

提高图片模糊部位的清晰度或聚焦程度。

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/unsharp/<boolean>` | true | 锐化，默认 `false` |

### 高斯模糊

减少图片噪音和降低图片细节层次，使图片模糊化。

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/gaussblur/<radius>x<sigma>` | 模糊半径x标准差，如 5×2 | 高斯模糊 |

**注**

* `0 <= radius <= 50` 且 `radius` 是整数，`sigma` 是正整数。当 `radius = 0` 时，`raduis` 根据 `sigma` 自动计算产生。
* `<radius>x<sigma>` 中的 `x` 是小写字母 x，不是乘号。

### 边框

为图片添加边框，支持设置边框颜色。

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/border/<w>x<h>` | 宽x高，如 3×2 | 边框尺寸，`w` 表示左右边框宽度，`h` 表示上下边框宽度 |
| `/brdcolor/<brdcolor>` | RRGGBBAA，如 FF000000（红色不透明） | 边框颜色和透明度，默认 `FFFFFF00（白色不透明）` |

**注**

* `brdcolor` 的值 `RRGGBBAA`，`RRGGBB` 表示边框颜色；`AA` 表示不透明度，取值 `[0-255]`，值越大越透明，`00` 表示完全不透明，`FF` 表示完全透明。
* `<w>x<h>` 中的 `x` 是小写字母 x，不是乘号。

### 画布

为图片添加画布，相当于把图片放入画布中。

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/canvas/<w>x<h>a<x>a<y>` | 宽x高axay，如 600x400a50a20 | 画布尺寸，`w` 表示画布宽，`h` 表示画布高，`x`、`y` 表示图片左上角在画布中的坐标，如果 `x`、`y` 不存在，则图片在画布中间 |
| `/cvscolor/<FFFFFF00>` | RRGGBBAA，如 FF000000（红色不透明） | 边框颜色和透明度，默认 FFFFFF00（白色不透明） |
| `/gravity/<northwest>` | 方位，如 north | 裁剪开始的方位，默认 `northwest`，详见[方位说明](#align_gravity)。特别地，`/gravity` 需要放在 `/canvas` 后面 |

**注**

* `cvscolor` 的值 `RRGGBBAA`，`RRGGBB` 表示边框颜色；`AA` 表示不透明度，取值 `[0-255]`，值越大越透明，`00` 表示完全不透明，`FF` 表示完全透明。
* `<w>x<h>` 中的 `x` 是小写字母 x，不是乘号。

### 灰白图

把图片转换成灰白图，适用于公祭、艺术欣赏等场景，参数如下：

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/gray/<boolean>` | true | 是否把图片转换成灰白图，默认 `false` |

**注**

* 暂时只支持 jpg/png 图片，其他格式图片可以先进行格式转换，加 `/format/jpg` 或 `/format/png`。

### 元数据获取

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/info` | 无 | 获取基本信息（包括宽、高、格式、帧数） |
| `/meta` | 无 | 获取 EXIF 信息 + 基本信息 |
| `/meta/iptc` | iptc | 获取 IPTC 信息 + 基本信息 |
| `/meta/all` | all | 获取图片所有信息，当前是 EXIF 信息 + IPTC 信息 + 基本信息 |

**注**

* 上传预处理时，响应信息中默认包含图片基本信息（`info`），获取其他图片信息，见 [FORM API](/knowledge-base/form_api/#upload_args) 中的 `x-gmkerl-type` 参数。
* `/meta/all` 获取到的信息会随着平台支持的信息增多而变化，请在使用时注意。
