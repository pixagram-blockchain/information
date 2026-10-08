# Censorship Resilience and Moderation

> **Status: Live.** Checked against the chain, the indexer at commit `5765e21` and the app at commit `ca1d157` on 2026-10-05.

Two layers decide what you see on Pixagram, and they follow different rules. The chain records whatever valid operations witnesses include in blocks, and it cannot forget them. The apps and indexers that read the chain choose what to show. Censorship resilience comes from the first layer; moderation happens in the second. This page explains both, and what each means for what you publish.

## What the chain guarantees

- **Inclusion.** Any valid, signed operation can be included in a block. Witnesses take turns producing blocks, so one witness refusing a transaction only delays it until the next slot. This guarantee weakens if a coordinated majority of the scheduled witnesses refuses. On 2026-10-05 the schedule had 9 witnesses (`condenser_api.get_witness_schedule`).
- **Permanence.** A block that has become irreversible is never rewritten. Every edit and every "deletion" is a new operation added to the history; the original stays.
- **Publicity.** Everything on chain is readable by anyone running a node or calling an API: posts, votes, transfers, balances and profile data. Only memos encrypted with a memo key keep their content private.

## What the chain does not do

- **Judge content.** The chain checks signatures, formats and limits, never meaning.
- **Delete.** Nothing removes data from past blocks. This includes data you later regret, and data that others may have a legal right to have removed.
- **Keep secrets.** The chain itself has no private posts, private follows or hidden balances.

## What the Pixagram app and the indexer do

| Tool | What it does | Where it is enforced |
|---|---|---|
| **Sanitizer** | Strips unsafe markup, scripts and malformed images before anything is displayed. It checks each image's real type and size, and screens SVG images against an allowlist. An artwork that fails inspection is shown as a plain card. | App, on your device |
| **NSFW flag** | The author can mark an artwork as not safe for work, and this is stored in the post's metadata. Before publishing, an on-device model turns the flag on when it is at least 40% confident, unless the author has already set it. It never blocks publishing. | Flag on chain; model in the app |
| **NSFW display** | By default, flagged posts are hidden from feeds and profiles. If you choose to show them, they are blurred until you also turn blurring off. While filtering is on, the on-device model also checks each artwork as it is shown, and blurs any it rates at least 40% likely to be NSFW, flagged or not. | App setting, per device |
| **Toxicity hint** | An on-device model shows a gentle warning while you type a comment, title or description that may come across as toxic. It never blocks. | App, on your device |
| **Community mutes and pins** | Moderators can mute or pin posts in their community ([Communities](communities.md#moderation)) | Indexer (Hivemind) and app |
| **Downvotes** | Any account whose vote counts, which since hardfork 30 means more than 2.5 effective Pixa Power, can lower a post's payout ([Voting and Curation](voting-and-curation.md#from-vote-to-rshares)) | Chain, rewards only |
| **Deleted posts** | Posts the author deleted in the app are hidden from every list | App |

**Not available yet:**

- muting or blacklisting users
- reporting a post to community moderators (Hivemind supports flags; the app does not send them yet)
- any automated check for plagiarism

A perceptual-hash library for pixel art exists in the project's repositories but is not used by the app. The chain records who posted a work first, not who made it ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)).

## Other interfaces

Any website or app can read the chain and apply its own rules. If Pixagram's app hides something, another interface can still show it, and the reverse is also true. The Steem whitepaper puts it this way: individual websites "may censor content on their particular site, but content published on the blockchain is inherently broadcast traffic and mirrors all around the world may continue to make it available."

## Before you publish

- **Assume it is permanent and public.** Do not publish personal data, yours or anyone else's, that you might need removed. Editing or deleting cannot take it back out of the chain's history.
- **Respect others' rights.** Publish only work you made or have the right to share. The chain's record of who posted first can be used against a copier, and against you.
- **Use the NSFW flag honestly.** It is how other people's settings protect them.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Chain-level censorship resistance | Rotating witnesses; no deletion | same; fewer witnesses today |
| Main front-end safety tools | Varied by front-end | On-device NSFW and toxicity models, sanitizer, community mutes |
| Content the chain stores in full | Text | Text, and the artwork itself |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Censorship".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §V.2 "Censorship Resilience by Design".
- **App**, commit [`ca1d157`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52):
  - sanitizer: [`sanitizer.js:1360-1466`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/sanitizer.js#L1360-L1466), and the image proxy, [`618-706`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/sanitizer.js#L618-L706)
  - NSFW model and threshold: [`nsfw.js:114-122`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/nsfw.js#L114-L122); blurring on display: [`PaperCard.js:71-86`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PaperCard.js#L71-L86)
  - toxicity hints: [`toxicity.js:30-72`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/toxicity.js#L30-L72)
  - NSFW auto-flag at publishing: [`NewPost.js:2571-2630`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L2571-L2630)
- **Hivemind**, commit [`5765e21`](https://github.com/pixagram-blockchain/hivemind/tree/5765e2113da3c2c3da3c056d7d795c51e925711a): community moderation operations, [`community.py:264-420`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/indexer/community.py#L264-L420).
