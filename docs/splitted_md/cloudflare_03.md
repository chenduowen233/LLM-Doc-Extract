### `gravity`

When cropping with `fit: "cover"` and `fit: "crop"`, this parameter defines the side or point that should not be cropped. Available options are:

* `auto`\
  Selects focal point based on saliency detection (using maximum symmetric surround algorithm).

* `side`\
  A side (`"left"`, `"right"`, `"top"`, `"bottom"`) or coordinates specified on a scale from `0.0` (top or left) to `1.0` (bottom or right), `0.5` being the center. The X and Y coordinates are separated by lowercase `x` in the URL format. For example, `0x1` means left and bottom, `0.5x0.5` is the center, `0.5x0.33` is a point in the top third of the image.

  For the Workers integration, use an object `{x, y}` to specify coordinates. It contains focal point coordinates in the original image expressed as fractions ranging from `0.0` (top or left) to `1.0` (bottom or right), with `0.5` being the center. `{fit: "cover", gravity: {x:0.5, y:0.2}}` will crop each side to preserve as much as possible around a point at 20% of the height of the source image.

Note

You must subtract the height of the image before you calculate the focal point.

* URL format

  ```js
  gravity=auto


  OR


  gravity=left


  OR


  gravity=0x1
  ```

* URL format alias

  ```js
  g=auto


  OR


  g=left


  OR


  g=0x1
  ```

* Workers

  ```js
  cf: {image: {gravity: "auto"}}


  OR


  cf: {image: {gravity: "right"}}


  OR


  cf: {image: {gravity: {x:0.5, y:0.2}}}
  ```

```plaintext
```

### `height`

Specifies maximum height of the image in pixels. Exact behavior depends on the `fit` mode (described below).

* URL format

  ```js
  height=250
  ```

* URL format alias

  ```js
  h=250
  ```

* Workers

  ```js
  cf: {image: {height: 250}}
  ```

### `metadata`

Controls amount of invisible metadata (EXIF data) that should be preserved.

Color profiles and EXIF rotation are applied to the image even if the metadata is discarded. Content Credentials (C2PA metadata) may be preserved if the [setting is enabled](https://developers.cloudflare.com/images/transform-images/preserve-content-credentials).

Available options are `copyright`, `keep`, and `none`. The default for all JPEG images is `copyright`. WebP and PNG output formats will always discard EXIF metadata.

Note

* If [Polish](https://developers.cloudflare.com/images/polish/) is enabled, then all metadata may already be removed and this option will have no effect.
* Even when choosing to keep EXIF metadata, Cloudflare will modify JFIF data (potentially invalidating it) to avoid the known incompatibility between the two standards. For more details, refer to [JFIF Compatibility](https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format#Compatibility).

Options include:

* `copyright`\
  Discards all EXIF metadata except copyright tag. If C2PA metadata preservation is enabled, then this option will preserve all Content Credentials.
* `keep`\
  Preserves most of EXIF metadata, including GPS location if present. If C2PA metadata preservation is enabled, then this option will preserve all Content Credentials.
* `none`\
  Discards all invisible EXIF and C2PA metadata. If the output format is WebP or PNG, then all metadata will be discarded.

- URL format

  ```js
  metadata=none
  ```

- Workers

  ```js
  cf: {image: {metadata: "none"}}
  ```

### `onerror`

Note

This setting only works directly with [image transformations](https://developers.cloudflare.com/images/transform-images/) and does not support resizing with Cloudflare Workers.

In case of a [fatal error](https://developers.cloudflare.com/images/reference/troubleshooting/#error-responses-from-resizing) that prevents the image from being resized, redirects to the unresized source image URL. This may be useful in case some images require user authentication and cannot be fetched anonymously via Worker. This option should not be used if there is a chance the source image is very large. This option is ignored if the image is from another domain, but you can use it with subdomains.

* URL format

  ```js
  onerror=redirect
  ```

### `quality`

Specifies quality for images in JPEG, WebP, and AVIF formats. The quality is in a 1-100 scale, but useful values are between `50` (low quality, small file size) and `90` (high quality, large file size). `85` is the default. When using the PNG format, an explicit quality setting allows use of PNG8 (palette) variant of the format. Use the `format=auto` option to allow use of WebP and AVIF formats.

We also allow setting one of the perceptual quality levels `high|medium-high|medium-low|low`

* URL format

  ```js
  quality=50


  OR


  quality=low
  ```

* URL format alias

  ```js
  q=50


  OR


  q=medium-high
  ```

* Workers

  ```js
  cf: {image: {quality: 50}}


  OR


  cf: {image: {quality: "high"}}
  ```
