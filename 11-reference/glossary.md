# Glossary

> **Status: Live.** It covers the terms used across these pages. Where an entry quotes a number, [Chain Parameters](chain-parameters.md) is the reference.

Each term has one entry. Older names, and names inherited from Steem and Hive, point to the term these pages use. The [Style Guide](../13-about/style-guide.md) explains why each name was chosen.

## Other names you may meet

| You may see | These pages say |
|---|---|
| STEEM, HIVE | [PIXA](#pixa) |
| PXA | [PIXA](#pixa). PXA is the ticker the price-feed software expects for PIXA market pairs; PIXA does not trade yet. |
| Steem Power (SP), Hive Power (HP), staked PIXA | [Pixa Power (PXP)](#pixa-power-pxp) |
| SBD, Steem Dollars, HBD, Hive Backed Dollars | [Pixa Supra (PXS)](#pixa-supra-pxs) |
| PixaFlat, PixaSupra, "the stable token" | [Pixa Supra (PXS)](#pixa-supra-pxs) |
| DHF, Decentralized Hive Fund, Steem Proposal System, Decentralized Proposal Fund | [Decentralized Pixa Fund (DPF)](#decentralized-pixa-fund-dpf) |
| `hive.fund`, `steem.dao`, the DAO | [`pixa.omnibus`](#pixaomnibus) |
| `pixa.ico`, ICO account, ICO pool | [`pixa.rex`](#pixarex) |
| Pixa Operations S.A. | [Pixa Rex S.A.](#pixa-rex-sa) |
| Pixagram AG | [Pixagram SA](#pixagram-sa) |
| block producer, delegate | [Witness](#witness) |
| bandwidth | [Resource Credits](#resource-credits-rc) |
| voting power | [Voting mana](#voting-mana) |
| `STM…` public keys | [`PIX…` public keys](#pix) |
| pixagram.io | pixagram.com (the app) and pixa.org (for developers) |

## Terms

### Account
An identity on the chain: a name of 3 to 16 characters controlled by four [keys](#keys). An account is opened either by paying the account creation fee or with a ticket claimed through [Resource Credits](#resource-credits-rc) ([limits](chain-parameters.md#accounts-and-keys)).

### Account recovery
A way to take back an account whose [owner key](#keys) was stolen. The account's [recovery partner](#recovery-partner) starts the request. You then complete it with a new owner key and an owner key the account used within the last 30 days. On Pixa this cannot succeed until the chain starts recording owner-key history, about 2026-12-24 ([details](chain-parameters.md#accounts-and-keys)).

### Author reward
The part of a post's payout that goes to its author: the 60% left after the [curation](#curation) share, less any [beneficiaries](#beneficiary). It is paid partly in [PXS](#pixa-supra-pxs) and partly in [Pixa Power](#pixa-power-pxp), or entirely in Pixa Power if the author chooses.

### Beneficiary
An account named in a post to receive part of its author reward. A post can name up to 8.

### Big Mac reference
The real-world good the PXS reference points to. It is a direction, not a price PXS promises. Each [witness](#witness) works out how many PIXA buy one Big Mac where it operates, using the local price of a Big Mac and a market price for PIXA, and publishes that figure. The chain takes the median ([feed rules](chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). PIXA does not trade on any market yet, so for now witnesses use an agreed placeholder price for PIXA.

### Block
A batch of transactions signed by one witness. A new block arrives every 3 seconds.

### Block log
The file in which a node keeps every block since genesis: the chain itself. A node rebuilds everything else from it ([Run a Node](../10-node-operators/run-a-node.md#what-the-node-keeps)).

### Chain ID
A 32-byte value mixed into every signature, so a transaction signed for Pixa is invalid on Hive and the other way round. Pixa's is the ASCII word `pixagram`, padded with zeros.

### Claimed account
A ticket for opening an account, paid with [Resource Credits](#resource-credits-rc) instead of the creation fee. Apps use these tickets to open accounts for new users.

### Collateral ratio
The value of all PIXA divided by the value of the PXS held outside the treasury, with both valued at the [median feed](#median-feed). The [haircut](#haircut) is calculated from it.

### Collateralized conversion
Turning PIXA into PXS. You lock twice the value in PIXA and receive the PXS at once, minus a 5% fee. The conversion settles after 3.5 days, and any excess collateral comes back to you. The chain refuses it if PXS would grow past its limit ([limits](chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).

### Comment
The operation behind every post and reply. A post is a comment with no parent; a reply names its parent. On Pixagram, an artwork is a post whose body is a [data URI](#data-uri).

### Community
A group of posts with its own moderators, run by [Hivemind](#hivemind). Its name is `portal-` followed by a digit from 1 to 3 and then 4 to 6 more digits, for example `portal-100001`.

### Content constant
A parameter of the reward curves, written *s*. Pixa sets it to 2,500, far below Hive's, to suit this chain's scale.

### Conversion
Turning PXS into PIXA. It settles after 3.5 days at the [median feed](#median-feed), reduced by the [haircut](#haircut) if one applies.

### Curation
Voting on posts. Voters share 40% of each post's reward. Early votes earn more than later votes of equal weight, and the reward falls further for votes cast more than 24 hours, and again more than 72 hours, after the post was published ([curve and windows](chain-parameters.md#voting-and-curation)).

### `custom_json`
An operation that carries arbitrary JSON for apps, such as follows, community actions and games. On Pixa it can hold up to 64 KiB.

### Data URI
Text of the form `data:image/webp;base64,…` that contains a whole image. On Pixagram, an artwork post's body is exactly one data URI holding a lossless [WebP](#webp) image, so the image itself is stored in the block.

### Debt ratio
The value of the PXS held outside the treasury, as a share of that PXS plus all PIXA. At 20%, new PXS stops being printed. Above 30%, the [haircut](#haircut) applies.

### Decentralized Pixa Fund (DPF)
The on-chain fund that pays for proposals the community votes for. It is held by the keyless account [`pixa.omnibus`](#pixaomnibus) and receives a share of every block's [issuance](#issuance). It is the counterpart of Hive's DHF ([how it pays](system-accounts.md#the-treasury-pixaomnibus)).

### Delayed voting
Stake that is powered up, or received from the allocation accounts, counts in witness and proposal votes only after 30 days; rewards count at once. This blocks quick governance takeovers with freshly bought stake.

### Delegation
Lending [Pixa Power](#pixa-power-pxp) to another account. The borrower gets its weight for voting on posts and its Resource Credits. You keep ownership, and witness and proposal votes still count the stake as yours. When you take a delegation back, the stake reaches you 5 days later.

### Downvote
A vote that lowers a post's payout. Downvotes spend a separate pool of mana worth a quarter of your voting mana.

### DPoS
Delegated Proof of Stake: a consensus method in which stakeholders elect the block producers. On Pixa these producers are the [witnesses](#witness).

### Dust deduction
A fixed 50,000,000 rshares that every vote loses, inherited from Hive. On Pixa a VESTS is worth about one PIXA, so a full-strength vote needs more than 2,500 Pixa Power to count at all ([details](chain-parameters.md#voting-and-curation)).

### Genesis
The start of the chain: block 0, 2026-09-04 12:00:00 UTC. Pixa began with a new genesis, so no balances were copied from Steem or Hive. See [Genesis allocation](system-accounts.md#genesis-allocation).

### HAF
Hive Application Framework: an indexer that copies the chain into PostgreSQL so apps can query it. Pixa's public API nodes run it.

### Haircut
A factor, at most 1, applied when PXS converts to PIXA. It is 1 while the [collateral ratio](#collateral-ratio) is at least 7 : 3. Below that it falls in proportion, to 3R ÷ 7. Under stress, a PXS settles for less instead of the system defending a number ([formula](chain-parameters.md#pixa-supra-pxs-and-the-price-feed), [how it works](../05-pixa-supra/haircut-corridor-and-settlement.md#the-haircut)).

### Hardfork
A protocol upgrade. It activates once enough of the scheduled witnesses run the new version and vote for it. Hardfork 29, applied on 2026-09-18, is the first made for Pixa ([quorum](chain-parameters.md#blocks-and-witnesses)).

### Hivemind
The social indexer behind feeds, follows and communities. The `bridge.*`, `follow_api.*` and `tags_api.*` API methods are answered by Hivemind.

### Issuance
The new PIXA created in every block. Most goes to the reward fund. The rest goes to the DPF and to the witness that produced the block; none goes to stakers for simply holding ([rate and split](chain-parameters.md#issuance)).

### Jussi
The JSON-RPC proxy in front of a public node. On `api.pixagram.com` it also renames Hive's `hbd_*` fields to `pxs_*`.

### Keys
Every account has four key pairs, each with a different power:

- **Owner** can replace the other keys and recover the account. Keep it offline.
- **Active** moves funds and changes most settings.
- **Posting** posts, votes and follows. It cannot move funds.
- **Memo** encrypts private memos.

Public keys start with [`PIX`](#pix).

### Median feed
The rate the chain uses for conversions: how many PIXA one PXS converts to, before any [haircut](#haircut). It is the median of the last 84 hourly samples, and each sample is the middle value of the witnesses' feeds ([rules](chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).

### Multisig
An authority that needs several signatures. [`pixa.rex`](#pixarex) and [`pixa.team`](#pixateam) each need 3 of 3.

### NAI
Numeric Asset Identifier, the code each token carries on the wire: PIXA `@@000000021`, PXS `@@000000013`, VESTS `@@000000037`.

### Node
A computer running hived, the chain's software. A follower node validates and stores the chain; a witness node also produces blocks; an API node also serves apps ([Run a Node](../10-node-operators/run-a-node.md)).

### Payout
Seven days after a post is published, the rewards it has gathered are paid to its author, beneficiaries and curators. A payout below 0.020 PXS is not made.

### PIX
The prefix of Pixa public keys, for example `PIX6LLegb…`. Hive keys start with `STM`.

### PIXA
The liquid token of the Pixa chain, with three decimals. It is the counterpart of HIVE and STEEM.

### Pixa chain
The public blockchain Pixagram runs on. It is built from Hive's code with Pixa-specific rules, and started from its own [genesis](#genesis).

### Pixa Power (PXP)
PIXA that has been staked, held on chain as [VESTS](#vests). It gives voting weight, earns curation rewards and supplies Resource Credits. Turning it back into PIXA takes 13 weekly instalments, and holding it earns nothing by itself. It is the counterpart of Hive Power and Steem Power.

### Pixa Supra (PXS)
The chain's second unit. **PXS promises no price.** It has no peg, cannot be redeemed for money, pays no interest, and no one stands behind its value. In one phrase, it is a Big Mac referenced [supracoin](#supracoin). It converts into PIXA at the [median feed](#median-feed), which references one Big Mac, less the [haircut](#haircut) when the network is stretched. It is the counterpart of HBD and SBD ([PXS at a Glance](../05-pixa-supra/pxs-at-a-glance.md)).

### Pixagram
The social network for pixel art that runs on the Pixa chain (pixagram.com). The name also refers to the project as a whole.

### Posting interval
The pause the chain requires between your posts: 5 minutes between top-level posts, and 3 seconds between replies or edits.

### Power up, power down
Powering up turns PIXA into Pixa Power at once. Powering down turns it back into PIXA in 13 weekly instalments.

### Price feed
A witness's published statement of how many PIXA one PXS references. Witnesses publish about once an hour; feeds older than 7 days are ignored.

### Print rate
The share of the PXS part of author rewards that is actually paid in PXS. It is 100% while the [debt ratio](#debt-ratio) is under 20% and 0 at or above it; when it is 0, those rewards are paid in PIXA instead.

### Proof-of-Brain
Paying for contributions according to stake-weighted votes. Authors are rewarded for what they publish, and curators for finding it early. The chain records the votes; people supply the judgement.

### Proposal
A request for money from the DPF, with a receiver, a daily amount, start and end dates. It is funded while it has more votes than the [return proposal](#return-proposal), up to the fund's daily budget.

### Proxy
Handing your governance votes to another account. It then votes your stake for witnesses and on DPF proposals, and your own proposal votes are ignored while the proxy is set.

### Recent claims
The running total of recent reward claims, which decays over 15 days. Each post's payout is its claim divided by this total, times the reward fund's balance. Hardfork 29 reset it, because the value inherited from Hive had made early payouts too small to pay.

### Recovery partner
The account allowed to start a recovery for you.

### Replay
Rebuilding a node's state by re-applying every block of its own [block log](#block-log). Needed after a version change or a new indexing plugin.

### Resource Credits (RC)
The stake-based allowance that pays for operations instead of fees. Every operation spends credits, bigger transactions spend more, and credits recharge fully in 5 days.

### Restricted account
[`pixa.rex`](#pixarex) or [`pixa.team`](#pixateam). These two accounts may only move VESTS and update their own keys ([rules](system-accounts.md#restricted-accounts-pixarex-and-pixateam)).

### Return proposal
A DPF proposal that pays back to the fund itself, so it sets the bar: only proposals with more votes are paid. On Pixa it is proposal 2.

### Reward fund
The pool that pays post rewards. It receives most of each block's issuance.

### rshares
Reward shares: the weight of a vote in the reward calculation. It is the mana the vote spends, minus the [dust deduction](#dust-deduction), and reduced further for votes cast in the last 12 hours before payout.

### Savings
Balances that can only be withdrawn after a 3-day delay, which gives you time to react if your active key is stolen. Savings earn no interest on Pixa.

### Signing key
The key a witness registers on chain and keeps on its server to sign blocks. It is separate from the account's [keys](#keys). Besides blocks, it can only update the witness's own settings, such as its URL, price feed and parameter votes; it cannot move funds ([Become a Witness](../10-node-operators/become-a-witness.md#the-two-keys)).

### TGE
Token generation event: the creation of the genesis allocation at block 0, on 2026-09-04. The operator, Pixa Rex S.A., initiated it.

### Timeshare witness
The 21st slot of a full witness round, which rotates among witnesses that are not in the top 20. It exists only once more than 20 witnesses are active.

### Transaction
A signed bundle of operations. It names an expiry up to 24 hours ahead, and a node drops it if it is not included within an hour of reaching that node. It cannot be larger than the current block size limit ([size and expiry](chain-parameters.md#transaction-and-block-size)).

### Treasury
See [`pixa.omnibus`](#pixaomnibus).

### VESTS
The on-chain unit of [Pixa Power](#pixa-power-pxp), with six decimals. On Pixa, 1 VESTS has stayed worth about 1 PIXA since genesis.

### Voting mana
How much voting an account can do. Since hardfork 28, a full-strength vote spends 2% of the full mana bar, however much is left, so 50 such votes empty it. Mana recharges by 20% of the full amount per day.

### WebP
The image format used for artworks. The app encodes each artwork as a lossless WebP file and stores it in the post itself as a [data URI](#data-uri).

### Witness
An elected block producer. Up to 21 are elected, and the chain needs only 1 to run. Witnesses sign blocks in turn, publish the [price feed](#price-feed) and vote on chain settings such as the account creation fee and block size. Every account can vote for up to 30 of them, weighted by Pixa Power.

### Witness schedule
The order in which the elected witnesses take turns producing blocks.

## Accounts and organisations

### `pixa.omnibus`
The keyless treasury account of the [Decentralized Pixa Fund](#decentralized-pixa-fund-dpf) ([details](system-accounts.md#the-treasury-pixaomnibus)). It is not the [Pixa Omnibus Foundation](#pixa-omnibus-foundation).

### `pixa.rex`
The operator's genesis allocation of 75,000,000 VESTS. It is a [restricted account](#restricted-account) ([details](system-accounts.md#restricted-accounts-pixarex-and-pixateam)).

### `pixa.team`
The team and contributor allocation of 25,000,000 VESTS. It is a [restricted account](#restricted-account).

### Pixa Omnibus Foundation
The foundation, based in the Cayman Islands, that stewards the protocol and speaks for the ecosystem. It holds no keys to [`pixa.omnibus`](#pixaomnibus).

### Pixa Rex S.A.
The operator, based in Panama. It runs the front-end, initiated the [TGE](#tge) and holds the [`pixa.rex`](#pixarex) allocation.

### Pixagram SA
The Swiss development company in Zug that develops the protocol and owns its intellectual property. Some documents call it Pixagram AG.

## Design vocabulary

The design notes for PXS describe it with terms from monetary theory and cybernetics. These terms describe how the system is meant to behave. They are not objects on the chain. Each entry says where the idea meets the code.

### Algedonic alert
In Beer's Viable System Model, a pain signal that skips the slow channels. In the PXS design, it is the [haircut](#haircut) switching on when the collateral ratio falls too low. On chain, each hour the haircut applies, the chain records a `system_warning` operation ([Viable System Model](../06-economic-cybernetics/viable-system-model.md#the-algedonic-alert)).

### Atlas
The collateral base of PXS: all PIXA and Pixa Power, which together are the network's own economy. No one can add to it or draw from it to support PXS. On chain, it appears as *P*, the PIXA supply in the haircut formula.

### Basin of attraction
The range of states a system returns to after a disturbance. Over-collateralisation is meant to widen it.

### Chaotic stability
Staying inside a band rather than pinned to a single point, the way living systems persist. PXS aims for this instead of a defended price.

### Corridor
The design notes' band of collateral ratios, roughly 3 to 10, inside which no haircut applies. The chain does not enforce it: printing stops at a ratio of 4, and the haircut starts below 7/3 ([the two compared](../05-pixa-supra/haircut-corridor-and-settlement.md#corridor-and-thresholds-design-and-chain)).

### Disintermediation
Removing the layers of an issuer, custodian, reserve and redemption desk, so that holder and base meet directly. Here they meet through consensus rather than through a counterparty.

### Feedback order
Beer's ladder of control:

- **First order** pursues a goal it is given.
- **Second order** chooses how to pursue it.
- **Third order** chooses the goal.

A defended peg is first-order. The PXS design aims higher, because its reference and its thresholds can be changed by consensus.

### Homeostasis
Keeping a key variable within survivable bounds by adjusting rather than resisting. The *homeostatic band* is the range of collateral ratios in which no haircut applies.

### Macro
The regulated flow of PXS: conversions between PXS and PIXA, whose rate the haircut adjusts. In the four-part model it is the control function.

### Oracle
The sensing part of PXS: the witnesses' feeds, reduced by a median across witnesses and a median over 84 hours. It reports which way to lean; it does not promise a price ([Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md)).

### Orientation
How PXS relates to its reference. PXS promises no price: it points toward one Big Mac's worth of purchasing power without promising to reach it, and under stress it settles for less. Orientation is the opposite of a peg.

### Projection
What a PXS balance is in the design's terms: the [Atlas](#atlas) seen through the [Oracle](#oracle). It settles in PIXA at the haircut and gives no claim on any asset or person. See [Supra](#supra).

### Requisite variety
Ashby's law: a regulator must be able to respond in as many ways as the disturbances it faces. A fixed peg can only defend a single number ([Variety and Regulation](../06-economic-cybernetics/variety-and-regulation.md)).

### Resilience
After Walker, Holling and colleagues (2004), a system's resilience has four aspects:

- **Latitude:** how far it can be pushed before it cannot recover.
- **Resistance:** how hard it is to push.
- **Precariousness:** how close to that edge it already is.
- **Panarchy:** how much the systems above and below it shape it.

Applied to PXS: [Resilience and Cascades](../06-economic-cybernetics/resilience-and-cascades.md).

### Self-organised criticality
After Bak, Tang and Wiesenfeld (1987), a connected system that drifts to a critical state where one small event can set off a cascade of any size. The remedy is fewer connections and gentler slopes, not hunting for triggers ([Resilience and Cascades](../06-economic-cybernetics/resilience-and-cascades.md#self-organised-criticality)).

### Supra
What a PXS holder holds: the [Atlas](#atlas) read through the [Oracle](#oracle). It is a projection that settles in PIXA at the haircut, not a claim on any asset or person.

### Supracoin
The category the PXS design proposes: a unit oriented toward purchasing power, with no peg, no par claim and no issuer. PXS is a Big Mac referenced supracoin: its reference is one Big Mac, and it promises no price.

### Variety attenuator
A filter that reduces the noise reaching a controller. The Oracle's two medians, across witnesses and over time, are attenuators.

### Viable System Model (VSM)
Stafford Beer's model of the five functions any self-sustaining system needs: operations, coordination, control, intelligence and policy. The PXS design maps its four parts onto them ([Viable System Model](../06-economic-cybernetics/viable-system-model.md)).
