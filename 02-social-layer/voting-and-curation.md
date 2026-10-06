# Voting and Curation

> **Status: Live.** The figures were read at block 895,415 on 2026-10-05 and move with the reward fund.

A vote on Pixa does two things. It tells the chain where part of each day's rewards should go, and it earns the voter a share of the rewards of posts they find early. This page explains what a vote costs and what it is worth, and why votes from small accounts currently have no effect.

## Voting mana

Every account has a bar of voting mana whose size equals its effective Pixa Power: its own stake, plus stake lent to it, minus stake it has lent out and this week's power-down instalment.

- **The cost of a vote.** Since hardfork 28, a full-strength (100%) vote costs 2% of the *full* bar, however much is left. Fifty full votes empty a full bar, and a vote's strength does not shrink as the bar runs down. A 50% vote costs half as much.
- **Recharge.** The bar refills by 20% of its size each day, so it fills from empty in 5 days. About 10 full votes a day keeps it steady.
- **Downvotes** draw first on a separate pool, worth a quarter of the bar. They lower a post's payout and earn no curation reward.

## From vote to rshares

The chain turns each vote into *rshares*, its weight in the reward calculation:

```
rshares = mana spent − 50,000,000
```

The result is never below zero. In the last 12 hours before payout it is scaled down further ([late votes](#late-votes)).

### Why small votes count for nothing

The deduction of 50,000,000 is Hive's, unchanged. On Hive, one Hive Power is worth about 1,608 VESTS; on Pixa, one Pixa Power is worth about one VESTS. The same deduction is therefore about 1,600 times heavier here.

A full-strength vote spends 2% of the voter's stake (as raw VESTS), so it produces rshares only when that 2% exceeds 50,000,000. That means more than **2,500 Pixa Power**. Below that, every vote is cancelled entirely.

| Effective Pixa Power | rshares of a full vote | Effect |
|---|---|---|
| 1,000 | 0 | none |
| 2,500 | 0 | none |
| 5,000 | 50,000,000 | half its natural weight |
| 10,000 | 150,000,000 | three quarters of its natural weight |
| 100,000 | 1,950,000,000 | close to its natural weight |

Delegated stake counts toward the bar, so a delegation can lift an account above the line. On 2026-10-05, 23 of the chain's 83 accounts cleared it, and 21 of those can vote (`condenser_api.get_accounts`). Changing the deduction would take a hardfork ([Chain Parameters](../11-reference/chain-parameters.md#voting-and-curation)).

## What a vote is worth

Assume one full-strength vote on a post with no other votes, cast in its first 24 hours, with the reward fund as it stood on 2026-10-05. The figures are rounded:

| Voter's Pixa Power | Post payout | Author's 60% | Curator's 40% (to the voter) |
|---|---|---|---|
| 2,500 | none | — | — |
| 5,000 | 2.09 PIXA (0.040 PXS) | 0.012 PXS + 0.63 Pixa Power | 0.84 Pixa Power |
| 10,000 | 6.28 PIXA (0.121 PXS) | 0.036 PXS + 1.88 Pixa Power | 2.51 Pixa Power |
| 100,000 | 81.6 PIXA (1.57 PXS) | 0.47 PXS + 24.5 Pixa Power | 32.6 Pixa Power |
| 1,000,000 | 833 PIXA (16.1 PXS) | 4.82 PXS + 250 Pixa Power | 333 Pixa Power |

A single vote must come from about 3,740 Pixa Power to lift a post over the 0.020 PXS minimum payout. These figures change daily as the reward fund grows and older claims decay.

PXS promises no price. The PXS amounts above use the median feed of 2026-10-05, 51.833 PIXA per PXS, which is a placeholder ([why](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).

## Curation rewards

Curators share 40% of a post's payout in proportion to their *curation weight*. A vote's weight is how much it raised the square root of the post's total rshares:

```
weight = √(rshares after the vote) − √(rshares before the vote)    (approximately)
```

The chain computes the square root with a fast approximation, so real weights can differ noticeably from this formula.

**Early votes earn most.** The first vote on a post gains the most weight. Each later vote of the same size gains less, because the square root grows more slowly as the total rises.

A post on the live chain showed this on 2026-10-05. While it had three votes, of about 30.0, 0.69 and 0.62 billion rshares, their curation weights were 166,783, 1,369 and 1,198. The first vote held about 98% of the weight.

The age of the post at the moment of the vote also matters:

| Age of the post | Curation weight |
|---|---|
| First 24 hours | full |
| 24 to 72 hours | ½ |
| After 72 hours | ⅛ |

### Late votes

Votes are accepted right up to payout. In the last 12 hours, though, each vote's rshares, up or down, are multiplied by the time left ÷ 12 hours. A vote one hour before payout carries about a twelfth of its weight. This stops a last-minute vote from swinging a payout no one has time to answer.

## Changing your vote

- **Changing or removing.** You can change a vote's weight, or remove it with a weight of 0, any number of times until payout. Every change spends fresh mana; removal costs none and refunds none. After payout, votes are ignored.
- **Self-votes.** The chain allows them. Downvotes and social pressure are the only checks.
- **A first vote** cannot have a weight of 0.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Vote cost | 2% of the full bar since Hive's HF28 | same |
| Curation share | 50% | 40% |
| Curation curve | linear since Hive's HF25 | square-root shaped (convergent) |
| Smallest vote that counts | about 1.6 HP on Hive | more than 2,500 Pixa Power |
| Late-vote damping | last 12 hours | same |

## Sources

- **Vote**: [hive_evaluator_social.cpp:609-856](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L609-L856), covering mana cost, dust deduction, late damping, curation weight and time windows.
- **Curves**: [reward.cpp:60-71](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/reward.cpp#L60-L71).
- **Live chain**: `condenser_api.get_reward_fund ["post"]`, `database_api.get_comment_pending_payouts` and `condenser_api.get_active_votes`, read on 2026-10-05. The worked examples assume the fund's state stays unchanged until payout.
