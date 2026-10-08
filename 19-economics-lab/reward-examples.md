# Reward Examples

> **Status: Live.** Computed with the rules of hived 1.30.0 (hardfork 30, since block 949,330) and the reward fund as read on 2026-10-08 at block 977,074. Example 2 reproduces a real payout from before hardfork 30 to the unit.

This page does the arithmetic the chain does when a vote lands and when a post pays out, with every intermediate figure, so that a reader can check a payout in their own history or predict one. The rules are explained on [Proof-of-Brain](../02-social-layer/proof-of-brain.md), [Voting and Curation](../02-social-layer/voting-and-curation.md) and [Posting and Rewards](../02-social-layer/posting-and-rewards.md); the constants are on [Chain Parameters](../21-reference/chain-parameters.md). Here there are only numbers, integer arithmetic throughout, as in the code. Amounts are in base units where it matters: 1 PIXA = 1,000 units, 1 VESTS = 1,000,000 units.

## The formulas

```python
# (a) a vote -> rshares                          hive_evaluator_social.cpp:660-718 (v1.30.0)
used_mana = ceil( E * |weight| * 86_400 / 10_000 / 4_320_000 )   # E: effective Pixa Power in VESTS units
rshares   = max(0, used_mana - 50_000)                           # 50,000 since HF30; 50,000,000 before
if seconds_to_payout < 43_200: rshares = rshares * seconds_to_payout // 43_200

# (b) a post's claim on the fund                 util/reward.cpp:7-32, s = 2,500 (content constant)
claim = ((r + s)**2 - s**2) // (r + 4*s)        # r: the post's net rshares; about r - 5,000 for large r

# (c) the fund's denominator, every block        database_comment.cpp:409
recent_claims -= recent_claims * 3 // 1_296_000   # decays by e^(-t / 15 days); every paying post adds its claim

# (d) the payout                                 util/reward.cpp:17-29
payout = reward_balance * claim // (recent_claims + claims paying out in this block)
if payout in PXS at the median feed < 0.020 PXS: payout = 0

# (e) the split                                  database_comment.cpp:227-228, 281-301; database.cpp:979-1035 (v1.30.0)
curation = payout * 40 // 100;  author = payout - curation
liquid_half  = author // 2;  vested_half = author - liquid_half
author_pxs   = liquid_half * print_rate // 10_000, converted to PXS at the median feed, rounded down to 0.001 PXS
author_pixa  = liquid_half - ceil(author_pxs in PIXA)   # since HF30: the PIXA that did not fit a whole 0.001 PXS is paid, not burned
author_vests = vested_half, converted at the VESTS price

# (f) a vote's curation weight                   hive_evaluator_social.cpp:784-831
W(x) = x // approx_sqrt(x + 2*s)                # approx_sqrt: the chain's integer approximation
weight = W(rshares before + this vote) - W(rshares before)
weight //= 1 in the first 24 h, 2 until 72 h, 8 after
curator's share = curation * weight // sum of weights
```

The late-vote factor in (a), the age factors in (f) and the dust test in (d) are the three places where timing changes an amount. Everything else is proportion.

## Example 1: one full vote from 10,000 Pixa Power

An account with E = 10,000 Pixa Power (10,000,000,000 VESTS units), full mana, votes 100% on a fresh post with no other votes.

**(a) Mana and rshares.** `used_mana = ceil(10,000,000,000 × 10,000 × 86,400 / 10,000 / 4,320,000) = 200,000,000`, exactly 2% of the bar. `rshares = 200,000,000 − 50,000 = 199,950,000`.

| Weight | Mana spent | rshares (HF30) | rshares before HF30 |
|---|---|---|---|
| 100% | 200,000,000 (2% of the bar) | 199,950,000 | 150,000,000 |
| 30% | 60,000,000 | 59,950,000 | 10,000,000 |
| 0.25% | 500,000 | 450,000 | 0 |
| 0.01% | 20,000 | 0 | 0 |

**The threshold.** A vote produces rshares when its mana exceeds 50,000, which for a full vote means more than 2.5 Pixa Power: E = 2.500000 VESTS gives 0, E = 2.500001 VESTS gives 1. Before hardfork 30 the deduction was 50,000,000 and the line was 2,500 Pixa Power: a 100-Pixa-Power account's full vote spent 2,000,000 mana and produced nothing; today it produces 1,950,000 rshares ([Voting and Curation](../02-social-layer/voting-and-curation.md#from-vote-to-rshares)).

**(b) to (d) Payout**, with the fund as read on 2026-10-08: `reward_balance` 517,193.258 PIXA, `recent_claims` 9,930,574,867,540, median feed 1.000 PXS = 51.833 PIXA (a placeholder; PXS promises no price).

```
claim  = ((199,950,000 + 2,500)² − 2,500²) / (199,950,000 + 10,000) = 199,945,000
payout = floor(517,193,258 × 199,945,000 / (9,930,574,867,540 + 199,945,000)) = 10,413 units = 10.413 PIXA = 0.200 PXS   (≥ 0.020 PXS: paid)
```

**(e) The split.** Curation 40%: 4.165 PIXA, to the only curator as 4.164999 VESTS. Author 60%: 6.248 PIXA; the liquid half, 3.124 PIXA, becomes 0.060 PXS (`floor(3,124 × 1,000 / 51,833)`), and since hardfork 30 the 0.014 PIXA that did not fit into a whole 0.001 PXS is paid as PIXA instead of being burned (`3,124 − ceil(60 × 51,833 / 1,000) = 14` units); the vested half, 3.124 PIXA, becomes 3.123999 VESTS.

The same vote at 30% gives 59,950,000 rshares and 3.121 PIXA (0.060 PXS). Before hardfork 30 it gave 10,000,000 rshares and 0.520 PIXA, below the minimum, so nothing.

**What a lone full vote is worth today**, with the same fund, for other stakes:

| Voter's Pixa Power | rshares | Payout | Author | Curator |
|---|---|---|---|---|
| 50 | 950,000 | 0: 0.049 PIXA is under 0.020 PXS | — | — |
| 100 | 1,950,000 | 0: 0.101 PIXA is under 0.020 PXS | — | — |
| 1,000 | 19,950,000 | 1.038 PIXA (0.020 PXS) | 0.006 PXS + 0.312 Pixa Power | 0.415 Pixa Power |
| 2,500 | 49,950,000 | 2.601 PIXA (0.050 PXS) | 0.015 PXS + 0.781 Pixa Power | 1.040 Pixa Power |
| 10,000 | 199,950,000 | 10.413 PIXA (0.200 PXS) | 0.060 PXS + 3.124 Pixa Power | 4.165 Pixa Power |
| 100,000 | 1,999,950,000 | 104.137 PIXA (2.009 PXS) | 0.602 PXS + 31.242 Pixa Power | 41.654 Pixa Power |
| 1,000,000 | 19,999,950,000 | 1,039.521 PIXA (20.055 PXS) | 6.016 PXS + 311.857 Pixa Power | 415.808 Pixa Power |

In each row the author also receives the few thousandths of a PIXA that did not fit into a whole 0.001 PXS. The smallest lone full vote that clears the 0.020 PXS minimum today comes from about 998.3 Pixa Power (19,916,369 rshares, 1.037 PIXA). A smaller vote is not wasted: its rshares add to the post's total. Eleven full votes from 100-Pixa-Power accounts make 21,450,000 rshares and pay 1.116 PIXA (0.021 PXS), and the eleven share the curation; ten make 19,500,000 and fall just under the line, because each vote loses its own 50,000. Before hardfork 30 any number of such votes produced nothing.

**Live checks.** The account `wang`, with 50 VESTS of received delegation, voted 100% after hardfork 30; the chain's `effective_comment_vote` recorded 950,000 rshares, as the table says. And the first payouts after hardfork 30 show the conversion remainder: `@saitam/far-away-staying-awake-1790785626144`, paid in block 954,672, received 16.814 PXS, 0.033 PIXA and 871.553993 VESTS. The liquid half was 871,554 units: `floor(871,554 × 1,000 / 51,833) = 16,814` PXS units, `871,554 − ceil(16,814 × 51,833 / 1,000) = 33` units of PIXA. Before hardfork 30 those 33 units were burned and `hive_payout` was always 0 while the print rate was 100%.

## Example 2: a real payout, reproduced to the unit

The post `@bryan/horus-portrait-1790597187843`, published in block 690,312 with the creation time 2026-09-28 12:06:27 (the time of the block before it, which is what the chain records), paid out 7 days later in block 891,898, 2026-10-05 12:06:27. This was **before hardfork 30**, so the deduction is 50,000,000. Three votes, read from the `effective_comment_vote` operations (`account_history_api.enum_virtual_ops`):

| Voter | Time | Age of post | E (VESTS) | Weight | Mana spent | rshares | Chain's rshares |
|---|---|---|---|---|---|---|---|
| `bryan` | 12:10:33 | 4 min | 100.000000 | 100% | 2,000,000 | 0 | 0 |
| `mathiew` | 18:38:42 | 6.5 h | 3,396,923.076920 | 25% | 16,984,615,385 | 16,934,615,385 | 16,934,615,385 |
| `matias` | 19:06:42 | 7.0 h | 733,062.272804 | 75% | 10,995,934,093 | 10,945,934,093 | 10,945,934,093 |

**Curation weights (f).** All three votes fell in the first 24 hours, so no age factor. `mathiew`: W(16,934,615,385) − W(0) = 130,130. `matias`: W(27,880,549,478) − W(16,934,615,385) = 32,069. `bryan`: 0 rshares, weight 0. The chain recorded 130,130, 32,069 and a total of 162,199.

**Claim (b).** net rshares 27,880,549,478; claim = 27,880,544,478 (5,000 less).

**The fund at the payout block.** The fund is read every block, so it was reconstructed from a snapshot 1,493 blocks later (block 893,391: 481,746.405 PIXA and 11,598,498,893,914) by undoing the decay and the issuance between them, 653 units a block in that window: `reward_balance` 481,925.934 PIXA, `recent_claims` 11,610,772,368,671 before this post's claim, 11,638,652,913,149 with it; it was the only post paying out in that block.

**Payout (d).** `floor(481,925,934 × 27,880,544,478 / 11,638,652,913,149) = 1,154,459 units = 1,154.459 PIXA`, which is 22.272 PXS at the feed.

**Split (e).** Curation `floor(0.40 × 1,154,459) = 461,783`; author 692,676.

| Who | Formula | Units | Paid as | Chain's record |
|---|---|---|---|---|
| `mathiew` | 461,783 × 130,130 / 162,199 | 370,482 | 370.481997 VESTS | 370.481997 VESTS |
| `matias` | 461,783 × 32,069 / 162,199 | 91,300 | 91.299999 VESTS | 91.299999 VESTS |
| fund keeps | the rounding | 1 | | |
| `bryan`, liquid half | 692,676 / 2 = 346,338 at 51.833 | | 6.681 PXS | 6.681 PXS |
| `bryan`, vested half | 346,338 | | 346.337997 VESTS | 346.337997 VESTS |

The `comment_reward` operation recorded `payout` 22.272 PXS, `total_payout_value` 13.362 PXS (the author's part in PXS) and `curator_payout_value` 8.909 PXS, all matching. The VESTS figures use the reward VESTS price `(total_vesting_shares + pending rewarded shares) / (fund + pending rewarded PIXA)`, about 0.9999999928 VESTS per PIXA at the time.

**Pending payout check.** The app's "pending payout" figure follows the same arithmetic with the fund of the moment. For `@retro/peach-knight-1791211388189` at block 895,530: net rshares 24,319,843,531, claim 24,319,838,531, fund 483,143.172 PIXA = 9,321.150 PXS, `recent_claims` 11,541,212,091,810: `floor(claim × 9,321,150 / recent_claims) = 19.641 PXS`, which is what the `effective_comment_vote` operation carried as `pending_payout` (the account-history plugin computes it with the fund of the moment).

## Example 3: when the vote lands

Voter A has 100,000 Pixa Power and votes 100% one hour after publication; voter B has 50,000 Pixa Power and votes 100% at different ages. Hardfork 30 rules; the fund of 2026-10-08.

A: 1,999,950,000 rshares, curation weight W(1,999,950,000) − W(0) = 42,642. (The chain's `approx_sqrt(1,999,955,000)` is 46,900 where the true root is 44,720; the approximation is part of the rule.)

| B votes at | B's rshares | B's raw weight | Age factor | B's weight | Post payout | Curation pot | A gets | B gets | B's share |
|---|---|---|---|---|---|---|---|---|---|
| 1 h | 999,950,000 | 11,259 | ×1 | 11,259 | 156.190 PIXA | 62.476 PIXA | 49.425 PIXA | 13.050 PIXA | 20.9% |
| 30 h | 999,950,000 | 11,259 | ÷2 | 5,629 | 156.190 PIXA | 62.476 PIXA | 55.190 PIXA | 7.285 PIXA | 11.7% |
| 80 h | 999,950,000 | 11,259 | ÷8 | 1,407 | 156.190 PIXA | 62.476 PIXA | 60.480 PIXA | 1.995 PIXA | 3.2% |
| 162 h, 6 h before payout | 499,975,000 (× 21,600 / 43,200) | 5,581 | ÷8 | 697 | 130.165 PIXA | 52.066 PIXA | 51.228 PIXA | 0.837 PIXA | 1.6% |

Three things to read off the table. B's vote is half the size of A's but, cast second, its raw weight is about a quarter of A's: the square-root curve rewards being first. The age factors then divide it by 2 or 8. And a vote in the last 12 hours loses rshares too, so it raises the post's payout less: 130.165 instead of 156.190 PIXA.

**Live check of the age factors.** On `@karo/diving-in-clear-waters-1790621283370` (created 2026-09-28 18:48:03), six votes at ages 0.3 h, 40 h, 45 h, 56 h, 94 h and 124 h have raw weights 102,020, 60,041, 88,338, 93,234, 45 and 42; the chain recorded 102,020, 30,020, 44,169, 46,617, 5 and 5: ×1, ÷2, ÷2, ÷2, ÷8, ÷8.

## The constants used

| Constant | Value | Where it is defined |
|---|---|---|
| Vote mana regeneration | 5 days (432,000 s) | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Vote denominator | 10 × 432,000 = 4,320,000 | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Dust deduction | 50,000 rshares since HF30; 50,000,000 before | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Late-vote window | 12 hours | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Payout window | 7 days | [Posts and comments](../21-reference/chain-parameters.md#posts-and-comments) |
| Content constant s | 2,500 | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Recent-claims decay | 15 days | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Curation share | 40% | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Age factors | ×1 to 24 h, ÷2 to 72 h, ÷8 after | [Voting and curation](../21-reference/chain-parameters.md#voting-and-curation) |
| Minimum payout | 0.020 PXS | [Posts and comments](../21-reference/chain-parameters.md#posts-and-comments) |
| Author's liquid half | paid as PXS while the print rate is 100%; the rounding remainder paid as PIXA since HF30 | [Pixa Supra (PXS) and the price feed](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed) |

## Sources

- **Code**, at tag [`v1.30.0`](https://github.com/pixagram-blockchain/pixagram/tree/746118eb3b87dcca768b72fa262ad2aa63e1f177) for the vote evaluator and at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443) for the unchanged rest: [`hive_evaluator_social.cpp:660-718`](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/hive_evaluator_social.cpp#L660-L718) (mana, dust, late damping) and [`784-831`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L784-L831) (curation weight); [`util/reward.cpp:7-71`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/reward.cpp#L7-L71) (claim, payout, curves, `approx_sqrt`); [`database_comment.cpp:129-325, 395-444`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_comment.cpp#L129-L325) (the split and the fund); [`database.cpp:979-1035` at v1.30.0](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/database.cpp#L979-L1035) (the author's PXS and the remainder); [`supplement_operations.hpp:25-73`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/include/hive/chain/util/supplement_operations.hpp#L25-L73) (pending payout); `approx_sqrt` test vector in [`basic_tests.cpp:594-597`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/tests/unit/tests/basic_tests.cpp#L594-L597).
- **Live chain**: `condenser_api.get_reward_fund ["post"]` and `get_dynamic_global_properties` at block 977,074 (2026-10-08 11:07 UTC) and at blocks 893,391, 895,071, 895,416 (2026-10-05); `account_history_api.enum_virtual_ops` for blocks 690,312 to 891,898 (the votes and the payout of Example 2) and for `@karo/diving-in-clear-waters-1790621283370`; the `effective_comment_vote` operation with its `pending_payout` at block 895,530; the `effective_comment_vote` of `wang` after block 949,330; `account_history_api.enum_virtual_ops` for the `author_reward` operations in blocks 950,000 to 979,000.
- The arithmetic was run in a script with integer operations only; every chain figure quoted matches its output to the unit.
