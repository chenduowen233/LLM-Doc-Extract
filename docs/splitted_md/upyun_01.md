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
