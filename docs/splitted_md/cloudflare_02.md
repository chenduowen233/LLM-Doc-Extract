### `dpr`

Device Pixel Ratio. Default is `1`. Multiplier for `width`/`height` that makes it easier to specify higher-DPI sizes in `<img srcset>`.

* URL format

  ```js
  dpr=1
  ```

* Workers

  ```js
  cf: {image: {dpr: 1}}
  ```

### `fit`

Affects interpretation of `width` and `height`. All resizing modes preserve aspect ratio. Used as a string in Workers integration. Available modes are:

* `scale-down`\
  Similar to `contain`, but the image is never enlarged. If the image is larger than given `width` or `height`, it will be resized. Otherwise its original size will be kept. Example:
* `contain`\
  Image will be resized (shrunk or enlarged) to be as large as possible within the given `width` or `height` while preserving the aspect ratio. If you only provide a single dimension (for example, only `width`), the image will be shrunk or enlarged to exactly match that dimension.
* `cover`\
  Resizes (shrinks or enlarges) to fill the entire area of `width` and `height`. If the image has an aspect ratio different from the ratio of `width` and `height`, it will be cropped to fit.
* `crop`\
  Image will be shrunk and cropped to fit within the area specified by `width` and `height`. The image will not be enlarged. For images smaller than the given dimensions, it is the same as `scale-down`. For images larger than the given dimensions, it is the same as `cover`. See also [`trim`](#trim)
* `pad`\
  Resizes to the maximum size that fits within the given `width` and `height`, and then fills the remaining area with a `background` color (white by default). This mode is not recommended, since you can achieve the same effect more efficiently with the `contain` mode and the CSS `object-fit: contain` property.

- URL format

  ```js
  fit=scale-down
  ```

- Workers

  ```js
  cf: {image: {fit: "scale-down"}}
  ```

### `flip`

Flips the image horizontally, vertically, or both. Can be used with the `rotate` parameter to set the orientation of an image.

Flipping is performed before rotation. For example, if you apply `flip=h,rotate=90,` then the image will be flipped horizontally, then rotated by 90 degrees.

Available options are:

* `h`: Flips the image horizontally.
* `v`: Flips the image vertically.
* `hv`: Flips the image vertically and horizontally.

- URL format

  ```js
  flip=h
  ```

- Workers

  ```js
  cf: {image: {flip: "h"}}
  ```

### `format`

The `auto` option will serve the WebP or AVIF format to browsers that support it. If this option is not specified, a standard format like JPEG or PNG will be used. Cloudflare will default to JPEG when possible due to the large size of PNG files.

Workers integration supports:

* `avif`: Generate images in AVIF format if possible (with WebP as a fallback).
* `webp`: Generate images in Google WebP format. Set the quality to `100` to get the WebP lossless format.
* `jpeg`: Generate images in interlaced progressive JPEG format, in which data is compressed in multiple passes of progressively higher detail.
* `baseline-jpeg`: Generate images in baseline sequential JPEG format. It should be used in cases when target devices don't support progressive JPEG or other modern file formats.
* `json`: Instead of generating an image, outputs information about the image in JSON format. The JSON object will contain data such as image size (before and after resizing), source image's MIME type, and file size.

- URL format

  ```js
  format=auto
  ```

- URL format alias

  ```js
  f=auto
  ```

- Workers

  ```js
  cf: {image: {format: "avif"}}
  ```

For the `format:auto` option to work with a custom Worker, you need to parse the `Accept` header. Refer to [this example Worker](https://developers.cloudflare.com/images/transform-images/transform-via-workers/#an-example-worker) for a complete overview of how to set up an image transformation Worker.

```js
const accept = request.headers.get("accept");
let image = {};


if (/image\/avif/.test(accept)) {
  image.format = "avif";
} else if (/image\/webp/.test(accept)) {
  image.format = "webp";
}


return fetch(url, { cf: { image } });
```

### `gamma`

Increase exposure by a factor. A value of `1.0` equals no change, a value of `0.5` darkens the image, and a value of `2.0` lightens the image. `0` is ignored.

* URL format

  ```js
  gamma=0.5
  ```

* Workers

  ```js
  cf: {image: {gamma: 0.5}}
  ```
