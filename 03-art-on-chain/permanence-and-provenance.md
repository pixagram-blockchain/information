# Permanence and Provenance

> **Status: Live.** Checked against the chain and the app at commit `ca1d157` on 2026-10-05.

Two promises are often made for art on a blockchain: that it lasts, and that it proves who made it. This page says exactly how far the Pixa chain keeps each promise, and where it stops. It also describes the licence every artwork carries.

## Permanence

**How long an artwork lasts.** An artwork sits in a block, and blocks are copied by every node that keeps the chain's full history. The artwork lasts as long as someone keeps that history. No company has to stay in business and no image host has to keep a file. The record of the first Steem blocks of 2016 is still served today by nodes of the chains descended from it ([From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md)). Permanence on a chain is a matter of continued operation, not a guarantee. It is still a far stronger basis than a link.

**What irreversible means.** Within a few seconds a block becomes irreversible: enough witnesses have confirmed it that it will never be replaced ([Chain Parameters](../11-reference/chain-parameters.md#blocks-and-witnesses)). From then on, its contents never change.

**Edits and deletions leave past blocks unchanged.**

| You do | The chain records | What remains |
|---|---|---|
| Edit an artwork | A new `comment` operation with the same permlink | Every earlier version, in its block |
| Delete an artwork in the app | A new version whose body is `deleted`, marked as deleted in its metadata | The original image, in the block where it was first published |
| Delete a post or reply with `delete_comment` | A deletion, allowed only before payout, and only with no replies and no net positive votes. The post leaves the chain's current state and the API. | The original, in the block where it was published |

**Consequences**

- **Nothing can be withdrawn.** Personal data, a mistake, or a work you later want withdrawn will stay readable to anyone who looks at the history.
- **Interfaces can hide; the record cannot change.** An app can hide something, and it may be legally obliged to. The record stays as it is.

## Provenance

When you publish, the chain records:

- **Who:** the author's account, proven by a signature from its posting key.
- **When:** the block's number and timestamp. Blocks come every 3 seconds, so this is precise to within 3 seconds.
- **What:** the exact bytes of the image.
- **Which transaction:** an id anyone can look up.

**Checking it yourself.** These calls show the post as it is now, list the author's posts with the block each was written in, and fetch that block:

```bash
curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_content","params":["AUTHOR","PERMLINK"],"id":1}'
curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_account_history","params":["AUTHOR",-1,1000,2,0],"id":1}'
curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_block","params":[BLOCK_NUMBER],"id":1}'
```

**What provenance proves:**

- This account published these bytes at this time.
- No earlier post *on this chain* has the same bytes, if you search for them.

**What provenance does not prove:**

- **That the publisher made the work.** Anyone can publish a copy of someone else's image. The chain proves who posted first on this chain, not who created the work.
- **That the work is original.** The app does not check for copies yet. The project has published a perceptual-hash library for detecting near-identical pixel art, but nothing uses it so far.
- **Anything about other chains or the wider web.** An image posted earlier elsewhere has its own history there.

## Licence

Every artwork the app publishes carries a licence record in its metadata: the **PIXA NFT LICENSE 1.0**. The author can switch each right on or off. These are the defaults:

**Rights of the holder**

| Right | Default |
|---|---|
| Display for personal, non-commercial use | on |
| Commercial use | on |
| Social media or advertising | on (needs commercial use) |
| Printing on physical goods | on (needs commercial use) |
| Licensing to third parties, such as stock sites | **off** (needs commercial use) |
| Modifying or adapting | on |
| Public derivative works or remixes | on (needs modifying) |
| Minting the work or derivatives as new NFTs | **off** (needs modifying) |
| Use in virtual worlds, games, apps, music videos, films, exhibitions and education | on |

**Rights of visitors**

| Right | Default |
|---|---|
| Share with credit to the author | on |
| Share without credit | **off** |
| Modify and share under the same licence | **off** |
| Train or use in AI or machine-learning models | **on** |

The record also holds:

- **A royalty percentage**, 5% by default.
- **Governing-law fields:** a jurisdiction, a court and arbitration terms.

**Who enforces the licence.** The licence is a statement of the author's terms, recorded publicly with the work. The chain does not enforce it. In particular, no royalty is collected anywhere today, because there is no marketplace yet ([NFTs and Marketplace](nfts-and-marketplace.md)). Enforcing it is a matter for the law of the jurisdiction the author names. The governing-law fields are empty by default, and most artworks published so far leave them empty.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| What the chain records for an image | Usually a link | The image itself |
| Proof of who posted first | Yes, for the post's text | Yes, for the post and the artwork's bytes |
| Licence record | None by default | PIXA NFT LICENSE 1.0 in every artwork's metadata |
| Originality checks | None | None yet |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Shifting toward Blockchain-based Attribution".
- **App**, commit [`ca1d157`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52):
  - licence rights and defaults: [`pixa_license.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/pixa_license.js)
  - deletion: [`EditPostDialog.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditPostDialog.js)
- **Chain**: [`delete_comment` conditions](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L56-L75).
- **Perceptual hash**: [github.com/pixagram-blockchain/paph-js](https://github.com/pixagram-blockchain/paph-js), not used by the app.
