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