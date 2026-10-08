# Witnesses and DPoS

> **Status: Live.** 8 witnesses on 2026-10-08; up to 21 elected, 1 required. Figures were read at block 979,298, after hardfork 30.

Witnesses are the accounts that produce the Pixa chain's blocks. They also publish the price feed and, through the median of their votes, set a few network parameters. Stakeholders elect them with their Pixa Power. The system is called delegated proof of stake (DPoS). This page explains what witnesses do, how they are elected and paid, who they are today, and how to vote.

## What witnesses do

| Task | How it works |
|---|---|
| Produce blocks | One block every 3 seconds. The elected witnesses take turns. |
| Make blocks final | A block becomes irreversible once a supermajority of the scheduled witnesses have confirmed it. |
| Publish the price feed | PXS promises no price. Each witness publishes the price of one Big Mac in PIXA, the reference PXS is oriented toward, and is expected to update it every hour. Conversions use the median of the feeds over 3.5 days, and a feed older than 7 days stops counting ([rules](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed), [how the median is made](../05-pixa-supra/oracle-and-price-feed.md)). |
| Set network parameters | Each witness publishes values for the account creation fee, the maximum block size and the subsidy for account tickets. The chain uses the median across the scheduled witnesses. |
| Approve upgrades | A witness approves a hardfork by running the new version and signalling for it ([Protocol Upgrades](protocol-upgrades.md)). |

**What witnesses can and cannot do**

- **One witness can delay a transaction, not block it.** A witness can leave a transaction out of the blocks it produces, but the next witness in the round can include it.
- **A majority can do more.** Witnesses acting together can refuse operations of chosen kinds, or from chosen accounts. A majority of Steem's witnesses did this in 2020 ([From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split)).
- **Rule changes need most of them.** A change to the rules activates only when a supermajority of the witnesses run it. It reaches users only if the nodes and apps that serve them upgrade too.
- **No witness can sign for your account.** No witness can spend the fund without votes, or change a parameter alone.

## How witnesses are elected

- **Who can vote.** Every account with Pixa Power can vote for up to 30 witnesses. Each vote carries the voter's full weight; votes are not split.
- **The weight.** It is your own Pixa Power, including stake you have lent out, plus the weight of any accounts that named you as their proxy. Stake you power up, or receive from the allocation accounts, counts only after 30 days ([Pixa Power](../04-tokens-and-economy/pixa-power.md#effective-pixa-power)).
- **Who cannot vote.** The allocation accounts `pixa.rex` and `pixa.team` cannot vote.
- **Proxies.** You can name a proxy to vote for you on witnesses and on DPF proposals. Naming one replaces your own witness votes. A proxy can itself name a proxy, up to 4 levels deep.
- **Expiry.** An account's witness votes, proposal votes and proxy are cleared if it takes no governance action for 365 days. A governance action is voting for a witness, setting a proxy or voting on a proposal.
- **The schedule.** Up to 21 witnesses are elected to produce blocks, and the chain needs only 1 to run ([Chain Parameters](../21-reference/chain-parameters.md#blocks-and-witnesses)).
- **The approval floor.** Since hardfork 30, a witness is scheduled only once accounts holding at least 1% of all outstanding Pixa Power have voted for it.

## How witnesses are paid

Witnesses receive the witness share of issuance, 15%, paid as Pixa Power to the producer of each block ([Issuance](../21-reference/chain-parameters.md#issuance)):

- **Per block:** about 0.141 PIXA on 2026-10-08.
- **Per witness:** with 8 witnesses, each produces about 3,600 blocks a day, or about 507 PIXA a day.
- **Missed blocks** are not paid.
- **Before hardfork 30** Hive's weighting spread 21 blocks' worth of pay over the witnesses present, so each block paid about 0.329 PIXA and each of 9 witnesses earned about 1,050 PIXA a day, 2.33 times the nominal share. Since 2026-10-07 every block pays the nominal share while fewer than 21 witnesses are scheduled.

The pay is for running nodes and publishing feeds, and it arrives as stake, so it adds to the witnesses' own votes on posts and in governance.

## The witnesses on 2026-10-08

On 2026-10-08, 8 witnesses were scheduled, all running version 1.30.0. All published a maximum block size of 2,097,152 bytes and the same price feed, 51.833 PIXA per PXS, which is the agreed placeholder rather than a market reading ([why](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). The median account creation fee was 20.000 PIXA. Seven accounts, five of them with stake, had elected them ([Decentralization and Safeguards](decentralization-and-safeguards.md)). Five of the eight also run a public API node ([Architecture](../18-infrastructure/architecture.md#the-six-public-nodes)).

The live list, with each witness's last block, is on the [witness status page](https://pixagram.com/witness-status/).

## How to vote

- **In the app:** open Governance, then Viability Management, and choose the tab with the ballot-box icon. You can vote for up to 30 witnesses there, or name a proxy ([step by step](../08-guides/take-part-in-governance.md#vote-for-witnesses)).
- **With any Hive-compatible library:** broadcast `account_witness_vote` with `approve` set to `true` or `false`, or `account_witness_proxy`. Both need your active key.

Your vote counts in proportion to your matured stake. You can change it at any time.

## Becoming a witness

A witness runs a block-producing node, registers it on chain with its block-signing key, publishes a price feed every hour, and asks stakeholders for votes. [Become a Witness](../10-node-operators/become-a-witness.md) gives the steps; pixa.org's [node operator guide](https://pixa.org/witness.html) covers the same ground for a witness and an API node together.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Slots per round | 21: 20 elected and 1 timeshared | same; 8 scheduled on 2026-10-08 |
| Witness votes per account | 30 | 30 |
| Witness share of issuance | Hive: 10% | 15% |
| Approval needed to be scheduled | none | 1% of all stake, since HF30 |
| What the feed states | HIVE per HBD, one US dollar | PIXA per PXS, one Big Mac |
| 30-day delay on new governance weight | Hive, since HF24 (2020) | from genesis |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Consensus in Steem".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §III.1, §III.3 and §III.4.
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - witness votes and proxies: [hive_evaluator.cpp:228-348](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L228-L348)
  - vote expiry: [database.cpp:3580-3623](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L3580-L3623)
  - pay: [database.cpp:1803-1828 at v1.30.0](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/database.cpp#L1803-L1828)
  - approval floor: [witness_schedule.cpp:155-159 at v1.30.0](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/witness_schedule.cpp#L155-L159)
  - constants: [Chain Parameters](../21-reference/chain-parameters.md#blocks-and-witnesses)
- **Live chain**, read on 2026-10-08: `condenser_api.get_witnesses_by_vote`, `condenser_api.get_witness_schedule`, `database_api.list_witness_votes`, and the `producer_reward` operations before and after block 949,330 (0.328999 and 0.140999 VESTS).
