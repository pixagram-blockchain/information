# Supply, Inflation and Yield

> **Status: Live.** Figures were read at block 895,415 on 2026-10-05. While 9 witnesses run, the chain issues about 1.16 times its nominal schedule.

New PIXA is created in every block and paid to the people who keep the network running. This page explains how much is created, where it goes, what is destroyed, and how supply may grow over the coming decades. It also explains why holding tokens earns nothing.

## How much is issued

The yearly rate depends only on the block number *h*:

```
rate(h) = max( 9.78% − 0.01 percentage points × floor(h / 250,000) , 0.95% )
```

- **Today:** 9.75%.
- **Each year:** about 0.42 percentage points lower. A year holds about 42 steps of 250,000 blocks.
- **The floor:** 0.95% from block 220,750,000, about 2047.

**What the rate applies to.** In every block, the rate is applied to all PIXA plus the PXS held outside the fund, valued at the median feed. On 2026-10-05 this gave 0.934 PIXA per block, about 26,900 PIXA a day.

**Where the constants come from.** They are Steem's. Its hardfork 16 chose them so that the rate stood at 9.5% at Steem's block 7,000,000, late in 2016. Pixa counts blocks from its own genesis, so it started at the top of the schedule. Hive, further along the same schedule, issued 5.36% a year on 2026-10-05 ([Chain Parameters](../11-reference/chain-parameters.md#issuance)).

## Where new tokens go

| Recipient | Nominal share | Paid as | On 2026-10-05 |
|---|---|---|---|
| Reward fund, for authors and curators | 70% | PIXA, paid out by votes on posts | about 18,800 PIXA a day |
| Witnesses | 15% | Pixa Power, to the producer of each block | about 9,475 PIXA a day |
| Decentralized Pixa Fund | 15% | PXS, to `pixa.omnibus` | 57.6 PXS a day |
| Holders of Pixa Power | 0% | — | nothing |

Two inherited rules change these shares in practice:

- **Witness pay assumes a full schedule.** While fewer than 21 witnesses run, more of the witness share reaches each active witness. With 9 witnesses, a block paid about 0.329 PIXA on 2026-10-05, more than a full schedule would give; as the count approaches 21, the per-block pay falls to its nominal share.
- **The fund's share is rounded down in every block.** The 0.140 PIXA due to the fund in each block came to 0.0027 PXS at the median feed of 51.833 PIXA per PXS. It was rounded down to 0.002 PXS, about 74% of the share. The loss depends on the feed. At today's issuance, a median above about 140 PIXA per PXS would round the fund's share down to nothing.

Together, the chain issues about **1.16 times** the nominal amount, about 11.3% a year in PIXA-equivalent terms. The PIXA supply itself grows by about 0.982 PIXA a block, because the fund's part is created as PXS. As more witnesses join, the witness part falls back toward its nominal share.

**Not yet paid out.** On 2026-10-05 the reward fund held 483,068.730 PIXA that had been issued for content but not yet paid to anyone. It is released as posts reach their payout, in proportion to the votes they received ([Proof-of-Brain](../02-social-layer/proof-of-brain.md)).

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

| Year | Rate at the year's end | PIXA supply with 21 witnesses | PIXA supply with 9 witnesses |
|---|---|---|---|
| 1 | 9.36% | × 1.08 | × 1.11 |
| 2 | 8.94% | × 1.17 | × 1.22 |
| 5 | 7.68% | × 1.45 | × 1.58 |
| 10 | 5.58% | × 1.92 | × 2.24 |
| 15 | 3.48% | × 2.33 | × 2.84 |
| 20 | 1.38% | × 2.58 | × 3.23 |
| 21 | 0.95% | × 2.61 | × 3.27 |
| 30 | 0.95% | × 2.80 | × 3.57 |

The multiples are relative to the supply at genesis. With 21 witnesses, 85% of nominal issuance becomes PIXA: 70% for content and 15% for witnesses. The fund's 15% is created as PXS. With 9 witnesses for good, the witness part is 2.33 times larger, and PIXA grows at 1.05 times the nominal rate. Burns and conversions are left out, because they depend on use.

## Yield: there is none

**Nothing pays you for holding.**

- **PIXA**, liquid or in savings, earns nothing.
- **Pixa Power** earns nothing by itself. No share of issuance goes to stake.
- **PXS** earns no interest. The rate is fixed at 0, and witnesses cannot set any other ([Chain Parameters](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).

**What earns is work:**

| Who | Receives | For |
|---|---|---|
| Authors | 60% of a post's payout, minus any beneficiaries | publishing work that others vote for |
| Curators | 40% of a post's payout | voting early for work that others vote for later. Votes count only above 2,500 Pixa Power ([why](../02-social-layer/voting-and-curation.md#why-small-votes-count-for-nothing)). |
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
| Witness pay per block | scaled for 21 witnesses; Hive always runs 21 | 2.33 times nominal while 9 run |
| Burns | account fees, conversions, `null` | same |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Allocation & Supply" and "Impact of Token Creation Rate".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §II.4.
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - issuance, its base, its split and witness pay: [database.cpp:1725-1800](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1725-L1800)
  - every constant: [Chain Parameters](../11-reference/chain-parameters.md#issuance)
- **Live chain**, read on 2026-10-05:
  - supply and the issuance split: `condenser_api.get_dynamic_global_properties` at block 895,415
  - the reward fund: `condenser_api.get_reward_fund ["post"]`
  - fee burns: the `clear_null_account_balance` operations in the history of `null`
  - conversions and author rewards: the `fill_collateralized_convert_request`, `fill_convert_request` and `author_reward` operations, from `account_history_api.enum_virtual_ops` over blocks 1 to 895,415
