# Posting and Rewards

> **Status: Live.** Checked against the chain at block 895,415 and the app at commit `ca1d157` on 2026-10-05.

This page follows a post from publication to payout. It covers what a post is on chain, how its rewards are split and in which tokens, which options exist, and what happens when you edit or delete it.

## What a post is

Every post and reply is a `comment` operation signed with the author's posting key.

- **Posts and replies.** A post is a comment with no parent; a reply names the comment it answers.
- **Category.** A post's first tag is its category, or, inside a community, the community's name.
- **Replies earn too.** Every reply has its own seven-day payout, paid from the same reward fund as posts.

The Pixagram app publishes two kinds of post:

| Kind | Body | Where it appears |
|---|---|---|
| **Artwork** | Exactly one `data:image/webp;base64,…` image ([Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md)) | Feeds and profiles |
| **Blog post** | Markdown text, with images linked from Arweave | A community, chosen by the author |

The app tells them apart by the body: a body that starts with `data:image/` and contains no markup is an artwork.

## The life of a post

1. **Publish.** The post is in the chain from the next block onward.
2. **Seven days of voting.** Members can vote until payout. Votes cast in the last 12 hours count for less, shrinking toward zero at the deadline ([Voting and Curation](voting-and-curation.md#late-votes)).
3. **Payout.** Exactly seven days after publication, the chain computes the post's share of the reward fund ([Proof-of-Brain](proof-of-brain.md)). A payout worth less than 0.020 PXS is not made.
4. **Claim.** The rewards land in each recipient's reward balance. You move them into your wallet with a claim, which the app offers as a button.

The pending amount the app shows during the week is an estimate. It moves as votes arrive and as other posts cash out.

## Who receives what

| Recipient | Share of the post's payout | Paid in |
|---|---|---|
| Author | 60%, minus beneficiaries | Half PXS, half Pixa Power by default. The PXS half is limited by the print rate. |
| Beneficiaries | Their named share of the author's 60% | The same split as the author, except the fund, `pixa.omnibus`, which is paid entirely in PXS |
| Curators | 40% | Pixa Power only, divided by curation weight |

- **The print rate.** PXS promises no price. The print rate sets how much of the PXS half is created as PXS. It is 100% while PXS outside the treasury stays under 20% of the combined value. If PXS ever passed that line, the PXS half would be paid in liquid PIXA instead ([Chain Parameters](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). On 2026-10-05 that share was about 0.12% (`condenser_api.get_dynamic_global_properties`).
- **Unclaimed curation stays in the fund.** If no one curates a post, or its author switched curation off, the curators' 40% stays in the reward fund. It is not passed to the author.

**A real payout.** On 2026-10-05, a post paid out 22.272 PXS-equivalent, valued at the placeholder median feed of 51.833 PIXA per PXS:

- **Author:** 6.681 PXS and 346.337997 VESTS of Pixa Power.
- **Its two curators:** 461.781996 VESTS between them.

That is exactly 60/40, with the author's share split half and half (block 891,898).

## Options the chain offers

An author can attach `comment_options` to a post. Each option can only make the post's terms less generous, never more, and most must be set before the first vote.

| Option | Default | Effect |
|---|---|---|
| `max_accepted_payout` | 1,000,000 PXS | A cap on the payout. Set it to `0.000 PXS` to decline rewards entirely. |
| `percent_hbd` (`percent_pxs` through the public API) | 10000 | The share of the author's liquid half paid as PXS. `0` means everything is paid as Pixa Power. |
| `allow_votes` | true | When false, upvotes are rejected; downvotes still work. |
| `allow_curation_rewards` | true | When false, voters earn nothing from this post. |
| `beneficiaries` | none | Up to 8 accounts, each with a share of the author reward |

**The Pixagram app sets none of these today.** Every post it publishes uses the defaults, with no beneficiaries. Its "preferred payout" setting has no effect yet. Other apps, and any custom transaction, can use them.

## Editing and deleting

- **Editing** re-sends the post with the same permlink. The chain keeps every version in its history. When you edit an artwork's title, tags or description, the app re-sends the whole image too, so each edit writes another copy of it into the chain.
- **Deleting in the app** replaces an artwork's body with the word `deleted` and marks the post as deleted in its metadata. The app then hides it from feeds and profiles. **The version first published stays in its block.** Anyone reading the chain's history can still see it.
- **Deleting a reply** with the chain's own `delete_comment` works only before payout, while the reply has no replies of its own and no net positive votes. Even then, the reply stays in the block where it was published.

## Limits

The chain's limits are on [Chain Parameters](../11-reference/chain-parameters.md#posts-and-comments):

- 5 minutes between top-level posts
- a title under 256 bytes
- a body bounded only by the transaction size

The app adds its own limits for artworks:

- a title of at most 24 characters
- an optional description of at most 1,024 characters
- 1 to 5 tags of at least 3 characters each

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Payout window | 7 days | 7 days |
| Author / curator split | 50 / 50 | 60 / 40 |
| Author payout tokens | Half HBD, half Hive Power | Half PXS, half Pixa Power |
| Curation paid in | Hive Power | Pixa Power |
| Artworks | Links to image hosts | Stored inside the post body |

## Sources

- **Payout routing**
  - Author and beneficiary splits: [database_comment.cpp:249-300](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_comment.cpp#L249-L300).
  - Curators paid in Pixa Power: [database_comment.cpp:151-188](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_comment.cpp#L151-L188).
  - Print rate: [database.cpp:965-1009](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L965-L1009).
- **Options**: [hive_evaluator_social.cpp:138-173](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L138-L173); beneficiary rules, including no earlier votes and at most 8: [hive_evaluator_social.cpp:118-135](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L118-L135).
- **App**
  - Publishing: [`NewPost.js:3374-3440`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/NewPost.js#L3374-L3440).
  - Deleting: [`EditPostDialog.js:424-490`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditPostDialog.js#L424-L490).
- **Live chain**: `author_reward` and `curation_reward` operations in block 891,898; `condenser_api.get_content` for a post's options.
