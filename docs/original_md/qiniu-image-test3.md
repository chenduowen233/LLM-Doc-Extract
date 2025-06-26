[内容分发网络 CDN](/document/product/228)

查询

[文档中心](/document/product "文档中心")*>*[内容分发网络 CDN](/document/product/228 "内容分发网络 CDN")*>*[配置指南](/document/product/228/37851 "配置指南")*>*[域名配置](/document/product/228/6283 "域名配置")*>*[访问控制](/document/product/228/7865 "访问控制")*>*视频拖拽配置

视频拖拽配置
======

最近更新时间：2024-08-22 19:24:41

* 微信扫一扫
* QQ
* 新浪微博
* 复制链接

  链接复制成功

*我的收藏*

配置场景
----

视频拖拽主要产生于视频点播场景中，当用户拖拽播放进度时，会向服务端发起类似如下请求：
`http://www.test.com/test.flv?start=10`
此时会返回第10字节开始的数据，由于点播类视频文件均缓存在各 CDN 节点上，开启此项配置，各节点可直接响应此类请求。

开启视频拖拽需同步开启忽略参数配置，即 [缓存键规则](https://cloud.tencent.com/document/product/228/47671 "https://cloud.tencent.com/document/product/228/47671") 中所有规则的忽略参数配置需为“全部忽略”，且源站需要支持 range 请求。支持的文件格式为：mp4、flv、ts。

|  |  |  |  |
| --- | --- | --- | --- |
| 文件类型 | meta 信息 | start 参数说明 | 请求示例 |
| MP4 | 源站视频的 meta 信息必须在文件头部，不支持 meta 信息在尾部的视频 | start 参数表示的是时间，单位是秒，支持小数以表示毫秒（如 start = 1.01，表示开始时间是1.01s），CDN 会定位到 start 所表示时间的前一个关键帧（如果当前 start 不是关键帧） | `http://www.test.com/demo.mp4?start=10` 表示从第10秒开始播放 |
| FLV | 源站视频必须带有 meta 信息 | start 参数表示字节，CDN 会自动定位到 start 参数所表示的字节的前一个关键帧（如果 start 当前不是关键帧） | `http://www.test.com/demo.flv?start=10` 表示从第10个字节开始播放 |
| TS | 无特殊要求 | start 参数表示字节，CDN 会自动定位到 start 参数所表示的字节 | `http://www.test.com/demo.ts?start=10` 表示从第10个字节开始播放 |

查看配置
----

登录 [CDN 控制台](https://console.cloud.tencent.com/cdn "https://console.cloud.tencent.com/cdn")，在左侧菜单栏选择**域名管理**，选择业务类型为流媒体点播加速的域名，进入域名配置页面，Tab**访问控制**页中即可找到**视频拖拽**，默认为关闭状态，可通过 CDN 音视频点播域名推荐配置默认开启**视频拖拽** 。

﻿

﻿

中国站

在线咨询

目录

返回顶部