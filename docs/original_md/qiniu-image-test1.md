当您的图片格式不满足需求，例如图片格式导致文件过大，或不同平台对图片格式有要求导致图片显示错误。您可以通过格式转换，将图片自动转换为WEBP格式或转换为指定格式。

**说明** 

* 阿里云CDN、DCDN和OSS的图片处理都是独立的功能，不能相互混用。
* 图像处理为付费服务，公测期间**暂不收费**，收费时间另行通知。

自适应WEBP
-------

WEBP是一种支持有损压缩和无损压缩的图片文件格式。CDN支持自适应WEBP功能，开启自适应WEBP，通过对请求头Accept进行判断，如果请求头Accept包含`image/webp`，则CDN会将其他格式图片自动转换为WEBP格式进行缓存。开启自适应WEBP，请参见[图像处理操作方法](https://help.aliyun.com/zh/cdn/user-guide/image-processing-operation-method)。

**重要** 开启该功能后，短时间内会导致命中率下降，过后会自动恢复正常，请勿在业务高峰期开启。

**操作示例**

下方的Accept内容仅作为示例，实际的Accept内容以真实情况为准。示例中Accept里包含了`image/webp`，表示支持自适应WEBP功能。

```
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
```

**格式转换**处理参数
------------

### **参数说明**

操作名称：**format**

|  |  |
| --- | --- |
| **取值范围** | **说明** |
| jpeg | 将原图保存为JPG或JPEG格式。 |
| png | 将原图保存为PNG格式。 |
| webp | 将原图保存为WEBP格式。 |
| bmp | 将原图保存为BMP格式。 |
| gif | 原图为GIF图片则继续保存为GIF格式；原图不是GIF图片，则按原图格式保存。 |
| tiff | 将原图保存为TIFF格式。 |
| jpeg 2000 | 将原图保存为JPEG 2000格式，图片后缀为JP2。 |

### **操作示例**

将原图转换为BMP格式，图片处理URL为：`http(s)://example.com/image_01.png?image_process=format,bmp`

[上一篇：图片处理操作方法](/zh/cdn/user-guide/image-processing-operation-method)[下一篇：质量转换](/zh/cdn/user-guide/adjust-image-quality)

反馈