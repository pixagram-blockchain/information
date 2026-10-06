# Resource Credits

> **Status: Live.** Costs were measured on 2026-10-05, between blocks 895,213 and 895,300. They change every block with network use.

Pixa does not charge a fee for posting, voting or sending tokens. Instead, every account has a stock of Resource Credits (RC) that operations use up and that recharge over time, in proportion to the account's stake. This page explains why, how credits are counted and priced, and what they buy today.

## Why credits instead of fees

The Steem whitepaper's argument still holds. Micropayments don't work. Asking someone to pay a cent to like a picture makes them stop and decide, and that decision costs more than the cent. Fees also lock out newcomers who hold no tokens yet.

Resource Credits replace the fee with an allowance. Your stake entitles you to a share of the chain's capacity, which renews every day. Spam is still expensive: flooding the chain would need a large stake, and the stake would only buy a limited rate.

## How credits are counted

- **Size of the stock.** Your maximum is about **1,000,000 credits per Pixa Power** you can use: your own, plus any lent to you, minus any you have lent out and this week's power-down instalment. Every account also has a small bonus: the account creation fee in force when it was opened, valued in VESTS, even if it was opened with a ticket.
- **Recharge.** Credits recharge at **20% of the maximum per day**, so an empty account is full again after 5 days.
- **Spending.** An operation that costs more credits than you hold is rejected by the node you send it to. Credits are checked by each node, not by consensus.
- **Delegation.** You can lend credits to other accounts with a `custom_json` operation (id `rc`, action `delegate_rc`), up to 100 accounts at a time. You can lend only your own credits. On 2026-10-05 one such delegation existed.

## How operations are priced

The chain prices five resources. Every transaction uses the first three:

| Resource | What it measures |
|---|---|
| History | The transaction's size in bytes, stored forever in the block log |
| State | The memory the operation adds to every node's live state |
| Execution | The time needed to process it, including signature checks |
| Market | Extra history cost, charged only when a transaction contains a transfer or a market operation |
| New accounts | Account tickets, charged only when a ticket is claimed with credits |

Each resource has a pool that refills every block, and its price rises as the pool runs low. Prices are recalculated every block from the last 24 hours of use, so a single large post can move them by a third on a chain as quiet as Pixa is today. On 2026-10-05, the history resource dominated: about **128 credits per byte**.

## What credits buy today

| Operation | Credits (2026-10-05) | At the previous day's usage |
|---|---|---|
| Vote (121 bytes) | 20,492 | 18,305 |
| Transfer, no memo (114 bytes) | 17,562 | 14,877 |
| Follow or other small `custom_json` (170 bytes) | 24,628 | 19,711 |
| Artwork post, 26 kB body | 3,756,396 | 2,822,873 |
| Artwork post, 100 kB body | 13,258,626 | 9,472,463 |
| Account ticket (`claim_account`) | about 303,900,000 | about the same |

What a day's recharge pays for at those prices:

| Pixa Power | Votes | Transfers | 26 kB artworks | 100 kB artworks | Account tickets |
|---|---|---|---|---|---|
| 100 | 975 | 1,138 | 5 | 1 | none |
| 1,000 | 9,759 | 11,388 | 53 | 15 | 0.66 |
| 10,000 | 97,599 | 113,882 | 532 | 150 | 6.6 |

Other limits apply first:

- **Voting mana** allows about 10 full-strength votes a day ([Voting and Curation](../02-social-layer/voting-and-curation.md)).
- **Posting** is limited to one top-level post every 5 minutes.

## Account tickets

Opening an account costs either the account creation fee (20.000 PIXA on 2026-10-05, which is burned) or a ticket claimed with credits.

- **What a ticket costs.** About 304 million credits, a full day's recharge for about 1,500 Pixa Power.
- **Where tickets come from.** They are drawn from a shared subsidy pool, with room for about 15,600 on 2026-10-05.
- **When they can be claimed.** A ticket can be claimed only in a block whose producing witness has subsidy left. Once claimed, it can be spent at any time.

## Fees that remain

Three operations still carry a fee on top of credits, each to deter abuse:

- opening an account
- creating a DPF proposal
- converting PIXA into PXS

The fees are listed in [Chain Parameters](../11-reference/chain-parameters.md#figures-you-may-meet-elsewhere).

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Model | Resource Credits since Steem's hardfork 20 (2018) | same, unchanged code |
| Credits per staked token | about 1,608 million per Hive Power on Hive | about 1 million per Pixa Power |
| Credit delegation | Since Hive's hardfork 26 | same |
| Recharge | 5 days | 5 days |

Credits per staked token differ only because a VESTS is worth far more here. What counts is your share of all stake, which is the same on both chains.

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Eliminating Transaction Fees", "Micropayments Don't Work", "Bandwidth Instead of Micropayment Channels".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §II.2.
- **Code**
  - Cost model: [rc_utility.cpp:243-316](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/rc/rc_utility.cpp#L243-L316).
  - Usage counting: [resource_count.cpp:582-633](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/rc/resource_count.cpp#L582-L633).
  - Credit delegation: [hive_custom_operations.hpp:8-30](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/hive_custom_operations.hpp#L8-L30) and [rc_utility.cpp:27-112](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/rc/rc_utility.cpp#L27-L112).
- **Live chain**
  - Pools and parameters: `rc_api.get_resource_pool`, `rc_api.get_resource_params` and `rc_api.get_rc_stats`.
  - An account's credits: `rc_api.find_rc_accounts`.
  - The validating vote is in block 895,216.
