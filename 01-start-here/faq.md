# FAQ

> **Status: Live.** Short answers, each linking to the page that explains it. Last checked 2026-10-05.

## Using Pixagram

**What is Pixagram?**
A social network for pixel art on its own blockchain, the Pixa chain. Artworks are stored inside posts, and members' votes decide who is rewarded. See [What Is Pixagram](what-is-pixagram.md).

**Does it cost anything to join?**
No. The app opens your account after you verify a phone number, and the operator pays the account fee. A community-funded proposal covers that fee until 2026-12-31 ([Who Does What](who-does-what.md#who-pays-for-what-today)).

**Do I need to buy tokens to post?**
No. Posting and voting spend [Resource Credits](../04-tokens-and-economy/resource-credits.md), not fees. New accounts receive enough to publish several artworks a day.

**Why does my vote show no value?**
A vote moves rewards only once the voter holds more than 2,500 Pixa Power. Below that, the chain's dust deduction cancels it ([why](../02-social-layer/voting-and-curation.md#why-small-votes-count-for-nothing)).

**When are rewards paid?**
Seven days after a post is published. The rewards then wait in your wallet until you claim them ([Posting and Rewards](../02-social-layer/posting-and-rewards.md)).

**Can I decline rewards, or take them all as Pixa Power?**
The chain allows both, but the app does not offer either yet. Every post uses the default split.

## Art and data

**Where is my artwork stored?**
Inside your post, as a lossless WebP image in the block itself. It is not a link or a hash ([Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md)). Images inside blog posts are different: they are links to files stored on Arweave.

**Can I delete a post?**
The app can hide it and replace an artwork's body with the word `deleted`. The version first published stays in its block forever. Never post anything you may need to remove ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)).

**Is anything private?**
No. Posts, votes, transfers and balances are public. Only memos encrypted with a memo key hide their content.

**Does the app use AI on my pictures?**
Only if you choose it. If you accept the AI conversion, your picture is sent to a Hugging Face Space run by the project. Otherwise conversion happens in your browser ([Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md)).

**Can I sell my art?**
Not yet. Buying and selling artworks on chain is planned for 2027 ([NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md)).

## Tokens

**What are PIXA, Pixa Power and PXS?**
PIXA is the liquid token. Pixa Power is staked PIXA. PXS promises no price: it is a second unit that converts into PIXA ([Tokens at a Glance](../04-tokens-and-economy/tokens-at-a-glance.md)).

**Is PXS a stablecoin?** <!-- retired-ok -->
No. Nothing defends its price, no one redeems it for money, and it pays no interest. It is a Big Mac referenced supracoin: it converts into PIXA at the median of the witnesses' feeds, which reference one Big Mac, less a haircut if the network is stretched ([the difference](../05-pixa-supra/supracoin-vs-stablecoin.md)). <!-- retired-ok -->

**Does holding PIXA, Pixa Power or PXS earn anything?**
No. Holding earns nothing by itself. Rewards pay for publishing, curating and producing blocks ([Supply, Inflation and Yield](../04-tokens-and-economy/supply-inflation-and-yield.md)).

**Is PIXA deflationary?** <!-- retired-ok -->
No. New PIXA is issued every block, at a yearly rate that started at about 9.8% and falls to 0.95% by about 2047 ([Issuance](../11-reference/chain-parameters.md#issuance)).

**What is PIXA worth?**
PIXA does not trade on any market yet. Fiat values in the app use a fixed placeholder price, as do the witnesses' feeds ([placeholder](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).

## Safety and control

**What happens if I lose my keys?**
Your recovery phrase recreates them, together with the password you set with it, if any, so keep the PDF backup offline ([Keys and Recovery](../08-guides/keys-and-recovery.md)). Account recovery, which reverses a theft of your owner key, becomes possible on the chain from about 2026-12-24 ([why](../11-reference/chain-parameters.md#accounts-and-keys)).

**Who controls the chain?**
The witnesses whom stakeholders elect. Rule changes take effect only when enough witnesses run them ([Witnesses and DPoS](../07-governance/witnesses-and-dpos.md)).

**Who controls the community fund?**
Stakeholders, through proposal votes. The fund's account has no keys ([Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md)).

**What if the company behind Pixagram disappeared?**
The chain would keep running as long as witnesses produce blocks and nodes serve its data, and your artworks would stay in the chain's history. The software is open source, so anyone can run a node or build another app.

**Is Pixagram on Ethereum or Solana?**
No. It runs on its own chain, built from Hive's code, and does not integrate with either.

**Where do I report a security problem?**
Privately, to the maintainers. Never in a public post or issue ([Style Guide](../13-about/style-guide.md#security-and-disclosure)).
