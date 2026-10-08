# NFTs and Marketplace

> **Status: Planned (2027).** Buying and selling artworks on chain is on the roadmap for 2027. Nothing on this page runs yet, except what is marked as live. Last updated 2026-10-08.

Pixagram already records each artwork on chain, with its author and its licence. What it does not have is a way to own, transfer or sell an artwork as a distinct asset. This page says what exists today, what is planned, and which design questions are still open.

## What exists today

| Element | State |
|---|---|
| The artwork's bytes, author and time, recorded on chain | **Live** ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)) |
| A licence record with rights and a royalty percentage | **Live** as metadata; not enforced |
| Escrow transfers with a third-party agent, inherited from Steem | **Live** on chain; not offered in the app |
| An ownership token for an artwork, transfers of ownership, sales | **Not built** |
| The app's NFT tab on a post | A preview, marked "on its way" |

Owning the account that posted an artwork is not the same as owning the artwork as an asset. Today the post belongs to its author's account and cannot be passed to anyone else.

## What a post is and is not

The word "NFT" appears in the app and in the project's writing, so it is worth stating what the chain holds. A published artwork is a **post**: a `comment` operation signed by its author, carrying the image in its body and the author's metadata, including a licence record if the author chose one ([Operations Reference](../11-protocol-reference/operations-reference.md#content-and-voting), [Artwork Encoding Spec](../09-developers/artwork-encoding-spec.md)).

| A post is | A post is not |
|---|---|
| A permanent, dated, signed record that this account published these bytes | A token: there is no ownership record, no owner field, nothing that can be transferred |
| Editable by its author, who can mark it deleted in the app; the first version stays in its block | Transferable: the account can change hands, the post cannot leave the account |
| The bearer of a licence record, which states the author's terms in public | A sale, a contract or an enforcement of those terms; the chain reads none of them |
| Rewardable for 7 days through votes | Unique by any rule: the same image can be posted again by anyone, and nothing marks the copy ([PAPH](../15-search-and-indexing/paph.md)) |
| Readable by every program from the blocks | An asset in the sense of Hive-Engine or Ethereum tokens; the chain has no token standard |

The data model says the same from the other side: the chain knows posts; "artwork", "NFT", "licence" and "deleted" are readings of the metadata that the app and this documentation define ([Data Model](../11-protocol-reference/data-model.md#application-only-what-the-pixagram-app-defines)). The app's NFT tab is a preview of what the 2027 marketplace may show, not a view of anything on chain.

## What is planned

**For 2027: buying and selling artworks on chain.** The project's stated design direction is a marketplace built into the protocol itself, with no sidechain or separate smart-contract layer. NFT functionality would then share the chain's security and last as long as the chain does.

No specification or code for it has been published yet, so these pages describe no ownership model as decided.

## Proposed, not decided

A December 2025 article by the project set out these terms. They are proposals, recorded here so that readers can follow how they change:

| Proposal | Detail |
|---|---|
| First-sale fee | 10% of the price |
| Resale fee | 2.5% of the price |
| What happens to fees | Paid in PIXA and burned |

## Open questions

These need public answers before the marketplace ships, and this page will record them as they are settled:

1. **What is owned?** The post itself, or a token that points to it? Can a deleted or edited post still be sold?
2. **How does a sale settle?** In PIXA, in PXS, or both? With an escrow step?
3. **How do royalties work?** Does the royalty in each artwork's licence record become an enforced payment to the creator on resale, and at what rate?
4. **What does an owner receive?** The licence rights recorded with the work, or rights defined at sale?
5. **How are copies handled?** Without an originality check, someone could sell another person's work ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md#provenance)).
6. **What does it cost to use?** Do the new operations draw on Resource Credits, like posting, or carry fees?

## Where the idea comes from

The idea goes back to Steem's first year:

- **2016.** Steem's early plan, "Steemit's Evil Plan for Cryptocurrency World Domination", put a marketplace as its second phase, after a currency.
- **Escrow.** Steem built escrow payments into its protocol, letting a third party release or return a payment. Its 2017 Bluepaper describes them, and Pixa inherits them.
- **2025.** The July 2025 edition of the Steem whitepaper describes "social commerce with escrow payments".

Steem built escrow, but never a marketplace. Pixagram's aim is to build one for a kind of good it can store completely: the artwork itself.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Marketplace | Proposed in 2016; on Hive, built by second-layer apps | Planned in the protocol for 2027 |
| What a sale could transfer | A token that refers to off-chain data | An artwork whose bytes are on chain |
| Escrow operations | Available | Available |

## Sources

- Roadmap: [Roadmap](../01-start-here/roadmap.md).
- Proposed fees and design direction: "How Pixagram Completes the Vision for Blockchain World Domination", LinkedIn, 2025-12-20.
- [Steemit's Evil Plan for Cryptocurrency World Domination](https://steemit.com/steem/@dan/steemit-s-evil-plan-for-cryptocurrency-world-domination), 2016-07-06.
- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf), July 2025 edition: "Social Commerce with Escrow Payments"; [Steem Bluepaper](https://steem.com/steem-bluepaper.pdf) (2017): "Payments Through Escrow".
- **App**: NFT preview in [`PostDialog.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PostDialog.js).
