快速入门
----

又拍云处理（图片处理）基于 CDN 或云存储服务，您在使用它之前，请确保您已经注册又拍云账号并完成实名验证，请确保您已经创建 [CDN 服务](/knowledge-base/cdn-quick-start/)或[云存储服务](/knowledge-base/quick_start/)。

收费方面，图片处理是完全免费的。

相关阅读：[演示 WebP 如何让您的图片大小平均减少 70%](https://www.upyun.com/webp)，[WebP 开发专题](#webp)。

开发者指南
-----

### URL 作图

通过 URL 访问图片时，对图片进行处理，并把处理后的图片返回。

**URL 作图的格式**

```
图片 URL + 间隔标识符 + 参数或缩略图版本

```

间隔标识符说明，见[间隔标识符](#tag)；参数说明，见[功能](#function)；缩略图版本说明，见[缩略图版本](#thumb)。

**例如**

图片 URL 是 [`https://p.upyun.com/docs/cloud/demo.jpg`](https://p.upyun.com/docs/cloud/demo.jpg "查看")， 间隔标识符是 `!`， 功能是 `格式转换成 webp`， 访问的 URL 是 [`https://p.upyun.com/docs/cloud/demo.jpg!/format/webp`](https://p.upyun.com/docs/cloud/demo.jpg!/format/webp "查看")。

### 间隔标识符

用于分隔图片 URL 和处理信息，有 3 种可选，分别是：`!`（感叹号/默认值）、`-`（中划线）和 `_`（下划线），可登录又拍云[控制台](https://console.upyun.com/services/)，在 「服务」 > 「功能配置」 > 「图片处理」 中设置。

### 缩略图版本

缩略图版本在又拍云[控制台](https://console.upyun.com/services/)，「服务」 > 「功能配置」 > 「图片处理」 中创建，它里面包含许多图片处理功能。如下图： [![缩略图版本](https://upyun-assets.b0.upaiyun.com/docs/process/image_version.png)](https://upyun-assets.b0.upaiyun.com/docs/process/image_version.png "查看大图") **例如** 缩略图版本名称是 `upyun520`， 访问的 URL 是 [`https://p.upyun.com/docs/cloud/demo.jpg!upyun520`](https://p.upyun.com/docs/cloud/demo.jpg!upyun520 "查看")。 其中，`!` 是[间隔标识符](#tag)。

### 原图保护密钥

* 上传图片时，保护密钥通过 [REST API](/knowledge-base/rest_api/#upload_file) | [FORM API](/knowledge-base/form_api/#upload_args) 的 `Content-Secret` 设置。
* 已经存在存储的图片，可以通过编辑 [Metadata](/knowledge-base/rest_api/#metadata_2) 设置保护密钥。

图片添加保护密钥后，访问时需要带上 「[间隔标识符](#tag)」 和 「保护密钥」，才能访问图片。

例如，保护密钥是 `abc`，访问图片 URL 是 [`https://p.upyun.com/docs/cloud/secret.jpg!abc`](https://p.upyun.com/docs/cloud/secret.jpg!abc "查看")。 如果保护密钥跟缩略图版本名称相同，当作保护密钥。特别地，对有保护密钥的图片进行处理时，不需要加保护密钥。

### 混合使用

假设存在缩略图版本 `upyun520`，现在针对某类图片需要调整缩略图版本的配置，比如限定宽度为 500px（`/fw/500`），可以使用缩略图版本与参数混合，通过参数对缩略图版本进行动态调整。因为，参数的优先级高于缩略图版本。 URL 作图混合使用是：

```
https://p.upyun.com/docs/cloud/demo.jpg!upyun520/fw/500

```

上传预处理混合使用是：

```
x-gmkerl-thumb: upyun520/fw/500

```

特别地，参数只能出现在缩略图版本的后面，如 `/fw/500` 出现在 `upyun520` 后面。

### 图片拼接

请查看[图片拼接(异步)](/knowledge-base/async_image/)

### 上传预处理（同步）

在上传图片时，对上传的图片进行处理，并保存处理后的图片到又拍云存储。

支持的 API： [REST API](/knowledge-base/rest_api/#upload_file) | [FORM API](/knowledge-base/form_api/#upload_args) | [文件拉取](/knowledge-base/spider/)。

参数名是 `x-gmkerl-thumb`，参数值是 `参数或缩略图版本`。处理参数见[功能](#function)。

**举例**

例 1：转换图片格式为 png

```
x-gmkerl-thumb: /format/png

```

例 2：限定图片宽度为 300px、锐化、压缩质量 80、存储为 png 格式（参数不区分先后顺序）

```
x-gmkerl-thumb: /fw/300/unsharp/true/quality/80/format/png

```

### 上传预处理（异步）

在上传图片时，对上传的图片进行处理，生成一张或多张新的图片，同时保存上传的图片到又拍云存储。任务以异步的方式处理，处理完成后，回调通知用户处理结果。

支持的 API： [FORM API](/knowledge-base/form_api/#upload_args)。

参数名是 `apps`，参数值是 JSON 数组。一个 `apps` 最多允许包含 10 个图片处理任务。 设置了 `apps` 参数，会创建异步处理任务，否则为同步处理任务

**apps 参数结构**

| 参数 | 必选 | 说明 |
| --- | --- | --- |
| name | 是 | 使用异步图片处理服务，固定值 `thumb` |
| x-gmkerl-thumb | 是 | 图片处理功能参数或缩略图版本名称，处理参数见[功能](#function) |
| x-gmkerl-split | 否 | 图片分块，按 `宽x高` 把图片分成数块，见「注」 |
| save\_as | 否 | 结果图片保存路径 |
| notify\_url | 否 | 回调地址，不填时使用[上传参数](/knowledge-base/form_api/#upload_args)中的 `notify-url` |

**save\_as 支持的变量**

| 变量名 | 说明 |
| --- | --- |
| {filepath} | 原图在存储中的路径 |
| {filename} | 原图文件名 |
| {suffix} | 原图文件名后缀，不带点 |
| {row} | 切割后小图的位置行号，从 0 开始，从左到右依次增大 |
| {column} | 切割后小图的位置列号，从 0 开始，从上到下依次增大 |
| {seq} | 切割后小图的序列号，从 0 开始，从左到右、从上到下依次增大 |

**注**

* `x-gmkerl-split` 会在 `x-gmkerl-thumb` 的基础上把图片分成数块，用户可以根据回调信息中的行号跟列号来确定分块后的图片在原图中的位置。
* `x-gmkerl-split` 会输出多个图片，从左上角开始，往右列号从 0 依次增大，往下行号从 0 依次增大，序列号按行从左往右、从上到下、从 0 依次增大。

**举例**

```
apps = [
    {                                             
        "name": "thumb",
        "x-gmkerl-thumb": "/fw/300/quality/95",    
        "save_as": "/path/to/fw_300.jpg",          
        "notify_url": "http://your/notify/url"     
    },
    ......
]

```

### 异步处理

对已经存在云存储中的图片文件，以 `POST` 方法向 `http://p0.api.upyun.com/pretreatment/` 提交处理任务，响应中返回任务 `task_id`。任务以异步的方式处理，处理完成后，回调通知用户处理结果。

```
curl -X POST \
    http://p0.api.upyun.com/pretreatment/ \
    -H "Authorization: UPYUN <Operator>:<Signature>" \
    -H "Date: <Wed, 29 Oct 2014 02:26:58 GMT>" \
    -H "Content-MD5: <Content-MD5>" \
    -d "service=<service>" \
    -d "app_name=thumb" \
    -d "notify_url=<notify_url>" \
    -d "source=<图片文件相对路径>" \
    -d "accept=json"  \
    -d "tasks=<base64 编码后的任务字符串>" 

```

**认证鉴权**

`Authorization` 详见[签名认证](/knowledge-base/cloud_process_authorization/)。

**请求参数**

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| service | string | 是 | 图片文件所在的服务名 |
| app\_name | string | 是 | thumb: 固定值图片处理 |
| notify\_url | string | 是 | 回调通知地址，详见[回调通知](#notice) |
| source | string | 否 | 可在每个task中单独指定原图片文件路径 |
| accept | string | 否 | 回调信息的格式，默认值为`json` |
| tasks | string | 是 | 任务信息，详见tasks 参数说明 |

**tasks 参数说明**

按 JSON 格式组装任务，一次请求 `tasks` 最多可以提交 10 个任务。任务参数见[功能](#function)。

```
[
    {
        "x-gmkerl-thumb": "/fw/100/100",                        // 图片处理参数
        "source": "/image/1.jpg",                               // 图片源路径
        "save_as": "/image/new_1.jpg"                           // 保存路径
    },
    …
]

```

### 回调通知

异步任务处理完成后，向 `notify_url` 地址发送回调通知。回调信息为 JSON 格式，字段名及含义如下：

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | string | 异步处理任务 ID（在上传时返回） |
| `service` | string | 文件所在空间名 |
| `status_code` | integer | 处理结果状态码，`200` 表示成功处理 |
| `imginfo` | map | 输出单张图片信息 |
| `imginfos` | array | 输出多张图片信息 |
| `error` | string | 错误信息 |

`imginfo` 、 `imginfos` 中包含信息如下：

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `path` | string | 作图结果保存路径（`save_as`参数指定） |
| `type` | string | 图片类型 |
| `width` | integer | 图片宽度 |
| `height` | integer | 图片高度 |
| `frame` | integer | 图片帧数 |
| `row` | integer | 相对于左上角的行号，从 `0` 开始，仅当图片分块时有效 |
| `column` | integer | 相对于左上角的列号，从 `0` 开始，仅当图片分块时有效 |

**举例**

例 1：输出单张图片的回调信息

```
{
    "task_id": "b52c96bea30646abf8170f333bbd42b9",
    "service": "upyun-demo",
    "status_code": 200,
    "imginfo": {
        "path": "/images/upyun.jpg",
        "type": "jpg",
        "width": 720,
        "height": 360,
        "frames": 1
    }
}

```

例 2：输出多张图片（使用了[图片分块 x-gmkerl-split](#async_process)） 的回调信息

```
{
    "task_id": "b52c96bea30646abf8170f333bbd42b9",
    "service": "upyun-demo",
    "status_code": 200,
    "imginfos": [
      {
        "path": "/images/upyun.jpg-1.jpg",
        "type": "jpg",
        "width": 72,
        "height": 36,
        "frames": 1,
        "row": 0,
        "column": 0
      },
      {
        "path": "/images/upyun.jpg-2.jpg",
        "type": "jpg",
        "width": 72,
        "height": 36,
        "frames": 1,
        "row": 0,
        "column": 1
      }
    ]
}

```

### 状态码表

| 状态码 | 说明 |
| --- | --- |
| 200 | 处理成功 |
| 400 | 参数错误，返回 JSON 中包含具体错误信息 |
| 404 | 指定 Profile 信息不存，Not Profile |
| 405 | 图片数据无效，Not an image |
| 405 | 图片宽高超出限制，Image Width/Height Limit Error |
| 406 | 非图片获取图片基本信息时数据无效，Not an image |
| 409 | 图片大小超出限制，限制为 2 亿像素，Limit Exceeded |
| 413 | 请求处理超时，A Big Image! |
| 5xx | 服务端错误。如遇此类错误，请反馈给[售后](https://www.upyun.com/contact)或您的商务经理 |

上传预处理的更多错误码，请查询 [API 错误码表](/knowledge-base/errno/)。

### 支持格式

| 类型 | 值 |
| --- | --- |
| 输入格式 | JPG、JPEG、PNG、WebP、动态 WebP、GIF、动态 GIF、BMP、SVG等 |
| 输出格式 | JPG、PNG、WebP、动态 WebP |

**其他约束**

* 图片宽或高最大不能超过 2 万像素，「宽 \* 高 \* 帧数」最大不能超过 2 亿。

### WebP 开发专题

有损 WebP 效果演示：[WebP 如何让您的图片大小平均减少 70%](https://www.upyun.com/webp.html)

无损 WebP 使用指南：[无损 WebP 正确的使用姿势](https://help.upyun.com/2017/06/22/%E6%97%A0%E6%8D%9F-webp%E6%AD%A3%E7%A1%AE%E7%9A%84%E4%BD%BF%E7%94%A8%E5%A7%BF%E5%8A%BF/)

格式转换成有损 WebP：`/format/webp`

格式转换成无损 WebP：`/format/webp/lossless/true`

**举例**

JPG 转成有损 WebP：www.domain.com/a.jpg!/format/webp

PNG 转成无损 WebP：www.domain.com/a.png!/format/webp/lossless/true

GIF/动态 GIF 转成有损 WebP：www.domain.com/a.gif!/format/webp

SVG 转成无损 WebP：www.domain.com/a.svg!/format/webp/lossless/true

其中，`!` 是[间隔标识符](#tag)，`/format/webp`、`/lossless/true` 的解释见「功能」> [输出设置](#output)。

功能
--

### 缩小&放大

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/fw/<width>` | 宽，如 300 | 限定宽度，高度自适应 |
| `/fh/<height>` | 高，如 200 | 限定高度，宽度自适应 |
| `/max/<max>` | 最长边，如 200 | 限定最长边，短边自适应 |
| `/min/<min>` | 最短边，如 200 | 限定最短边，长边自适应 |
| `/fwfh/<w>x<h>` | 宽x高，如 300×200 | 限定宽度或高度，宽高不足时不缩放 |
| `/fwfh2/<w>x<h>` | 宽x高，如 300×200 | 限定宽度最小值和高度最小值，宽高不足时不缩放 |
| `/both/<w>x<h>` | 宽x高，如 300×200 | 固定宽度和高度，宽高不足时居中裁剪再缩放。特别地，配合 `/force/true` 使用时，宽高不足时只缩放，不裁剪 |
| `/sq/<w>` | 宽或高，如 300 | 图片缩放成正方形，宽高相等 |
| `/scale/<scale>` | 缩放比例，如 50 | 宽高等比例缩放，取值范围 `[1-1000]` |
| `/wscale/<wscale>` | 宽度缩放比例，如 200 | 宽度按比例缩放，高度不变，取值范围 `[1-1000]` |
| `/hscale/<hscale>` | 高度缩放比例，如 200 | 高度按比例缩放，宽度不变，取值范围 `[1-1000]` |
| `/fxfn/<max>x<min>` | 长边x短边，如 300×200 | 限定长边或短边，进行等比缩放，不裁剪 |
| `/fxfn2/<max>x<min>` | 长边x短边，如 300×200 | 限定长边最小值和短边最小值，进行等比缩放，不裁剪 |
| `/fp/<integer>` | 宽高像素积，如 200000 | 宽高等比例缩放，直到宽高像素积小于但最接近指定值，取值范围 `[1-25000000]` |
| `/force/<boolean>` | true | 不支持放大的参数，指定 `/force/` 为 `true` 进行放大，默认 `false` |

**注**

* `fwfh` 当原图宽与期望缩放的宽的比例大于原图高与期望缩放的高的比例时，是 `fw`；否则，是 `fh`。
* `scale` 值取 `20` 时，缩小后的图片宽高是原图宽高的 `20%`；取 `200` 时，放大后的图片宽高是原图宽高的 `200%`。
* 特别地，大部分参数默认不支持放大，如果需要放大，请指定 `/force/true` 。 – `<w>x<h>` 中的 `x` 是小写字母 x，不是乘号。

### 裁剪

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/crop/<w>x<h>a<x>a<y>` | 宽x高axay，如 300x200a80a60 | 缩小或放大前进行裁剪 |
| `/clip/<w>x<h>a<x>a<y>` | 宽x高axay，如 300x200a80a60 | 缩小或放大后进行裁剪 |
| `/gravity/<gravity>` | 位置，如 north | 裁剪开始的方位，默认 `northwest`，详见[方位说明](#align_gravity)。特别地，`/gravity` 需要放在 `/crop` 或 `/clip` 的后面 |
| `/roundrect/<roundrect>` | 圆角半径，如 20 | 裁剪时对四角进行圆化（圆角裁剪），默认 `10` |

**注**

* `<w>x<h>` 中的 `x` 是小写字母 x，不是乘号。当 `<w>x<h>` 是 `0x0` 时，自动根据偏移量计算裁剪图片宽、高。
* `a<x>s<y>` 中的 `<x>`、`<y>` 表示偏移量，`a`、`s` 表示正、负，`x` 正负判断依据是：往 `east` 方向偏移，为 `a`；往 `west` 方向偏移，为 `s`; `y` 正负判断依据是：往 `south` 方向偏移，为 `a`；往 `north` 方向偏移，为 `s`。

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

### Exif 编辑

以 `/exifset/` 开头，后面的参数如下：

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/copyright/<Base64 版权信息>` | string | 指定 Exif 中的版权信息，需要 Base64 编码 |
| `/artist/<Base64 作者信息>` | string | 指定 Exif 中的作者信息，需要 Base64 编码 |

**举例**

* 同时修改版权和作者信息：`/exifset/copyright/dXB5dW4gaW5j/artist/5Y+I5ouN5LqR`。
* `/copyright/` 和 `/artist/` 关系版权，请审慎编辑。

### 输出设置

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/format/<图片格式>` | string | 可选值 `jpg`、`png`、`webp`。`webp` 包含动态 WebP |
| `/lossless/<boolean>` | true | 无损压缩，默认 `false`。仅当输出格式是 `WebP` 时有效 |
| `/quality/<quality>` | 整数值，如 75 | 设置压缩质量，可选范围`[1-99]` |
| `/compress/<boolean>` | true | JPG 、 PNG 大小压缩优化，默认 `false` |
| `/coalesce/<boolean>` | false | 是否填充动态 GIF 图像中共同部分，默认 `true`，见「注」 |
| `/progressive/<boolean>` | true | JPG 图片渐进式加载，图片加载从模糊到清晰 |
| `/gifto/<boolean>` | true | 多帧 GIF 图片转为单帧 GIF 图片 |
| `/exifswitch/<boolean>` | true | 保留 EXIF 信息 ，默认会删除 EXIF 信息 |
| `/noicc/<boolean>` | true | 清除图片 ICC 信息，默认 `false` |
| `/strip/<boolean>` | true | 去除图片所有元信息，包括 EXIF 、ICC 等。默认 `false` |
| `/ignore-error/<boolean>` | true | 是否忽略错误返回原图 ，默认 `false`，返回错误 |

**注**

* 一般来说，`quality（质量）` 是 `75`，在这个值压缩大小与图片质量损失得到平衡。
* `compress` 会对 JPG/PNG 进行一次压缩以减少图片体积，同时稍微延长了图片处理时间、降低了图片质量。
* `noicc` 会导致图片质量轻微的下降。
* 大部分动态 GIF 可以通过省略相邻帧之间共同部分来优化图片体积。如果 `coalesce` 参数为 `false`，当对动态 GIF 做缩略或放大时，可能会导致图片质量下降。
* `ignore-error` 只对 405、409、503 状态码有效，并会在响应头中附加 `x-gmkerl-err-code` 字段标记实际错误码。其他错误状态码无效，返回错误。

### 主题色提取

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/excolor/<integer>` | 颜色数量，如 128 | 提取的颜色数量。可选值：`[1-4096]` |
| `/exformat/<exformat>` | 颜色进制，如 hex | 返回颜色的进制，默认 `dec`。可选值：`dec`、`hex` |

**注**

* 以 JSON 格式返回颜色。`hex（十六进制）` 表示颜色为 `0xRRGGBB`，如 `0xff00aa`；`dec（十进制）` 表示颜色为 `12345678`。

### 静态图渐变

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `/gdori/<orientation>` | 方向，如 top,down（自上而下） | 渐变方向 |
| `/gdpos/<gdpos>` | 开始位置,结束位置，如 10,100 | 渐变从开始位置至结束位置。单位像素（px） |
| `/gdstartcolor/<gdstartcolor>` | RRGGBBAA，如 FF000000（红色不透明） | 开始位置颜色及透明度 |
| `/gdstopcolor/<gdstopcolor>` | RRGGBBAA，如 FF000000（红色不透明） | 结束位置颜色及透明度 |

**注**

* `gdori` 取值：`top,down`（自上而下）、`bottom,up`（自下而上）、`left,right`（自左向右）、`right,left`（自右向左）。
* `RRGGBBAA`：`RRGGBB` 表示边框颜色；`AA` 表示不透明度，取值 `[0-255]`，值越大越透明，`00` 表示完全不透明，`FF` 表示完全透明。

---

如有疑问请 [联系我们](https://www.upyun.com/contact)

### 这篇文章有帮助吗?

[Yes](#)
[No](#)

### 相关文章

* [盲水印（异步）](https://help.upyun.com/knowledge-base/%e7%9b%b2%e6%b0%b4%e5%8d%b0%ef%bc%88%e5%bc%82%e6%ad%a5%ef%bc%89/)
* [音视频处理（已弃用）](https://help.upyun.com/knowledge-base/av_pretreatment/)
* [图片拼接（异步）](https://help.upyun.com/knowledge-base/async_image/)
* [文档转换](https://help.upyun.com/knowledge-base/%e6%96%87%e6%a1%a3%e8%bd%ac%e6%8d%a2/)
* [音频处理（同步）](https://help.upyun.com/knowledge-base/sync_audio/)
* [视频处理（同步）](https://help.upyun.com/knowledge-base/sync_video/)