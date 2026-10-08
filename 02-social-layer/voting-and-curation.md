# Voting and Curation

> **Status: Live.** Since hardfork 30 (2026-10-07) a full vote counts from 2.5 Pixa Power. The figures were read at block 977,074 on 2026-10-08 and move with the reward fund.

A vote on Pixa does two things. It tells the chain where part of each day's rewards should go, and it earns the voter a share of the rewards of posts they find early. This page explains what a vote costs and what it is worth, and what hardfork 30 changed for small accounts.

## Voting mana

Every account has a bar of voting mana whose size equals its effective Pixa Power: its own stake, plus stake lent to it, minus stake it has lent out and this week's power-down instalment.

- **The cost of a vote.** Since hardfork 28, a full-strength (100%) vote costs 2% of the *full* bar, however much is left. Fifty full votes empty a full bar, and a vote's strength does not shrink as the bar runs down. A 50% vote costs half as much.
- **Recharge.** The bar refills by 20% of its size each day, so it fills from empty in 5 days. About 10 full votes a day keeps it steady.
- **Downvotes** draw first on a separate pool, worth a quarter of the bar. They lower a post's payout and earn no curation reward.

## From vote to rshares

The chain turns each vote into *rshares*, its weight in the reward calculation:

```
rshares = mana spent − 50,000          (since hardfork 30; 50,000,000 before)
```

The result is never below zero. In the last 12 hours before payout it is scaled down further ([late votes](#late-votes)).

### The dust threshold, before and after hardfork 30

Every vote loses a fixed number of rshares, so that the smallest votes count for nothing. Until 2026-10-07 the deduction was Hive's, 50,000,000. On Hive one Hive Power is worth about 1,608 VESTS; on Pixa one Pixa Power is worth about one VESTS, so the same deduction was about 1,600 times heavier here: a full-strength vote, which spends 2% of the voter's stake as raw VESTS, produced rshares only above **2,500 Pixa Power**, and in the chain's first month only 21 accounts could move a reward.

Hardfork 30 divided the deduction by 1,000. A full-strength vote now counts from **2.5 Pixa Power**, about Hive's threshold in PIXA terms, and 75 of the chain's 100 accounts clear it on 2026-10-08 (`condenser_api.get_accounts`). Resource Credits, not the threshold, limit vote spam.

| Effective Pixa Power | rshares of a full vote, since HF30 | Before HF30 |
|---|---|---|
| 2.5 | 0 | 0 |
| 50 | 950,000 | 0 |
| 100 | 1,950,000 | 0 |
| 1,000 | 19,950,000 | 0 |
| 2,500 | 49,950,000 | 0 |
| 10,000 | 199,950,000 | 150,000,000 |
| 100,000 | 1,999,950,000 | 1,950,000,000 |

Delegated stake counts toward the bar. Changing the deduction again would take a hardfork ([Chain Parameters](../21-reference/chain-parameters.md#voting-and-curation)).

## What a vote is worth

Assume one full-strength vote on a post with no other votes, cast in its first 24 hours, with the reward fund as it stood on 2026-10-08. The figures are rounded; [Reward Examples](../19-economics-lab/reward-examples.md) shows the arithmetic:

| Voter's Pixa Power | Post payout | Author's 60% | Curator's 40% (to the voter) |
|---|---|---|---|
| 100 | none: 0.10 PIXA is under the 0.020 PXS minimum | — | — |
| 1,000 | 1.04 PIXA (0.020 PXS) | 0.006 PXS + 0.31 Pixa Power | 0.41 Pixa Power |
| 2,500 | 2.60 PIXA (0.050 PXS) | 0.015 PXS + 0.78 Pixa Power | 1.04 Pixa Power |
| 10,000 | 10.4 PIXA (0.200 PXS) | 0.060 PXS + 3.12 Pixa Power | 4.16 Pixa Power |
| 100,000 | 104 PIXA (2.01 PXS) | 0.60 PXS + 31.2 Pixa Power | 41.7 Pixa Power |
| 1,000,000 | 1,040 PIXA (20.1 PXS) | 6.02 PXS + 312 Pixa Power | 416 Pixa Power |

A single vote must come from about 1,000 Pixa Power to lift a post over the 0.020 PXS minimum payout on its own; smaller votes add up, so several together can. These figures change daily as the reward fund grows and older claims decay.

PXS promises no price. The PXS amounts above use the median feed of 2026-10-08, 51.833 PIXA per PXS, which is a placeholder ([why](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). Since hardfork 30 the author also receives the few thousandths of a PIXA that did not fit into a whole 0.001 PXS.

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
| Smallest full vote that counts | about 1.6 HP on Hive | more than 2.5 Pixa Power since HF30; 2,500 before |
| Late-vote damping | last 12 hours | same |

## Sources

- **Vote**: [hive_evaluator_social.cpp:609-856](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L609-L856), covering mana cost, dust deduction, late damping, curation weight and time windows; the hardfork-30 deduction, [hive_evaluator_social.cpp:710 at v1.30.0](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/hive_evaluator_social.cpp#L710) and [config.hpp:255-260](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/include/hive/protocol/config.hpp#L255-L260).
- **Curves**: [reward.cpp:60-71](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/reward.cpp#L60-L71).
- **Live chain**: `condenser_api.get_reward_fund ["post"]` and `condenser_api.get_accounts` for all 100 accounts, read on 2026-10-08; `database_api.get_comment_pending_payouts` and `condenser_api.get_active_votes` on 2026-10-05. The worked examples assume the fund's state stays unchanged until payout.
