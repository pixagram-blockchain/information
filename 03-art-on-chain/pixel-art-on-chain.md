# Pixel Art On Chain

> **Status: Live.** Checked against the app at commit `ca1d157` and against the 141 artworks published from 2026-09-04 to 2026-10-04.

On Pixagram an artwork is not a link to an image. The post *is* the image. This page explains why pixel art makes that possible, how the app turns a picture into an artwork, what exactly is written to the chain, and which images on Pixagram live somewhere else.

## Why pixel art

A photograph runs to megabytes, which is too much to store in every node's copy of the chain. Pixel art is small by nature. It uses a few dozen colours on a grid of a few hundred pixels, and it compresses losslessly into a few tens of kilobytes. On the Pixa chain:

- the median artwork post is about 26 kB
- the largest so far is 497 kB

That is small enough to keep the whole image in the post, so the constraint of the medium becomes the property of the record.

## From picture to artwork

The app's publishing flow works in your browser. [Publish Your First Artwork](../08-guides/publish-your-first-artwork.md) walks through it.

1. **Choose a source.** Upload a picture (PNG, JPEG, GIF, WebP, BMP, AVIF, SVG or HEIC) or describe one in words.
2. **Pixel art passes through.** A picture with fewer than 160 colours is treated as pixel art and published as it is, at its own size.
3. **Anything else is converted.** You choose between:
   - **Local conversion** (the default): an in-browser downscaler reduces the picture to one of five sizes.
   - **AI conversion:** your picture is sent to a Hugging Face Space run by the project (`primerz/face-to-pixel-art-4K`), which redraws it in a chosen style (retroart, lucasart or vga). **The picture leaves your device.** Pictures over 1 MB are first shrunk to about 2 megapixels.
   - **From a description:** a second Space (`primerz/pixel-art`) generates pixel art from text, in one of five aspect ratios.
4. **Optionally quantize.** Shrink the picture 1 to 32 times and reduce it to 2 to 128 colours. Quantizing starts from the full working copy, not from the chosen size.
5. **Publish.** The app encodes the result as a **lossless WebP** image and publishes it.

| Local size | Largest area | Colours |
|---|---|---|
| S | 160 × 160 px | 48 |
| M | 192 × 192 px | 52 |
| L (default) | 224 × 224 px | 56 |
| XL | 256 × 256 px | 60 |
| XXL | 320 × 320 px | 64 |

## What is written to the chain

The artwork is an ordinary `comment` operation. Its body is a single data URI, and nothing else:

```text
data:image/webp;base64,UklGRl4gAABXRUJQVlA4TFEgAAAv…
```

Its `json_metadata` carries the rest:

```json
{
  "app": "pixagram/3.0.2",
  "format": "image",
  "tags": ["pixelart", "retro"],
  "image": [],
  "description": "…",
  "nsfw": false,
  "license": { "type": "PIXA_LICENSE", "version": "1.0", "…": "…" }
}
```

The licence record is described in [Permanence and Provenance](permanence-and-provenance.md#licence).

All 141 artworks published from 2026-09-04 to 2026-10-04 took this form exactly: one lossless WebP per post. By 2026-10-05, 8 of them had been deleted in the app and 133 still held their image. Avatars are another matter: older documentation mentions PNG, and some profile pictures are PNG, but posts are WebP.

## How large an artwork can be

| Limit | Value | Set by |
|---|---|---|
| Post body | No limit of its own | Chain |
| Whole transaction | About 2 MiB at the current block size | Witnesses' median vote ([Chain Parameters](../11-reference/chain-parameters.md#transaction-and-block-size)) |
| Request to `api.pixagram.com` | About 1 MiB | The node's server |
| Artwork size in the app | No byte limit. Converted pictures follow the size presets above; pixel art that passes through, and quantized pictures, can be larger. | App |

Size matters in another way: every byte costs [Resource Credits](../04-tokens-and-economy/resource-credits.md). On 2026-10-05, publishing a 26 kB artwork cost about 3.8 million credits. That is a day's recharge for about 19 Pixa Power, so an account with 120 Pixa Power could publish about six a day.

**Editing writes the image again.** When you edit an artwork's title, tags or description, the app re-sends the whole image, so the edit costs as much as publishing did.

## Images that live elsewhere

| Image | Where it lives | On chain? |
|---|---|---|
| Artworks | Inside the post body | Yes |
| Profile pictures | Inside the account's profile data, as pixel art of at most 48,000 bytes | Yes |
| Community avatars | Inside the community account's profile data | Yes |
| Blog cover | A small SVG gradient inside the post's metadata | Yes |
| Images inside blog posts | Uploaded to Arweave through a project service (WebP of at most about 99 kB), then linked from the post | **No.** The post holds a link. |
| Images from other websites | Linked by address, shown through the app's image proxy | **No** |
| Search results | Copies kept by the search service | **No.** They are a cache, not the record. |

Arweave is a separate permanent-storage network, so the stored file does not depend on a Pixagram server. The app still uploads blog images through a project service, and shows them, like every linked image, through the project's image proxy. They are not part of the Pixa chain, and these pages never describe them as on chain.

## Display

The app shows artworks enlarged with pixel-art scalers (xBRZ by default, or hex, CRT or triangle). You can download the original or a watermarked enlargement. Scaling happens only on your screen. The stored artwork is always the original small image.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Typical image in a post | A link to an image host | The image itself, as a data URI |
| Image format | Any; the host decides | Lossless WebP for artworks |
| Image cost | Hosting paid by a company | Resource Credits, paid by the author's stake |
| Images in long posts | Links | Links (Arweave) |

## Sources

- **App**, commit [`ca1d157`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52):
  - publishing: [`NewPost.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js)
  - size presets: [`file2imgd.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/pix2art/file2imgd.js)
  - AI conversion: [`AI.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/pix2art/AI.js)
  - WebP encoding: [`encodeImage.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/encodeImage.js)
  - Arweave uploads: [`arweaveImage.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/lexical/arweaveImage.js)
- **Chain survey**: `bridge.get_ranked_posts` (sort `created`) and `condenser_api.get_content`, read on 2026-10-05; the largest body is in block 65,406.
- **Resource Credits**: [Resource Credits](../04-tokens-and-economy/resource-credits.md).
