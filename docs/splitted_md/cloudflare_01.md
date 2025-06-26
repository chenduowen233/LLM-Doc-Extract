---
title: Transform via URL · Cloudflare Images docs
description: You can convert and resize images by requesting them via a specially-formatted URL. This way you do not need to write any code, only change HTML markup of your website to use the new URLs. The format is:
lastUpdated: 2025-03-14T14:35:48.000Z
source_url:
  html: https://developers.cloudflare.com/images/transform-images/transform-via-url/
  md: https://developers.cloudflare.com/images/transform-images/transform-via-url/index.md
---

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

### `blur`

Blur radius between `1` (slight blur) and `250` (maximum). Be aware that you cannot use this option to reliably obscure image content, because savvy users can modify an image's URL and remove the blur option. Use Workers to control which options can be set.

* URL format

  ```js
  blur=50
  ```

* Workers

  ```js
  cf: {image: {blur: 50}}
  ```

### `border`

Adds a border around the image. The border is added after resizing. Border width takes `dpr` into account, and can be specified either using a single `width` property, or individually for each side.

* Workers

  ```js
  cf: {image: {border: {color: "rgb(0,0,0,0)", top: 5, right: 10, bottom: 5, left: 10}}}
  cf: {image: {border: {color: "#FFFFFF", width: 10}}}
  ```

### `brightness`

Increase brightness by a factor. A value of `1.0` equals no change, a value of `0.5` equals half brightness, and a value of `2.0` equals twice as bright. `0` is ignored.

* URL format

  ```js
  brightness=0.5
  ```

* Workers

  ```js
  cf: {image: {brightness: 0.5}}
  ```

### `compression`

Slightly reduces latency on a cache miss by selecting a quickest-to-compress file format, at a cost of increased file size and lower image quality. It will usually override the `format` option and choose JPEG over WebP or AVIF. We do not recommend using this option, except in unusual circumstances like resizing uncacheable dynamically-generated images.

* URL format

  ```js
  compression=fast
  ```

* Workers

  ```js
  cf: {image: {compression: "fast"}}
  ```

### `contrast`

Increase contrast by a factor. A value of `1.0` equals no change, a value of `0.5` equals low contrast, and a value of `2.0` equals high contrast. `0` is ignored.

* URL format

  ```js
  contrast=0.5
  ```

* Workers

  ```js
  cf: {image: {contrast: 0.5}}
  ```
