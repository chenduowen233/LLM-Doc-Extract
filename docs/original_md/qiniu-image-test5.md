[智能多媒体服务](/dora) > API 文档 > 图片处理 >图片高级处理（imageMogr2） >旋转

旋转
==

最近更新时间: 2025-02-19 14:25:10

**简介**
======

**imageMogr2** 提供一系列高级图片处理功能，本文介绍 **图片旋转**，可与 **imageMogr2** 的其他参数一起使用，详细的计费说明请参见 [计费与定价](https://www.qiniu.com/prices/dora?source=dora)。

**限制说明**
========

* 原图格式支持： `psd`、`jpeg`、`png`、`gif`、`webp`、`tiff`、`bmp`、`avif`、`heic`
* 同步处理
  + 原图支持 20MB 以内的图片
  + 处理前动图帧数限制：`webp动图` 最大帧数为50，`gif` 最大帧数为 200
  + 处理前体积限制：图片 `w` 和`h`不能超过3万像素，总像素不能超过1.5亿像素
  + 处理后体积限制：图片`w`和`h` 不能超过9999像素，总像素不得超过2500w 像素。以下情况特别说明：
    - 输出为 `avif` 时，图片 `w`和`h` 不能超过9999像素，总像素不能超过768w像素
    - 输出为 `webp静图` 时，图片 `w` 和 `h`  不能超过16383像素，总像素不得超过2500w 像素
    - 仅限 `输入为webp动图格式，输出webp动图/gif动图时`，图片 `w` 和 `h`  不能超过999像素，总像素（宽x高x帧数）不能超过3150万像素
* 持久化处理
  + 原图支持 512MB 以内的图片
  + 处理前动图帧数限制：`gif`、`webp动图`，最大帧数为 500
  + 处理前体积限制：图片 `w`和`h` 不能超过3万像素，总像素不能超过1.5亿像素
  + 处理后体积限制：图片 `w`和`h` 不能超过14999像素，总像素不得超过6000w像素。以下情况特别说明：
    - 输出为 `heic`和 `avif` 时，图片 `w`和`h` 不能超过9999像素，总像素不能超过3072w像素
    - 输出为 `webp动图和静图` 时，图片 `w` 和 `h`  不能超过16383像素，总像素不得超过6000w像素

**参数说明**
========

**注意**：接口规格不含任何空格与换行符。

```
imageMogr2/auto-orient
          /rotate/<rotate>       

```

参数说明
----

| 参数名称 | 必填 | 说明 |
| --- | --- | --- |
| `/auto-orient` |  | 自适应旋转：与图像处理顺序相关，建议放在首位，根据原图EXIF信息自动旋正，便于后续处理。 |
| `/rotate/<rotate>` |  | 普通旋转：图片顺时针旋转角度，取值范围为1-360，默认为不旋转。 **注意**：输入输出是动图时，取值只能是90/180/270。 |

**示例**
======

* 原图

![img](https://dn-odum9helk.qbox.me/resource/gogopher.jpg)

* 顺时针旋转 45 度：

  ```
   https://dora-doc.qiniu.com/gogopher.jpg?imageMogr2/rotate/45

  ```

![img](https://dora-doc.qiniu.com/gogopher.jpg?imageMogr2/rotate/45)

**操作方式**
========

您可以通过 [同步处理](/dora/api/8266/synchronous-processing)、[持久化处理](/dora/api/1291/persistent-data-processing-pfop)、[图片样式设置](/dora/api/8264/the-picture-style)、[CDN中间源处理](https://developer.qiniu.com/fusion/4954/image-optimization) 等方式，对图片进行处理，详情介绍请参见[图片处理操作方式](/dora/api/8234/the-image-processing1)。

以上内容是否对您有帮助？

文档反馈
(如有产品使用问题，请 [提交工单](https://support.qiniu.com/tickets/category))

提交

![](/assets/icon-sevice-21342418ba5b3d3a9ba87d3ef1df87fabd3a1c59a9e76a8b71df63efdbfbfef1.png) 服务•咨询

[![Close](/assets/close-c80c279cfed4ad83fa45163d69624d1cfacc5a42b9338006dd1a26e4730e5e1e.png)](javascript:;)

回到顶部


×

#### 产品及服务咨询

提交成功！

提交失败，稍后重试！

此表单仅用于产品及服务售前咨询（您也可以拨打400-808-9176转2）  
如有售后技术咨询，请[提交工单](https://support.qiniu.com/tickets/category)

咨询内容\*

请填写咨询内容

最多可输入255字

姓名\*

请填写姓名

公司名称

省份\*

联系电话\*

请以正确的格式填写联系电话

电子邮箱\*

请填写电子邮箱

提交