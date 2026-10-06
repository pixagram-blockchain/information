# Artwork Encoding Spec

> **Status: Live.** Describes the format the Pixagram app writes as `pixagram/3.0.2` (app commit `ca1d157`) and the checks it applies when it displays an artwork. Checked against the 159 most recent posts on 2026-10-05: all 136 artworks among them that still held their image follow it.

This page specifies how an artwork is stored on the Pixa chain, so that other programs can publish artworks the Pixagram app displays and read the ones it publishes. It covers the operation, the image in the body, the metadata, editing and deleting, and how to read an artwork safely. Why the format is what it is, and what it costs, is on [Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md).

In this spec, **must** marks what the app relies on to display a post as an artwork, and **should** marks what the app itself writes.

## The operation

An artwork is a top-level post: one `comment` operation, signed with the author's posting key, with no other operation needed.

| Field | Value | Chain rule | App rule |
|---|---|---|---|
| `parent_author` | `""` | empty for a top-level post | |
| `parent_permlink` | The category: the first tag | under 256 bytes, UTF-8 | equals `tags[0]`; **must not** be a community name (`portal-…`), because the app shows every post in a community as a blog post |
| `author` | The publishing account | an existing account, 3–16 characters | |
| `permlink` | Unique per author | under 256 bytes, UTF-8 | *should* be the title's slug and a millisecond timestamp, such as `peach-knight-1791211388189` |
| `title` | The artwork's name | under 256 bytes, UTF-8 | 1 to 24 characters |
| `body` | The image, as one data URI ([below](#the-body)) | non-empty UTF-8; the whole transaction under about 2 MiB | **must** be a valid image data URI; the app recognises an artwork by its body |
| `json_metadata` | A JSON object as a string ([below](#json_metadata)) | valid JSON | *should* contain `"format": "image"` |

**Slug rule.** The app lowercases the title, replaces every run of characters other than `a–z` and `0–9` with a hyphen, trims hyphens from both ends, keeps the first 24 characters and appends `-` and `Date.now()`. Readers must not rely on this form; any permlink of lowercase letters, digits and hyphens is valid.

**Payout options.** The app sends no `comment_options`, so every artwork has the chain's defaults: rewards allowed, curation allowed, `percent_pxs` 10000 (Hive's `percent_hbd`), maximum payout 1,000,000.000 PXS and no beneficiaries ([Posting and Rewards](../02-social-layer/posting-and-rewards.md#options-the-chain-offers)).

**Timing.** An account can publish one top-level post every 5 minutes ([Chain Parameters](../11-reference/chain-parameters.md#posts-and-comments)).

## The body

```text
body       = "data:image/webp;base64," payload
payload    = standard base64 of one WebP file, padded with "=", with no spaces or line breaks
WebP file  = "RIFF" size "WEBP" "VP8L" …   (the lossless format)
```

- **One image, nothing else.** The body *must* be the data URI alone: no text before or after it, no `<`, no line break.
- **Lossless WebP.** The app *should* write lossless WebP (the `VP8L` chunk), and every artwork in the survey is one. It encodes with libwebp's `lossless` and `exact` options, so every pixel, including fully transparent ones, keeps its exact colour.
- **Size.** The image is stored at its own size; there is no scaling factor in the format. Artworks on chain on 2026-10-05 measured from 91 to 2,160 pixels wide and 91 to 1,184 high. The body must fit in the transaction: about 2 MiB on chain, and about 1 MiB through the public API ([limits](../11-reference/chain-parameters.md#transaction-and-block-size)).
- **Cost.** Every byte costs the author [Resource Credits](../04-tokens-and-economy/resource-credits.md); a smaller file is cheaper.

The start of a real artwork's body, which decodes to `RIFF`, the file size, `WEBP` and `VP8L`:

```text
data:image/webp;base64,UklGRjhJAABXRUJQVlA4TCxJAAAvwUBAAL/BJ…
```

## `json_metadata`

The app writes these keys, in this order:

```json
{
  "app": "pixagram/3.0.2",
  "format": "image",
  "tags": ["nature", "travel"],
  "image": [],
  "description": "",
  "nsfw": false,
  "license": { "type": "PIXA_LICENSE", "version": "1.0", "…": "…" }
}
```

| Key | Type | Meaning | Rule |
|---|---|---|---|
| `app` | string | The writing app and its version | *should* name your app, such as `"my-app/1.0"` |
| `format` | string | `"image"` marks an artwork. Blog posts use `"markdown"` and replies `"text"`. | *should* be `"image"`; the app itself goes by the body, other readers by this key |
| `tags` | array of strings | 1 to 5 tags; the first is the category | each 3 or more characters, matching `^[a-z][a-z0-9-]*$` |
| `image` | array | Empty. Hive apps list image addresses here; the artwork is the body itself. | *should* be `[]` |
| `description` | string | The author's description | up to 1,024 characters; may be empty |
| `nsfw` | boolean | The author marks the artwork as not safe for work. The app hides such artworks by default ([Moderation](../02-social-layer/censorship-resilience-and-moderation.md#what-the-pixagram-app-and-the-indexer-do)). | *should* be present |
| `license` | object | The author's licence terms ([below](#the-licence-record)) | optional |
| `deleted` | boolean | Written by every edit in the app: `false`, or `true` once the author deletes the artwork ([below](#editing-hiding-and-deleting)). The app also reads `"true"`, `1` and a `deleted` tag as deleted. | absent on new posts |

### The licence record

The app writes the licence the author has set as default in Settings, or the one chosen for this artwork. What each right means is in [Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md#licence); the chain does not enforce any of it.

| Key | Type | Value |
|---|---|---|
| `type` | string | `"PIXA_LICENSE"` |
| `version` | string | `"1.0"` |
| `isCustomized` | boolean | `true` if the author changed the defaults |
| `royaltyPercentage` | number | 0 to 100. Nothing collects it today. |
| `governingLaw` | object | `jurisdiction`, `court`, `arbitrationRules`, `arbitrationLocation`: strings, often empty |
| `rightsConfiguration.holderRights` | object of booleans | `personal-display`, `commercial-use`, `social-media`, `physical-goods`, `third-party-licensing`, `modify`, `derivatives`, `mint-new-nfts`, `metaverse`, `games-apps`, `music-video-film`, `exhibitions`, `educational` |
| `rightsConfiguration.visitorRights` | object of booleans | `share-with-attribution`, `share-without-attribution`, `modify-and-share`, `ai-training` |

- **Writers** should include `license` only with terms the author has chosen. A licence record states the author's terms in public, permanently.
- **Readers** should treat a post without `license` as carrying no licence record, and should not show terms for it.

## Editing, hiding and deleting

| Action | What the app broadcasts | Effect |
|---|---|---|
| Edit the title, tags, description, NSFW flag or licence | A new `comment` with the same `author`, `permlink`, `parent_author` and `parent_permlink`; `json_metadata` is the stored object with the changed keys replaced; the body is the full image again | The edit replaces what readers see. The first version stays in its block. |
| Mark as deleted (the *Deleted* switch when editing) | The same, with `"deleted": true` added to `json_metadata` | The app hides the post everywhere. Reversible. |
| Delete (the card menu), or erase the image (when editing) | The same, with the body `deleted`; the card menu also adds `"deleted": true` | The image is gone from the current version. The first version stays in its block. |
| Remove from the chain's state | `delete_comment` | Only while the post has no replies and no net positive votes, and before payout. The app offers it for replies, not for artworks. |

The category (`parent_permlink`) cannot change in an edit. Edits of other kinds of post can carry a diff patch instead of a full body; the app never sends one for an artwork.

## Reading an artwork

1. **Fetch the post:** `bridge.get_post` with `{"author": …, "permlink": …}` returns `json_metadata` already parsed. `condenser_api.get_content` returns it as a string.
2. **Skip what is not an artwork.** The app's test: the body, trimmed, starts with `data:image/`, contains no `<` and no line break, and passes the checks in step 4. Posts the app writes also carry `"format": "image"`.
3. **Skip deleted artworks:** `json_metadata.deleted` is `true`, `"true"` or `1`, or `tags` contains `deleted`, or the body is `deleted`.
4. **Validate before decoding.** The app accepts a data URI only if all of these hold, and so should any reader that shows images to people. A body that fails them is not shown as an image.

   | Check | App limit |
   |---|---|
   | Form | `data:image/<type>;base64,<payload>`, nothing else |
   | Base64 | length a multiple of 4, padding only at the end |
   | Declared type | must match the file's first bytes; a WebP must start with `RIFF` … `WEBP` |
   | Length | at most 7,000,000 characters |
   | Dimensions | not zero; at most 40,000,000 pixels |

5. **Decode** the base64 payload to bytes. The result is a complete `.webp` file.

A complete reader in Python, using only the standard library. Save it as `get_artwork.py`:

```python
#!/usr/bin/env python3
"""Save one Pixagram artwork as a WebP file. Python 3.8+, standard library only."""
import base64
import json
import struct
import sys
import urllib.request

API = "https://api.pixagram.com"
PREFIX = "data:image/webp;base64,"


def rpc(method, params):
    request = urllib.request.Request(
        API,
        json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode(),
        {"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        reply = json.load(response)
    if "error" in reply:
        raise RuntimeError(reply["error"]["message"])
    return reply["result"]


author, permlink = sys.argv[1], sys.argv[2]
post = rpc("bridge.get_post", {"author": author, "permlink": permlink})
meta, body = post["json_metadata"], post["body"].strip()

deleted = meta.get("deleted") in (True, "true", 1) or "deleted" in meta.get("tags", [])
if deleted or not body.startswith(PREFIX):
    sys.exit("not an artwork, or marked deleted")
data = base64.b64decode(body[len(PREFIX):], validate=True)
if data[:4] != b"RIFF" or data[8:16] != b"WEBPVP8L":
    sys.exit("not a lossless WebP")

bits = struct.unpack("<I", data[21:25])[0]
width, height = (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
with open(f"{permlink}.webp", "wb") as out:
    out.write(data)
licence = meta.get("license", {}).get("type", "none")
print(f"@{author}/{permlink}: {width} x {height} px, {len(data)} bytes, licence {licence}")
```

```bash
python3 get_artwork.py tetiana schwyz-1791219064927
```

Expected output on 2026-10-05:

```text
@tetiana/schwyz-1791219064927: 295 x 222 px, 24392 bytes, licence PIXA_LICENSE
```

The app shows a post at `https://pixagram.com/<category>/@<author>/<permlink>`.

## Writing an artwork

This Node.js script encodes an image as lossless WebP with [sharp](https://sharp.pixelplumbing.com/) and publishes it with dpixa ([Developer Quickstart](developer-quickstart.md#2-set-up-a-nodejs-project)). With `DRY_RUN=1` it prints the operation instead of broadcasting it.

```bash
npm install @pixagram/dpixa@1.5.4 sharp@0.34.5
```

```js
// publish-artwork.js: publish a pixel-art image as a Pixagram artwork
// usage: node publish-artwork.js <author> <image.png> "<title>" <tag> [more tags]
//        with POSTING_WIF in the environment; DRY_RUN=1 prints the operation instead of broadcasting
const sharp = require("sharp");
const { Client, PrivateKey } = require("@pixagram/dpixa/dist/dpixa.js");

const client = new Client(["https://api.pixagram.com"]);

async function main() {
  const [author, file, title, ...tags] = process.argv.slice(2);

  // 1. The body: one lossless WebP, as a base64 data URI
  const webp = await sharp(file).webp({ lossless: true, exact: true, effort: 6 }).toBuffer();
  const body = "data:image/webp;base64," + webp.toString("base64");

  // 2. The permlink: the app's form, a slug of the title and a millisecond timestamp
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 24);
  const permlink = `${slug}-${Date.now()}`;

  // 3. The metadata: format "image" marks an artwork
  const json_metadata = JSON.stringify({
    app: "my-app/1.0",
    format: "image",
    tags,
    image: [],
    description: "",
    nsfw: false,
  });

  const op = { parent_author: "", parent_permlink: tags[0], author, permlink, title, body, json_metadata };
  if (process.env.DRY_RUN) {
    console.log({ ...op, body: `${body.slice(0, 40)}… (${body.length} characters)` });
    return;
  }
  const key = PrivateKey.fromString(process.env.POSTING_WIF || "");
  const { id } = await client.broadcast.comment(op, key);
  console.log(`accepted, transaction ${id}: https://pixagram.com/${tags[0]}/@${author}/${permlink}`);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

```bash
DRY_RUN=1 node publish-artwork.js your-account checker.png "Checkerboard" pixelart retro
```

Expected output, for a 16 × 16 two-colour checkerboard (the permlink's timestamp changes):

```text
{
  parent_author: '',
  parent_permlink: 'pixelart',
  author: 'your-account',
  permlink: 'checkerboard-1791231967754',
  title: 'Checkerboard',
  body: 'data:image/webp;base64,UklGRioAAABXRUJQV… (91 characters)',
  json_metadata: '{"app":"my-app/1.0","format":"image","tags":["pixelart","retro"],"image":[],"description":"","nsfw":false}'
}
```

To publish for real, read the posting key from the keyboard, so it stays out of your shell history, and run without `DRY_RUN`:

```bash
read -rsp 'Posting key: ' POSTING_WIF && export POSTING_WIF && echo
node publish-artwork.js your-account checker.png "Checkerboard" pixelart retro
unset POSTING_WIF
```

Expected output: `accepted, transaction <40 hexadecimal characters>: https://pixagram.com/pixelart/@your-account/checkerboard-<timestamp>`.

- **Feed it pixel art.** The script stores the image at its own size. Reduce photos and large images first; the app's converter is described in [Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md#from-picture-to-artwork).
- **No licence by default.** Add a `license` object only with terms the author chose.
- **Avoid renamed words in text.** Until the gateway is fixed, a title or description containing `pxs_balance` or another name it renames fails to broadcast ([known issue](differences-from-hive.md#known-issue-renames-inside-text)).

## Other images on chain

| Image | Where | Format |
|---|---|---|
| Profile picture | `posting_json_metadata.profile.profile_image` of the account, written with `account_update2` | A data URI of the uploaded file, at most 48,000 bytes, which must be pixel art |
| Community avatar | The community account's profile data | Same |
| Images in blog posts | Links in a `format: "markdown"` post | Not on chain ([Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md#images-that-live-elsewhere)) |

## Sources

- **App,** commit [`ca1d157`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52), under `src/js/`:
  - publishing: [`components/NewPost.js:3363-3430`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L3363-L3430); field limits at [132-142](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L132-L142); permlink at [244-253](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L244-L253)
  - encoding: [`utils/encodeImage.js:5-49`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/encodeImage.js#L5-L49)
  - recognising an artwork: [`utils/api/pixaproxyapi.js:824-832`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L824-L832) and [9797-9808](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L9797-L9808); posts in communities: [`pages/Profile.js:468-476`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/pages/Profile.js#L468-L476); validating it: [`utils/api/sanitizer.js:461-555`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/sanitizer.js#L461-L555)
  - editing and deleting: [`components/EditPostDialog.js:423-500`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditPostDialog.js#L423-L500) and [860-900](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditPostDialog.js#L860-L900); the edit helper: [`utils/api/pixaproxyapi.js:6319-6440`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L6319-L6440); deleted posts: [`utils/constants.js:683-700`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L683-L700); post addresses: [655-662](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L655-L662)
  - profile pictures: [`components/EditProfileDialog.js:773`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditProfileDialog.js#L773) and [959-986](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditProfileDialog.js#L959-L986)
- **Chain,** commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443): `comment` validation in [`hive_operations.cpp:123-138`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L123-L138) and JSON validation at [22-33](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L22-L33); `delete_comment` in [`hive_evaluator_social.cpp:56-75`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L56-L75).
- **Survey,** 2026-10-05: the 159 most recent posts from `bridge.get_ranked_posts` (sort `created`): 144 with `format: "image"`, 136 still holding an image, every one a `VP8L` WebP; 8 erased.
- **Tests,** 2026-10-05: the reader and the dry run above; a full artwork `comment` signed by dpixa matched the node's serialization (`condenser_api.get_transaction_hex`).
- **WebP format:** [WebP Container Specification](https://developers.google.com/speed/webp/docs/riff_container) and [Lossless Bitstream Specification](https://developers.google.com/speed/webp/docs/webp_lossless_bitstream_specification).
