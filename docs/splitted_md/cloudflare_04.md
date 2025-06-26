### `rotate`

Number of degrees (`90`, `180`, or `270`) to rotate the image by. `width` and `height` options refer to axes after rotation.

* URL format

  ```js
  rotate=90
  ```

* Workers

  ```js
  cf: {image: {rotate: 90}}
  ```

### `saturation`

Increases saturation by a factor. A value of `1.0` equals no change, a value of `0.5` equals half saturation, and a value of `2.0` equals twice as saturated. A value of `0` will convert the image to grayscale.

* URL format

  ```js
  saturation=0.5
  ```

* Workers

  ```js
  cf: {image: {saturation: 0.5}}
  ```

### `sharpen`

Specifies strength of sharpening filter to apply to the image. The value is a floating-point number between `0` (no sharpening, default) and `10` (maximum). `1` is a recommended value for downscaled images.

* URL format

  ```js
  sharpen=2
  ```

* Workers

  ```js
  cf: {image: {sharpen: 2}}
  ```

### `slow-connection-quality`

Allows overriding `quality` value whenever a slow connection is detected.

Available options are same as [quality](https://developers.cloudflare.com/images/transform-images/transform-via-url/#quality).

* URL format

  ```js
  slow-connection-quality=50
  ```

* URL format alias

  ```js
  scq=50
  ```

Detecting slow connections is currently only supported on Chromium-based browsers such as Chrome, Edge, and Opera.

You can enable any of the following client hints via HTTP in a header

```txt
accept-ch: rtt, save-data, ect, downlink
```

slow-connection-quality applies whenever any of the following is true and the client hint is present:

* [rtt](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/RTT): Greater than 150ms.

* [save-data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Save-Data): Value is "on".

* [ect](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ECT): Value is one of `slow-2g|2g|3g`.

* [downlink](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Downlink): Less than 5Mbps.

### `trim`

Specifies a number of pixels to cut off on each side. Allows removal of borders or cutting out a specific fragment of an image. Trimming is performed before resizing or rotation. Takes `dpr` into account. For image transformations and Cloudflare Images, use as four numbers in pixels separated by a semicolon, in the form of `top;right;bottom;left` or via separate values `trim.width`,`trim.height`, `trim.left`,`trim.top`. For the Workers integration, specify an object with properties: `{top, right, bottom, left, width, height}`.

* URL format

  ```js
  trim=20;30;20;0
  trim.width=678
  trim.height=678
  trim.left=30
  trim.top=40
  ```

* Workers

  ```js
  cf: {image: {trim: {top: 12,  right: 78, bottom: 34, left: 56, width:678, height:678}}}
  ```

### `width`

Specifies maximum width of the image. Exact behavior depends on the `fit` mode; use the `fit=scale-down` option to ensure that the image will not be enlarged unnecessarily.

Available options are a specified width in pixels or `auto`.

* URL format

  ```js
  width=250
  ```

* URL format alias

  ```js
  w=250
  ```

* Workers

  ```js
  cf: {image: {width: 250}}
  ```

Ideally, image sizes should match the exact dimensions at which they are displayed on the page. If the page contains thumbnails with markup such as `<img width="200">`, then you can resize the image by applying `width=200`.

[To serve responsive images](https://developers.cloudflare.com/images/transform-images/make-responsive-images/#transform-with-html-srcset), you can use the HTML `srcset` element and apply width parameters.

`auto` - Automatically serves the image in the most optimal width based on available information about the browser and device. This method is supported only by Chromium browsers. For more information about this works, refer to [Transform width parameter](https://developers.cloudflare.com/images/transform-images/make-responsive-images/#transform-with-width-parameter).

## Recommended image sizes

Ideally, image sizes should match exactly the size they are displayed on the page. If the page contains thumbnails with markup such as `<img width="200" …>`, then images should be resized to `width=200`. If the exact size is not known ahead of time, use the [responsive images technique](https://developers.cloudflare.com/images/manage-images/create-variants/).

If you cannot use the `<img srcset>` markup, and have to hardcode specific maximum sizes, Cloudflare recommends the following sizes:

* Maximum of 1920 pixels for desktop browsers.
* Maximum of 960 pixels for tablets.
* Maximum of 640 pixels for mobile phones.

Here is an example of markup to configure a maximum size for your image:

```txt
/cdn-cgi/image/fit=scale-down,width=1920/<YOUR-IMAGE>
```

The `fit=scale-down` option ensures that the image will not be enlarged unnecessarily.

You can detect device type by enabling the `CF-Device-Type` header [via Cache Rule](https://developers.cloudflare.com/cache/how-to/cache-rules/examples/cache-device-type/).

## Caching

Resizing causes the original image to be fetched from the origin server and cached — following the usual rules of HTTP caching, `Cache-Control` header, etc.. Requests for multiple different image sizes are likely to reuse the cached original image, without causing extra transfers from the origin server.

Note

If Custom Cache Keys are used for the origin image, the origin image might not be cached and might result in more calls to the origin.

Resized images follow the same caching rules as the original image they were resized from, except the minimum cache time is one hour. If you need images to be updated more frequently, add `must-revalidate` to the `Cache-Control` header. Resizing supports cache revalidation, so we recommend serving images with the `Etag` header. Refer to the [Cache docs for more information](https://developers.cloudflare.com/cache/concepts/cache-control/#revalidation).

Cloudflare Images does not support purging resized variants individually. URLs starting with `/cdn-cgi/` cannot be purged. However, purging of the original image's URL will also purge all of its resized variants.
