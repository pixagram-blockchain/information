# Sources and Credits

> **Status: Live.** The code, documents, data and writing these pages cite, and the work Pixa is built on. Last checked 2026-10-06.

Each page cites its sources where it uses them. This page gathers them in one register: code with the commit cited and the licence its repository states, then documents, data, books and articles. Live values are not repeated here; each page gives the API call that returns them and the date it was read.

## Code

| Repository | What the pages draw from it | Commit cited | Licence stated in the repository |
|---|---|---|---|
| [pixagram-blockchain/pixagram](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443) | The chain node, hived 1.29.0: every protocol rule and number | `48f75a2`, 2026-09-18 | MIT |
| [pixagram-blockchain/pixagram-ui-dev](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52) | The app at pixagram.com: sign-up, keys, the artwork editor, the wallet, governance and communities | `ca1d157`, 2026-10-04 | GPL-3.0 (`LICENSE`); `package.json` says MIT |
| [pixagram-blockchain/hivemind](https://github.com/pixagram-blockchain/hivemind/tree/5765e2113da3c2c3da3c056d7d795c51e925711a) | The social layer: feeds, communities and roles | `5765e21`, 2026-08-18 | MIT |
| [pixagram-blockchain/dpixa](https://github.com/pixagram-blockchain/dpixa/tree/fddb47d677bf6b2364c1a7bcaba704208432071c) | The JavaScript library in the developer examples, a fork of dhive | `fddb47d`, 2026-05-01 | BSD-3-Clause-No-Military-License |
| [pixagram-blockchain/pixagram-node](https://github.com/pixagram-blockchain/pixagram-node/tree/7e57cca075d51a3ac1cf3065d367581a3efe56c6) | Node configurations, including the API node's plugins | `7e57cca`, 2026-09-22 | MIT |
| [pixagram-blockchain/witness](https://github.com/pixagram-blockchain/witness/tree/51938966c3714908a10f158be197064c2d16d94b) | The witness setup | `5193896`, 2026-09-16 | No licence file |
| [pixagram-blockchain/bigmac-feed](https://github.com/pixagram-blockchain/bigmac-feed/tree/c88c43c8b3b8e08ff472fe523b33277b9940ffb2) | The price feed the witnesses run | `c88c43c`, 2026-09-07 | No licence file |
| [pixagram-blockchain/bigmac-feed-agnostic](https://github.com/pixagram-blockchain/bigmac-feed-agnostic/tree/96b9d4a1f1a203d1fedbf603e7769f005c77cfba) | A feed witnesses may run instead: a local Big Mac price, a market price for PIXA and ECB exchange rates | `96b9d4a`, 2026-09-07 | GPL-3.0 |
| [pixagram-blockchain/witness-status](https://github.com/pixagram-blockchain/witness-status/tree/a376149c1c04e97d1b2391d4394699c6dc8c202c) | The witness status page | `a376149`, 2026-09-22 | MIT |
| [pixagram-blockchain/paph-js](https://github.com/pixagram-blockchain/paph-js) | PAPH, a perceptual hash for pixel art; not used by the app | Linked, not cited at a commit | MIT |
| [openhive-network/hive](https://github.com/openhive-network/hive/tree/1584099c3054a97f02abfb4788b23f02eea98728) | Hive's code, for comparison | Release 1.28.7, `1584099`, 2026-07-10 | MIT |
| [steemit/steem](https://github.com/steemit/steem/tree/b0e3644cd5cc4aae861348054df488915c2da472) | Steem's code: escrow and the private-message plugin; its [issue #143](https://github.com/steemit/steem/issues/143), "Add Escrow Operations" | Release 0.14.2, `b0e3644` | MIT |
| [steemit/condenser](https://github.com/steemit/condenser) | The code of steemit.com | Searched at snapshots from 2016-09 to 2020-03 | MIT (`package.json`) |
| [sharp](https://sharp.pixelplumbing.com/) | The image library in an encoding example | — | See its site |

## Documents

| Document | Edition | What the pages use it for |
|---|---|---|
| Steem whitepaper | [March 2016](https://web.archive.org/web/20160815131730/https://steem.io/SteemWhitePaper.pdf), archived | What Steem said at launch: Steem Dollars, rewards, the price feed |
| Steem whitepaper | [July 2025](https://steem.com/steem-whitepaper.pdf), steem.com | Steem's current description, including escrow payments |
| Steem Bluepaper | [2017](https://steem.com/steem-bluepaper.pdf) | Proof-of-Brain and escrow |
| Hive whitepaper | [2020](https://hive.io/whitepaper.pdf) | Resource Credits and what Hive changed |
| PXS design notes | Pixagram, June 2026; not published | The design of PXS, cited by section |
| WebP specifications | [Container](https://developers.google.com/speed/webp/docs/riff_container) and [lossless bitstream](https://developers.google.com/speed/webp/docs/webp_lossless_bitstream_specification), Google | The artwork format |
| Hive developer portal | [developers.hive.io](https://developers.hive.io/) | The API that Pixa shares with Hive |
| Docker documentation | [Merge Compose files](https://docs.docker.com/reference/compose-file/merge/) | Running an API node |

## Data

| Source | What it gives | Pages |
|---|---|---|
| The Pixa chain, through `api.pixagram.com` and the other public nodes | Every live value, named with its API call and the date it was read | All |
| Steem and Hive, through public API nodes and [SteemWorld](https://steemworld.org/block/1) | Blocks, hardfork dates and operations since 2016 | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md), [From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md), [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| Golos, through its [explorer](https://explorer.golos.id/) | Golos's first blocks | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| The Economist, [Big Mac index data](https://github.com/TheEconomist/big-mac-data) | Big Mac prices for the feed. The data are published under CC BY 4.0 and the software under MIT. | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md) |
| Frankfurter, frankfurter.dev | Exchange rates: the European Central Bank's reference rates for the agnostic feed, and the app's display currencies | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md), [Become a Witness](../10-node-operators/become-a-witness.md), [Wallet Basics](../08-guides/wallet-basics.md) |
| CoinMarketCap: [STEEM](https://coinmarketcap.com/currencies/steem/historical-data/), [SBD](https://coinmarketcap.com/currencies/steem-dollars/historical-data/), [snapshot of 2016-07-17](https://coinmarketcap.com/historical/20160717/) | Steem's market prices and rankings | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md), [From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md) |
| [CoinGecko, Hive Dollar](https://www.coingecko.com/en/coins/hive_dollar) | HBD prices | [From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md) |
| [Moneyhouse](https://www.moneyhouse.ch/en/company/pixagram-ag-1298024171) | The Swiss commercial register entry of Pixagram SA | [Who Does What](../01-start-here/who-does-what.md) |
| npm: [`@pixagram/dpixa`](https://www.npmjs.com/package/@pixagram/dpixa), [`@hiveio/dhive`](https://www.npmjs.com/package/@hiveio/dhive) | Library versions | [SDKs and Libraries](../09-developers/sdks-and-libraries.md), [Developer Quickstart](../09-developers/developer-quickstart.md) |

## Books and papers

| Work | Pages |
|---|---|
| W. Ross Ashby, *An Introduction to Cybernetics* (Chapman & Hall, 1956) | [Variety and Regulation](../06-economic-cybernetics/variety-and-regulation.md), [Viable System Model](../06-economic-cybernetics/viable-system-model.md) |
| Stafford Beer, *Brain of the Firm* (Allen Lane, 1972; second edition, Wiley, 1981) and *The Heart of Enterprise* (Wiley, 1979) | [Viable System Model](../06-economic-cybernetics/viable-system-model.md), [Variety and Regulation](../06-economic-cybernetics/variety-and-regulation.md) |
| C. S. Holling, "Resilience and Stability of Ecological Systems", *Annual Review of Ecology and Systematics* 4 (1973) | [Resilience and Cascades](../06-economic-cybernetics/resilience-and-cascades.md) |
| B. Walker, C. S. Holling, S. R. Carpenter and A. Kinzig, "Resilience, Adaptability and Transformability in Social–ecological Systems", *Ecology and Society* 9(2) (2004) | [Resilience and Cascades](../06-economic-cybernetics/resilience-and-cascades.md), [Glossary](glossary.md) |
| P. Bak, C. Tang and K. Wiesenfeld, "Self-organized criticality: An explanation of the 1/f noise", *Physical Review Letters* 59 (1987) | [Resilience and Cascades](../06-economic-cybernetics/resilience-and-cascades.md), [Glossary](glossary.md) |
| P. Bak and K. Chen, "Self-Organized Criticality", *Scientific American* 264(1) (1991) | [Resilience and Cascades](../06-economic-cybernetics/resilience-and-cascades.md) |

## Articles and posts

| Date | Author or publisher | Title | Pages |
|---|---|---|---|
| — | Hive | [Release 1.28.0](https://gitlab.syncad.com/hive/hive/-/releases/1.28.0) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| — | Blurt | [README](https://gitlab.com/blurt/blurt) and [FAQ](https://blurtwallet.com/faq.html) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| — | Alan Hibbard, GoldSilver | [Saving vs. Investing](https://goldsilver.com/hidden-secrets-of-value/savings-vs-investing/), in *Hidden Secrets of Value* | [Supracoin vs Stablecoin](../05-pixa-supra/supracoin-vs-stablecoin.md) <!-- retired-ok --> |
| 2013 | Mike Maloney | *Hidden Secrets of Money*, episode 1, a video series | [Supracoin vs Stablecoin](../05-pixa-supra/supracoin-vs-stablecoin.md) <!-- retired-ok --> |
| 2016-07-01 | Dan Larimer | [Why every Blockchain needs a Constitution](https://steemit.com/blockchain/@dan/why-every-blockchain-needs-a-constitution) | [Constitution](../07-governance/constitution.md), [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2016-07-01 | Dan Larimer | [How to Dodge Bullets - Creating your own Reality](https://steemit.com/philosophy/@dan/how-to-dodge-bullets-creating-your-own-reality) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2016-07-06 | Dan Larimer | [Steemit's Evil Plan for Cryptocurrency World Domination](https://steemit.com/steem/@dan/steemit-s-evil-plan-for-cryptocurrency-world-domination) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md), [NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md), [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2016-07-07 | Dan Larimer | [Escrow SIP - Steem Improvement Proposal](https://steemit.com/sip/@dan/escrow-sip-steem-improvement-proposal) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2016-09-13 | Steemit | [Steem 0.14.1 Released - Hardfork Postponed until 9/20/2016](https://steemit.com/steem/@steemitblog/steem-0-14-1-released-hardfork-postponed-until-9-20-2016) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2016-10-18 | ForkLog | [Состоялся запуск русскоязычной социально-медийной платформы «Голос»](https://forklog.com/sostoyalsya-zapusk-russkoyazychnoj-sotsialno-medijnoj-platformy-golos/), in Russian: the launch of Golos | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2017-01-27 | @son-of-satire | [How Social Media's Predictive Algorithms Are Perpetuating Division Among The People](https://steemit.com/life/@son-of-satire/how-social-media-s-predictive-algorithms-are-perpetuating-division-of-the-people) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2017-04-12 | Steemit | [Joint Statement](https://steemit.com/steemit/@steemitblog/joint-statement) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2017-09-28 | @ned | [Announcing: Smart Media Tokens (SMTs)](https://steemit.com/steem/@ned/announcing-smart-media-tokens-smts) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2018-08-15 | Steemit | [SMTs Release Dates!](https://steemit.com/steem/@steemitblog/smts-release-dates), updated 2019-03-11 | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2018-09-25 | Steemit | [HF20 Update: Hardfork Complete](https://steemit.com/steem/@steemitblog/hf20-update-hardfork-successful) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2019-02-07 | @aggroed | [Introducing Steem-Engine.com (smart contracts and token creation on Steem)](https://steemit.com/steemengine/@aggroed/introducing-steem-engine-com) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2019-04-15 | CryptoSlate | [Block Producers change EOS constitution following voting gridlock](https://cryptoslate.com/block-producers-change-eos-constitution-following-voting-gridlock/) | [Constitution](../07-governance/constitution.md) |
| 2020-02-14 | Business Wire | [Steemit Joining TRON Ecosystem](https://www.businesswire.com/news/home/20200214005129/en/Steemit-Joining-TRON-Ecosystem) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2020-02-24 | CoinDesk | [Justin Sun Bought Steemit. Steem Moved to Limit His Power](https://www.coindesk.com/tech/2020/02/24/justin-sun-bought-steemit-steem-moved-to-limit-his-power) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2020-03-02 | CoinDesk | [Why Crypto Should Care About Justin Sun's Steem Drama](https://www.coindesk.com/tech/2020/03/02/why-crypto-should-care-about-justin-suns-steem-drama) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2020-03-02 | The Block | [Tron takeover? Steem community in uproar as crypto exchanges back reversal of blockchain governance soft fork](https://www.theblock.co/post/57508/tron-steem-takeover-crypto-exchanges-governance-reversal-soft-fork-blockchain) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2020-03-17 | Hive, [@hiveio](https://hive.blog/@hiveio) | [Announcing the Launch of Hive Blockchain](https://hive.blog/communityfork/@hiveio/announcing-the-launch-of-hive-blockchain) | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md), [Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md) |
| 2020-03-25 | @aggroed | [Hive-Engine Update](https://peakd.com/hive-engine/@aggroed/hive-engine-update) | [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md) |
| 2021-02-21 | @smooth | [HBD stabilizer algorithm](https://hive.blog/hbd/@smooth/hbd-stabilizer-algorithm) | [From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md) |
| 2025-07-31 | @smooth | [HBD stabilizer proposal August 2025](https://inleo.io/@smooth/hbd-stabilizer-proposal-august-2025) | [From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md) |
| 2025-12-20 | Matias Affolter, Pixagram | [How Pixagram Completes the Vision for Blockchain World Domination](https://www.linkedin.com/pulse/how-pixagram-completes-vision-blockchain-world-domination-8ntve/) | [Essays](../12-history-and-perspectives/essays.md), [The Plan Revisited](../12-history-and-perspectives/the-plan-revisited.md), [Constitution](../07-governance/constitution.md), [NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md) |


## Credits

Pixa is built on the work of others. The credits below are as each repository's licence file, or its README where noted, states them.

| Work | Credited to | Licence |
|---|---|---|
| Steem, the original code base | "Steemit, Inc., and contributors" | MIT |
| Hive, the code Pixa's node is forked from | "Hive blockchain community contributors" | MIT |
| Graphene, FC and Boost, which the node depends on | Their own authors, "under their own individual licenses" | Their own |
| Hivemind, the social layer | Steemit Inc. | MIT |
| dpixa's original code, from dhive | Johan Nordberg | BSD-3-Clause-No-Military-License |
| The Big Mac index | The Economist Newspaper | Software: MIT (`LICENCE`); data: CC BY 4.0 (README) |

Who wrote and changed each page is recorded in this repository's history.
