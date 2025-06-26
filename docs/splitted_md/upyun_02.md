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
