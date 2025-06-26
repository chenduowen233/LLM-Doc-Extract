Title: 开启和使用图片处理_CDN(CDN)-阿里云帮助中心

URL Source: https://help.aliyun.com/zh/cdn/user-guide/image-processing-operation-method

Markdown Content:
如果有图片自适应 WEBP、自动旋转（仅自动调正功能）和自动瘦身需求，可通过控制台直接开启；您也可以通过在请求 URL 中添加图片处理参数，对图片文件进行更丰富的处理，例如图片裁剪、图片添加水印等。

**说明**

*   阿里云 CDN、DCDN 和 OSS 的图片处理都是独立的功能，不能相互混用。

*   图像处理为付费服务，公测期间**暂不收费**，收费时间另行通知。

*   当您使用图像处理功能时，由于不同图片格式在压缩算法上存在较大差异，因此不同图片格式之间相互转换可能会导致图片体积变大，例如：jpeg 转 webp、jpeg 转 png、png 转 webp。如果您需要降低图片文件的体积，建议您通过调整质量参数`quality`降低图片质量来实现。

开启图像处理
------

1.   登录[CDN 控制台](https://cdn.console.aliyun.com/)[](https://cdn.console.aliyun.com/)。

2.   在左侧导航栏，单击**域名管理**。

3.   在**域名管理**页面，找到目标域名，单击**操作**列的**管理**。

4.   在指定域名的左侧导航栏，单击**性能优化**。

5.   在**图像处理**区域框中，打开**图像处理**开关，选择您需要转换的图片类型。

**说明**

    *   选择支持的图片类型后，表示开启图片处理功能。开启图像处理后，[通过文件 URL 处理图片](https://help.aliyun.com/zh/cdn/user-guide/image-processing-operation-method#title-7fs-ak1-zn1)时，URL 中携带的图像处理参数才会生效，否则为无效参数。

    *   控制台上是否开启自适应 WEBP、图片自动旋转（仅自动调正功能）和图片自动瘦身功能，根据自身业务决定。

![Image 1: picture_process-cn.jpg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0710561371/p873001.jpg)

**参数****说明**
**支持转换的图片类型**选择您需要转换的图片类型（必选参数，可多选）。
**自适应 WEBP**开启后，通过对请求头 Accept 进行判断，如果请求头 Accept 包含`image/webp`，则 CDN 会将其他格式图片自动转换为 WEBP 格式进行缓存。

**说明**

开启该功能后，短时间内会导致命中率下降，过后会自动恢复正常，请勿在业务高峰期开启。
**图片自动旋转**开启图片自动旋转，可自动调正图片，方便用户查看。

**说明**

    *   图片自动旋转只对带有旋转参数`auto-orient`的图片生效。

    *   开启该功能后，短时间内会导致命中率下降，过后会自动恢复正常，请勿在业务高峰期开启。
**图片自动瘦身**开启后（默认不开启），在不改变分辨率、尺寸和格式的前提下对图片进行压缩，节省访问流量。

    *   0（默认值）：表示不开启。

    *   1~100：表示开启。例如，填写 90%表示保留原图质量的 90%。

**说明**

仅支持 JPEG 和 WEBP 格式。
**原图缓存**当一个原图存在多个转换后副本时，开启原图缓存将减少回源次数。

6.   单击**确定**，完成开通。

通过文件 URL 处理图片
-------------

1.   已选择支持转换的图片类型，请参考[开启图像处理](https://help.aliyun.com/zh/cdn/user-guide/image-processing-operation-method#title-2k7-dsk-jpb)。

2.   通过请求 URL 传参来完成自定义功能。

    *   格式：`http://example.com/image_01.png?image_process=action,param_value/action,param_value`

**字段****说明**
example.com 您的 CDN 加速域名。
image_01.png 图片名称。
image_process image_process 为固定参数，标明使用图片处理参数对图片文件进行处理。
action,param_value 图片处理的操作（action）、参数（param）和值（value），用于定义图片处理的方式。多个操作以正斜线（/）隔开，CDN 将按图片处理参数的顺序处理图片。图片处理支持的参数，请参见[图片处理参数](https://help.aliyun.com/zh/cdn/user-guide/image-processing-operation-method#0bee1f84d8ish)。
    *   示例：`http://example.com/image_01.png?image_process=resize,w_200/rotate,90/format,webp`

    *   图片处理效果：图片先按比例缩放至宽 200 px，再将图片旋转 90°，最终保存为 WEBP 格式。

### **支持的图片处理参数**

通过在请求 URL 中添加图片处理参数可实现更丰富的图像处理功能。CDN 支持携带一个或多个转换参数处理图片，支持的参数请参见下表。

**图片处理功能****处理参数****说明**
[格式转换](https://help.aliyun.com/zh/cdn/user-guide/convert-image-formats#concept-1999252)format 转换图片格式。
[质量转换](https://help.aliyun.com/zh/cdn/user-guide/adjust-image-quality#concept-1999251)quality 调整图片质量。
[图片裁剪](https://help.aliyun.com/zh/cdn/user-guide/crop-images#concept-1999196)crop 裁剪指定大小的图片。
[图片缩放](https://help.aliyun.com/zh/cdn/user-guide/resize-images#concept-1999176)resize 将图片缩放至指定大小（目前只支持将原图缩小处理，暂不支持将原图放大处理）。
[图片旋转](https://help.aliyun.com/zh/cdn/user-guide/rotate-images#concept-1999222)*   图片自动旋转：auto-orient

*   指定旋转方向：rotate 将携带旋转参数的图片进行自适应旋转或按指定角度以顺时针方向旋转图片。
[图片色彩](https://help.aliyun.com/zh/cdn/user-guide/change-the-color-of-an-image#concept-1999230)*   图片亮度：bright

*   图片对比度：contrast

*   图片锐化：sharpen 调整图片的亮度、对比度和清晰度。
[添加水印](https://help.aliyun.com/zh/cdn/user-guide/manage-image-watermarks#concept-1999247)watermark 为图片添加图片水印或文字水印。
[获取信息](https://help.aliyun.com/zh/cdn/user-guide/query-image-information#concept-1998910)info 获取图片信息，包括图片的长、宽、高、图片格式和图片质量等信息。
