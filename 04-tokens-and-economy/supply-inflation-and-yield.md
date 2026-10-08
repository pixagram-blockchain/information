# Supply, Inflation and Yield

> **Status: Live.** Since hardfork 30 (2026-10-07) the chain issues exactly its nominal schedule; before, with 9 witnesses, about 1.16 times it. Figures were read at block 979,298 on 2026-10-08, and the burn figures at block 895,415 on 2026-10-05.

New PIXA is created in every block and paid to the people who keep the network running. This page explains how much is created, where it goes, what is destroyed, and how supply may grow over the coming decades. It also explains why holding tokens earns nothing.

## How much is issued

The yearly rate depends only on the block number *h*:

```
rate(h) = max( 9.78% − 0.01 percentage points × floor(h / 250,000) , 0.95% )
```

- **Today:** 9.75%.
- **Each year:** about 0.42 percentage points lower. A year holds about 42 steps of 250,000 blocks.
- **The floor:** 0.95% from block 220,750,000, about 2047.

**What the rate applies to.** In every block, the rate is applied to all PIXA plus the PXS held outside the fund, valued at the median feed. On 2026-10-08 this gave about 0.936 PIXA per block, about 26,900 PIXA a day.

**Where the constants come from.** They are Steem's. Its hardfork 16 chose them so that the rate stood at 9.5% at Steem's block 7,000,000, late in 2016. Pixa counts blocks from its own genesis, so it started at the top of the schedule. Hive, further along the same schedule, issued 5.36% a year on 2026-10-05 ([Chain Parameters](../21-reference/chain-parameters.md#issuance)).

## Where new tokens go

| Recipient | Nominal share | Paid as | On 2026-10-08 |
|---|---|---|---|
| Reward fund, for authors and curators | 70% | PIXA, paid out by votes on posts | about 18,900 PIXA a day |
| Witnesses | 15% | Pixa Power, to the producer of each block | about 4,060 PIXA a day, about 507 each for 8 witnesses |
| Decentralized Pixa Fund | 15% | PXS, to `pixa.omnibus` | about 78 PXS a day |
| Holders of Pixa Power | 0% | — | nothing |

Since hardfork 30 these shares are paid as written. Two inherited rules used to change them, and did so for the chain's first 33 days:

- **Witness pay assumed a full schedule.** Hive weights each block's pay to spread 21 blocks' worth over the witnesses present. While 9 witnesses ran, a block paid about 0.329 PIXA, 2.33 times the nominal share, and the chain issued about 1.16 times its schedule, about 11.3% a year. Since 2026-10-07 every block pays the nominal share while fewer than 21 witnesses are scheduled: about 0.141 PIXA a block, the producer also taking the split's rounding remainder ([Witnesses and DPoS](../07-governance/witnesses-and-dpos.md#how-witnesses-are-paid)).
- **The fund's share was rounded down in every block.** The 0.140 PIXA due to the fund in each block is 0.0027 PXS at the median feed of 51.833 PIXA per PXS, and the rounding paid 0.002 PXS, about 74% of the share, 57.6 PXS a day. Since hardfork 30 consecutive blocks pay the exact amount between them, 0.002 or 0.003 PXS each ([Chain Parameters](../21-reference/chain-parameters.md#issuance)).

The PIXA supply itself grows by about 0.796 PIXA a block, because the fund's part is created as PXS; the rest of the 0.936 is the fund's share.

**Not yet paid out.** On 2026-10-08 the reward fund held 517,193.258 PIXA that had been issued for content but not yet paid to anyone. It is released as posts reach their payout, in proportion to the votes they received ([Proof-of-Brain](../02-social-layer/proof-of-brain.md)).

## Where PIXA is destroyed

PIXA leaves the supply in five ways. In the first three, PXS is created in its place.

| Route | Since genesis, to block 895,415 |
|---|---|
| Converting PIXA into PXS: the PIXA used, 5% fee included | 230,848.081 PIXA in eight conversions, 219,230.653 of it in two conversions requested on 2026-09-24 |
| Paying part of each author reward in PXS | 585.227 PXS in 90 payouts, replacing about 30,300 PIXA |
| Sending PIXA to the fund, which converts it to PXS at once | none so far |
| Account creation fees, burned through `null` | 360.010 PIXA |
| Transfers to `null` | none |

Converting the other way creates PIXA: eight conversions turned 91.749 PXS into 4,755.623 PIXA.

**The balance after 31 days**

| | PIXA |
|---|---|
| Supply at genesis, all of it staked | 100,000,000.000 |
| Supply at block 895,415 | 100,655,142.130 |
| of which still in the reward fund | 483,068.730 |

Issuance added about 0.91 million PIXA. Conversions into PXS, by users and in author rewards, removed about 0.26 million. Fees removed 360 PIXA, and conversions out of PXS added 4,756.

## How supply may grow

If nothing but issuance changed it, the PIXA supply would grow like this:

| Year | Rate at the year's end | PIXA supply |
|---|---|---|
| 1 | 9.36% | × 1.08 |
| 2 | 8.94% | × 1.17 |
| 5 | 7.68% | × 1.45 |
| 10 | 5.58% | × 1.92 |
| 15 | 3.48% | × 2.33 |
| 20 | 1.38% | × 2.58 |
| 21 | 0.95% | × 2.61 |
| 30 | 0.95% | × 2.80 |

The multiples are relative to the supply at genesis. 85% of nominal issuance becomes PIXA: 70% for content and 15% for witnesses. The fund's 15% is created as PXS. Burns and conversions are left out, because they depend on use. The first 33 days, when the witness weighting issued 1.16 times the schedule, added about 0.18% of the genesis supply that this table leaves out.

## Yield: there is none

**Nothing pays you for holding.**

- **PIXA**, liquid or in savings, earns nothing.
- **Pixa Power** earns nothing by itself. No share of issuance goes to stake.
- **PXS** earns no interest. The rate is fixed at 0, and witnesses cannot set any other ([Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).

**What earns is work:**

| Who | Receives | For |
|---|---|---|
| Authors | 60% of a post's payout, minus any beneficiaries | publishing work that others vote for |
| Curators | 40% of a post's payout | voting early for work that others vote for later. A full vote counts from 2.5 Pixa Power since hardfork 30 ([why](../02-social-layer/voting-and-curation.md#from-vote-to-rshares)). |
| Witnesses | the witness share of issuance | producing blocks and publishing the price feed ([Witnesses and DPoS](../07-governance/witnesses-and-dpos.md)) |
| Proposal workers | pay from the DPF | work that stakeholders vote to fund ([Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md)) |

**Holding without taking part dilutes your share.** Supply grows in every block. Take an account that holds 1% of all PIXA and does nothing for a year. At the end of the year it holds about 0.9%.

This follows the first of the [Design Principles](../01-start-here/design-principles.md#1-contribution-earns-a-share-holding-earns-nothing): new tokens go to contribution, not to capital.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Issuance schedule | 9.5% at Steem's block 7,000,000, falling 0.01 points every 250,000 blocks to 0.95% | same formula, counted from Pixa's genesis: 9.78% at block 0 |
| Split: content / stake / witnesses / fund | Hive: 65 / 15 / 10 / 10% | 70 / 0 / 15 / 15% |
| Reward for holding stake | Hive: 15% of issuance | none |
| Interest on the second unit | Hive: on savings, set by witnesses | none; fixed at 0 |
| Witness pay per block | scaled for 21 witnesses; Hive always runs 21 | nominal since HF30 while fewer than 21 run; before it, 2.33 times nominal with 9 |
| Burns | account fees, conversions, `null` | same |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Allocation & Supply" and "Impact of Token Creation Rate".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §II.4.
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - issuance, its base, its split and witness pay: [database.cpp:1725-1800](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1725-L1800); the hardfork-30 witness pay and fund share, [database.cpp:1803-1839 at v1.30.0](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/database.cpp#L1803-L1839) and [dhf_funding.hpp](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/include/hive/chain/util/dhf_funding.hpp)
  - every constant: [Chain Parameters](../21-reference/chain-parameters.md#issuance)
- **Live chain**:
  - supply and the issuance split: `condenser_api.get_dynamic_global_properties` at block 979,298 (2026-10-08) and 895,415 (2026-10-05); `producer_reward` operations before and after block 949,330
  - the reward fund: `condenser_api.get_reward_fund ["post"]`
  - fee burns: the `clear_null_account_balance` operations in the history of `null`
  - conversions and author rewards: the `fill_collateralized_convert_request`, `fill_convert_request` and `author_reward` operations, from `account_history_api.enum_virtual_ops` over blocks 1 to 895,415
