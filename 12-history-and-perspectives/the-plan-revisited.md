# The Plan Revisited

> **Status: Historical.** Larimer's three-phase plan for Steem (2016-07-06), what Steem, Hive and Pixa built of it, and the claims of Pixagram's essay of 2025-12-20 checked against the chain. Last checked 2026-10-06.

In July 2016, about three months after Steem's first block, Dan Larimer set out a plan for it in three phases: a currency, then a marketplace, then sidechains and smart contracts. In December 2025, an essay by Pixagram's co-founder argued that Pixagram completes that plan. This page sets the plan beside the record of the ten years since, then checks the essay's claims against the chain and the code. It quotes both and reports what the record shows.

## The plan, 2016

Larimer published "Steemit's Evil Plan for Cryptocurrency World Domination" as @dan on 2016-07-06. Its premise:

> The real money isn’t in blogging, content generation, or voting. The real money is found in bootstrapping a digital currency.

And its method:

> A blogging platform that makes it possible for everyone to earn their way in is just a trojan horse. It is a means of hiding the vegetables (honest money) in the food (fun content).

| Phase | In the plan's words | What it relied on |
|---|---|---|
| **1. Bootstrap a Stable Currency** | "establishing a price stable currency … This is the Steem Dollar." It would be "backed 20 to 1 by Steem" and pay "interest far beyond what the banks pay". | Posting rewards, to put the currency in people's hands, and a liquid market between it and STEEM |
| **2. Bootstrap a Marketplace** | "A successful marketplace needs two things": people and money. Steemit was "filling their pockets with fresh steem dollars." | In a reply the same day: "Once we have private messaging we will have a classified tag … We will add escrow support at the blockchain level." |
| **3. Sidechains, Smart Contracts and SmartCoins** | "Think of a side-chain as a Facebook app. It will allow developers to build new games. It will allow people to issue their own currencies." | A working currency, a community and a market. "Unlike other smart contract platforms, Steem will have no fees!" |

## What was built

| The plan | Steem, 2016–2020 | Hive, from 2020 | Pixa, 2026-10-06 |
|---|---|---|---|
| **A price-stable currency, earned by posting** | Steem Dollars (SBD), paid with author rewards. From hardfork 14 (2016-09-20), printing was limited and a haircut reduced conversions under stress. SBD closed at 13.76 USD on 2017-12-19 and at 0.517 USD on 2019-11-13. | Hive Dollars (HBD), convertible both ways since 2021, with interest on savings and a stabilizer paid by Hive's fund. From 2025-10-07 to 2026-10-02, HBD traded between 0.83 and 1.10 USD. | PXS promises no price. It is a Big Mac referenced supracoin, paid with author rewards and convertible both ways, with no interest and no stabilizer. |
| **A marketplace for goods and services** | Not built | Built by second-layer apps, not by the protocol | Buying and selling artworks is planned in the protocol for 2027 |
| **Private messaging and a "classified" tag** | No messaging on chain. An optional node plugin, archived in 2017, read messages sent as `custom_json`; steemit.com offered neither on-chain messages nor a classified section. | No messaging operation in the protocol | None. Transfer memos in the app are public. |
| **Escrow at the blockchain level** | Proposed on 2016-07-07 and activated with hardfork 14 on 2016-09-20. In use by 2017-02-11. | Inherited | Inherited. The app does not offer it. |
| **Sidechains** | Steem Engine, launched on 2019-02-07 by @aggroed, @yabapmatt and @harpagon. Its own software validates `custom_json` operations posted to Steem. | Hive Engine, running on Hive since 2020-03-25 | None |
| **Smart contracts** | None on the chain itself; Steem Engine ran them on its sidechain | None on the chain itself, as of Hive 1.28.7 | None |
| **People issuing their own currencies** | Smart Media Tokens: announced on 2017-09-28, postponed on 2019-03-11, never activated | Tokens on Hive Engine | None |
| **"No fees"** | Most operations carry no fee. Resource Credits replaced bandwidth limits with hardfork 20 (2018-09-25). | Same | Same. Opening an account, creating a proposal and converting PIXA to PXS each cost a fee. <!-- retired-ok --> |

## What the record shows

1. **The currency came first, as planned, and its price was never fixed.** Steem paid SBD with author rewards; SBD closed at 13.76 USD on 2017-12-19 and at 0.517 USD on 2019-11-13. Hive narrowed HBD's range with conversion both ways, interest and active trading ([From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md#what-the-record-shows)).
2. **Escrow shipped within three months; no protocol gained a marketplace.** The operations Larimer promised have been in the protocol since 2016-09-20, and Pixa still carries them. Marketplaces on Hive came from second-layer apps, and no classified section or messaging followed ([NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md#where-the-idea-comes-from)).
3. **Phase 3 was built beside the chain, not in it.** Smart contracts and user-issued tokens came from Steem Engine, a third party's sidechain. Smart Media Tokens never launched.

On Pixa, PXS is live and promises no price. Buying and selling artworks is planned in the protocol for 2027, with no specification published ([NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md#what-is-planned)).

## The 2025 essay, checked

Matias Affolter, Pixagram's co-founder and CTO, published "How Pixagram Completes the Vision for Blockchain World Domination" on Pixagram's LinkedIn page on 2025-12-20 ([Essays](essays.md)). It was written before mainnet, and several of its figures describe plans that have since changed. Each claim below is checked against the chain and the code as of 2026-10-06.

**About Larimer and Steem**

| The essay | The record |
|---|---|
| Larimer published "Steemit's Evil Plan for Cryptocurrency World Domination" in 2016, in three phases | Correct: 2016-07-06 |
| The marketplace, the escrow system and the classified section he promised "never happened" | Escrow did. It activated with hardfork 14 on 2016-09-20, and Pixa has it. The classified section and private messaging were never built. |
| Larimer wrote "Why Every Blockchain Needs a Constitution" and "How to Dodge Bullets - Creating your own Reality" | Correct. @dan posted both on 2016-07-01. |
| Larimer wrote "How Social Media's Predictive Algorithms Are Perpetuating Division Among The People" (2017) | Not Larimer. @son-of-satire posted it on 2017-01-27. |

**About Pixagram**

| The essay | The chain on 2026-10-06 | Details |
|---|---|---|
| PXS is "pegged to the Big Mac Index" | PXS promises no price and has no peg. It is a Big Mac referenced supracoin: conversions settle at the witnesses' median feed, reduced by a haircut when collateral is thin. | [PXS at a Glance](../05-pixa-supra/pxs-at-a-glance.md) <!-- retired-ok --> |
| "Each witness manually selects their country's Big Mac price" | Not today. At any one time, every witness has published the same feed: since 2026-09-04 17:39 UTC, the US Big Mac price in The Economist's index divided by a placeholder price for PIXA of 0.12 USD. The agnostic feed would let each witness declare a local price. | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#what-it-has-read-since-genesis) |
| PXS is "backed by a minimum 300% reserve of liquid PIXA tokens", with "an aspirational target of 1000%" | No reserve is held. The chain stops printing PXS when the PXS held outside the treasury reaches 20% of the combined value of that PXS and all PIXA, a collateral ratio of 4, and reduces conversions with a haircut below a ratio of 7/3. The design notes' corridor runs from about 3× to 10×. | [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#corridor-and-thresholds-design-and-chain) <!-- retired-ok --> |
| Witnesses "must maintain the PixaFlat peg" | Witnesses publish a price feed. Nothing defends a value. | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md) <!-- retired-ok --> |
| The marketplace is "nearly realized", with fees of 10% on first sales and 2.5% on resales, paid in PIXA and burned | Buying and selling artworks in the protocol remains the plan, for 2027. No specification has been published, and the fees are proposals. | [NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md#what-is-planned) |
| "Layer-1 native NFT integration … built directly into the blockchain protocol" | No NFT operation exists in hived 1.29.0. The app's NFT tab is a preview. | [operations.hpp:15-74][ops] |
| Artworks are "encoded in Base64 within the post body itself" | Correct. The body of an artwork post the app publishes is one lossless WebP image, written as a base64 data URI. Images inside blog posts are links to files hosted elsewhere; the editor uploads them to Arweave. | [Artwork Encoding Spec](../09-developers/artwork-encoding-spec.md) |
| "lossless WebP and PNG encoding" | The app writes artworks as lossless WebP only. | [Artwork Encoding Spec](../09-developers/artwork-encoding-spec.md) <!-- retired-ok --> |
| "up to 10,000 transactions per second" | No benchmark has been published. Capacity is bounded by the block size: 2,097,152 bytes every 3 seconds today. | [Chain Parameters](../11-reference/chain-parameters.md#transaction-and-block-size) <!-- retired-ok --> |
| The Decentralized Pixa Fund receives "17.5% of inflation rewards" | The nominal share is 15% of issuance. | [Chain Parameters](../11-reference/chain-parameters.md#issuance) <!-- retired-ok --> |
| "No Pixagram executive … can unilaterally access these funds" | Correct for the protocol: no one holds the fund's keys, and the chain pays only proposals that stake-weighted votes rank above the return proposal. On 2026-10-05, four accounts voted for the funded proposal, and one account set the threshold. | [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md#what-to-keep-in-mind) |
| A foundation, "potentially Swiss or Panamanian", should stand behind the constitution | The Pixa Omnibus Foundation (Cayman Islands) stewards the protocol and has not adopted a constitution. Pixa Rex S.A. (Panama) operates the app. | [Who Does What](../01-start-here/who-does-what.md) |
| Five constitutional principles | They remain a draft. | [Constitution](../07-governance/constitution.md#the-five-principles-draft) |
| "The proof-of-brain consensus rewards quality, not controversy" | Proof-of-Brain allocates rewards; DPoS orders the blocks. Which posts it rewards depends on who votes: on 2026-10-05, 21 accounts had votes large enough to move rewards. | [Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md#the-figures-on-2026-10-05) |
| Pixel artworks are "typically 3-30 kB" | Broadly consistent: artwork posts from 2026-09-04 to 2026-10-04 had a median body of about 26 kB. The largest so far is 497,479 bytes. | [Chain Parameters](../11-reference/chain-parameters.md#transaction-and-block-size) |
| "By May 2025, we will unveil a pre-alpha social media marketplace alongside the alpha testnet" | Mainnet launched on 2026-09-04 with the social network. The marketplace is planned for 2027. | [Roadmap](../01-start-here/roadmap.md) |
| The NFT market grew from "$380,000 in revenue in 2018 to projected $6.7 billion by 2028", and "up to 80%" of NFTs on some platforms are "allegedly fake or copies" | The essay gives no source. These pages do not use the figures. | — |
| "Learn more: pixagram.io \| pixa.pics" | The app is at pixagram.com and the developer pages are at pixa.org. pixa.pics is the pixel editor that the app opens. | [Style Guide](../13-about/style-guide.md#retired-names-and-claims) <!-- retired-ok --> |

## Sources

- **The plan:** Dan Larimer, "[Steemit's Evil Plan for Cryptocurrency World Domination](https://steemit.com/steem/@dan/steemit-s-evil-plan-for-cryptocurrency-world-domination)", 2016-07-06 18:52 UTC, and his [reply on the marketplace](https://steemit.com/steem/@dan/steemit-s-evil-plan-for-cryptocurrency-world-domination#@dan/re-cryptoctopus-re-dan-steemit-s-evil-plan-for-cryptocurrency-world-domination-20160706t195140853z), 19:51 UTC. The text was read with `condenser_api.get_content` on a Hive API node; Steem's history before 2020 is the same on both chains.
- **Larimer's other posts:** "[Why every Blockchain needs a Constitution](https://steemit.com/blockchain/@dan/why-every-blockchain-needs-a-constitution)" and "[How to Dodge Bullets - Creating your own Reality](https://steemit.com/philosophy/@dan/how-to-dodge-bullets-creating-your-own-reality)", both 2016-07-01.
- **The essay on social media:** @son-of-satire, "[How Social Media's Predictive Algorithms Are Perpetuating Division Among The People](https://steemit.com/life/@son-of-satire/how-social-media-s-predictive-algorithms-are-perpetuating-division-of-the-people)", 2017-01-27.
- **Escrow:**
  - Larimer, "[Escrow SIP - Steem Improvement Proposal](https://steemit.com/sip/@dan/escrow-sip-steem-improvement-proposal)", 2016-07-07, and [steemit/steem issue #143](https://github.com/steemit/steem/issues/143), "Add Escrow Operations".
  - @steemitblog, "[Steem 0.14.1 Released - Hardfork Postponed until 9/20/2016](https://steemit.com/steem/@steemitblog/steem-0-14-1-released-hardfork-postponed-until-9-20-2016)", 2016-09-13.
  - Hardfork 14 in Hive's code: scheduled for 2016-09-20 15:00 UTC ([0_14.hf:21-22][hf14-21]) and activated in block 5,137,542 ([hardfork_block.hpp:16][hfb-16]). Hive 1.28.7 still lists issue 143 among hardfork 14's changes ([0_14.hf:5][hf14-5]).
  - An `escrow_transfer` was in use by 2017-02-11: Steem block 9,284,729, at 21:02 UTC (`condenser_api.get_ops_in_block`).
- **Messaging and classifieds:** Steem's optional `private_message` plugin, [at release 0.14.2](https://github.com/steemit/steem/tree/b0e3644cd5cc4aae861348054df488915c2da472/libraries/plugins/private_message), was moved to `legacy_plugins` on 2017-08-03. The code of steemit.com, [steemit/condenser](https://github.com/steemit/condenser), searched at snapshots from 2016-09 to 2020-03, has no classified section and no messaging.
- **Smart Media Tokens:** @ned, "[Announcing: Smart Media Tokens (SMTs)](https://steemit.com/steem/@ned/announcing-smart-media-tokens-smts)", 2017-09-28; @steemitblog, "[SMTs Release Dates!](https://steemit.com/steem/@steemitblog/smts-release-dates)", 2018-08-15, updated on 2019-03-11 with the delay. On 2026-10-06, `condenser_api.get_config` on a Steem node reported version 0.23.0 and `STEEM_ENABLE_SMT: false`.
- **Steem Engine and Hive Engine:** @aggroed, "[Introducing Steem-Engine.com (smart contracts and token creation on Steem)](https://steemit.com/steemengine/@aggroed/introducing-steem-engine-com)", 2019-02-07, and "[Hive-Engine Update](https://peakd.com/hive-engine/@aggroed/hive-engine-update)", 2020-03-25.
- **The operations each chain accepts:** Hive 1.28.7, [operations.hpp:15-74][hive-ops]; Pixa 1.29.0, [operations.hpp:15-74][ops]. Neither defines an operation for contract code, NFTs or messages.
- **SBD and HBD prices:** [From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md#sources).
- **The essay:** Matias Affolter, "[How Pixagram Completes the Vision for Blockchain World Domination](https://www.linkedin.com/pulse/how-pixagram-completes-vision-blockchain-world-domination-8ntve/)", LinkedIn, 2025-12-20.

[ops]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/operations.hpp#L15-L74
[hive-ops]: https://github.com/openhive-network/hive/blob/1584099c3054a97f02abfb4788b23f02eea98728/libraries/protocol/include/hive/protocol/operations.hpp#L15-L74
[hf14-5]: https://github.com/openhive-network/hive/blob/1584099c3054a97f02abfb4788b23f02eea98728/libraries/protocol/hardfork.d/0_14.hf#L5
[hf14-21]: https://github.com/openhive-network/hive/blob/1584099c3054a97f02abfb4788b23f02eea98728/libraries/protocol/hardfork.d/0_14.hf#L21-L22
[hfb-16]: https://github.com/openhive-network/hive/blob/1584099c3054a97f02abfb4788b23f02eea98728/libraries/protocol/include/hive/protocol/hardfork_block.hpp#L16
