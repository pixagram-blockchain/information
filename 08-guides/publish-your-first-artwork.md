# Publish Your First Artwork

> **Status: Live.** One artwork per post, stored in the post itself. Described from the app's code of 2026-10-04. Last checked 2026-10-06.

This guide turns a picture into pixel art and publishes it from the app. The image is written into the post on the chain, not linked from somewhere else ([Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md)). You need an account and to be logged in ([Create an Account](create-an-account.md)).

## Before you start

- **One artwork every 5 minutes.** The chain refuses a second post within 5 minutes of the first ([Chain Parameters](../21-reference/chain-parameters.md#posts-and-comments)).
- **A picture to start from,** or a description of one: the app can also generate a picture.

## 1. Open the editor

Click **CREATE**, the round button with a camera. It sits at the bottom of the feeds (newest, hot, trending and promoted), of your personal feed and of your own profile, and it hides while you scroll down. The editor has three steps: Create, Adjust and Post.

## 2. Create: bring in a picture

Choose one of two tabs.

- **Convert picture.** Click to upload, drop a picture onto the editor, or paste it. Most image formats work, including HEIC photos from phones. **Edit picture** crops, rotates and flips it. Then click **Next**.
- **Create image.** Choose a shape (**Squared**, **Landscape** or **Portrait**), describe the picture under **Description**, and click **Generate**.

When a picture has 160 colours or more, the app asks "Transform your picture with AI?":

- **Transform** redraws it as pixel art in the style you pick: **Retro art**, **LucasArt style** or **VGA style**. **Your picture and its description leave your device:** they are sent to an AI service that the project runs on Hugging Face.
- **No, I don't want** converts it in your browser. Nothing leaves your device.

**Create image** always uses an AI service on Hugging Face, so your description is sent there.

## 3. Adjust: choose a size

Pick a size. Each one caps the number of pixels and of colours:

| Size | At most | Colours |
|---|---|---|
| S | 160 × 160 pixels | 48 |
| M | 192 × 192 pixels | 52 |
| L (default) | 224 × 224 pixels | 56 |
| XL | 256 × 256 pixels | 60 |
| XXL | 320 × 320 pixels | 64 |

The picture keeps its proportions: a wide picture becomes wider than tall, with the same number of pixels.

- **QUANTIZE** sets the downscale ratio and the number of colours yourself.
- **DOWNLOAD** saves a PNG copy, and **OPEN EDITOR** opens pixa.pics, a separate pixel editor.
- A picture that already has fewer than 160 colours skips the conversion and keeps its full size. The app says "Your artwork is already optimized for pixel art".

**Keep the artwork small.** The app sets no size limit, and larger sizes or more colours make larger posts. The next step shows the size under **Encoded Image**. The public node refuses requests over about 1 MiB; artworks so far have a median size of about 26 kB ([Chain Parameters](../21-reference/chain-parameters.md#transaction-and-block-size)).

## 4. Post: describe it

1. **Title.** Required, up to 24 characters.
2. **Description (Optional).** Up to 1,024 characters.
3. **Tags.** One to five, each followed by a space or Enter. A tag has at least 3 characters, starts with a letter, and uses only lowercase letters, digits and hyphens. **The first tag becomes the post's category, and it can never be changed.** It is also the first part of the post's address. Do not use a portal's name (`portal-…`) as the first tag: the app would then show the artwork as a text post.
4. **Not Safe For Work.** Switch it on for mature or sensitive content. The app checks the image on your device and switches it on by itself when the image looks sensitive; switch it off if that is wrong.
5. **NFT License.** Every artwork carries a licence, "PIXA NFT LICENSE 1.0". By default it grants a future holder 11 of 13 rights and visitors 2 of 4, with a 5% royalty. **Configure License** changes the rights, the royalty and the governing law. By default, the licence also lets visitors share the artwork with credit and use it to train AI models; untick that under **Configure License** if you do not want it. Your own default can be set in Settings, under **Licensing**. The licence is recorded with the work; nothing enforces it yet ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md#licence)).

The app may mark a title or description that could read as toxic. The check runs on your device and never stops you publishing.

## 5. Publish

Click **Publish**. If your keys are locked, the app asks for your vault password. The artwork is on the chain within seconds and appears in the feeds a few seconds later.

Two things are not chosen here:

- **A community.** An artwork is published under its first tag. Communities hold text posts written from the community's page ([Create a Community](create-a-community.md#post-in-your-community)).
- **How rewards are paid.** The chain's default applies: the author's share is paid half in PXS and half in Pixa Power, after 7 days. The **Preferred Payout** choice in Settings has no effect yet ([Posting and Rewards](../02-social-layer/posting-and-rewards.md#options-the-chain-offers)).

## After publishing

- **Edit.** Open the artwork's ⋮ menu and choose **Edit Details**, or open the artwork, then its info tab, **Manage** and **Edit post details**. You can change the title, the description, the tags except the first, the NSFW switch and the licence. The image cannot be replaced. Each edit writes the whole image to the chain again, so it costs as many Resource Credits as publishing did.
- **Hide.** The **Deleted** switch in **Edit Details** hides the artwork from every list and leaves the image in place. Switch it back to show the artwork again.
- **Delete.** In the ⋮ menu, choose **Delete Post**. **You cannot undo this.** The app replaces the image in the post with the word "deleted" and hides the post from every feed, profile and community page. The original stays in the chain's history of past blocks, and votes and payouts are not affected ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)).
- **No drafts.** Closing the editor before you publish discards the work: "Your current artwork will be lost."

## If something goes wrong

| The app says | What to do |
|---|---|
| "Title must be 24 characters or less …" | Shorten the title. |
| "At least 1 tag is required" | Add a tag. |
| "must start with a letter, min 4 chars", under the tags | The tag was not added. Start it with a letter, and use only lowercase letters, digits and hyphens; three characters are enough. |
| "Image not ready yet — please wait a moment and try again." | Wait until the image is encoded, then click **Publish** again. |
| "Please try again later", after **Transform** or **Generate** | The AI service did not answer. Try again, or choose **No, I don't want**. |
| A message that ends "You may only post once every 5 minutes." | Wait 5 minutes after your last artwork. |
| "Failed to publish post. Please try again." | Check your connection and try again. |

## Sources

- **The editor:** the CREATE button, [`CreateFab.js:21-35`][fab]; the three steps, the fields and their limits, [`NewPost.js:132-214`][np-132]; publishing, [`NewPost.js:3363-3441`][np-3363].
- **Conversion:** the sizes, [`file2imgd.js:196-292`][f2i]; the AI service, [`AI.js:84-154`][ai]; the lossless WebP encoding, [`encodeImage.js:5-49`][enc].
- **Checks on your device:** sensitive images, [`nsfw.js:250-357`][nsfw]; toxic wording, [`toxicity.js:25-96`][tox].
- **Licence:** [`pixa_license.js`][lic] and [`default_license.js:45-88`][dlic].
- **Editing and deleting:** [`EditPostDialog.js:860-956`][edit]; how a deleted post is recognised, [`constants.js:665-700`][del].
- **English text:** [`en.js:1514-1550`][en-1514] and [`en.js:750-762`][en-750].
- **Chain:** the 5-minute interval, [`hive_evaluator_social.cpp:214`][interval]; sizes and limits, [Chain Parameters](../21-reference/chain-parameters.md#transaction-and-block-size); the post's format, [Artwork Encoding Spec](../09-developers/artwork-encoding-spec.md).

[fab]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateFab.js#L21-L35
[np-132]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L132-L214
[np-3363]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L3363-L3441
[f2i]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/pix2art/file2imgd.js#L196-L292
[ai]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/pix2art/AI.js#L84-L154
[enc]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/encodeImage.js#L5-L49
[nsfw]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/nsfw.js#L250-L357
[tox]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/toxicity.js#L25-L96
[lic]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/pixa_license.js
[dlic]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/default_license.js#L45-L88
[edit]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditPostDialog.js#L860-L956
[del]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L665-L700
[en-1514]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1514-L1550
[en-750]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L750-L762
[interval]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L214
