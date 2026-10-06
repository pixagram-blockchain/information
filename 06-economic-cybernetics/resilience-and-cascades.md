# Resilience and Cascades

> **Status: Live.** The measures on this page come from the running chain, read at block 917,250 on 2026-10-06. The vocabulary comes from ecology and physics, as the PXS design notes use it.

PXS promises no price. The design notes argue that it fails gently rather than suddenly: it has no cliff to fall from and no tightly coupled web to carry a collapse. This page tests that argument with two ideas, resilience and self-organised criticality, and with the chain's own numbers.

## Resilience

C. S. Holling (1973) separated two properties that are easy to confuse. *Stability* is a system's tendency to return to an equilibrium after a disturbance. *Resilience* is its ability to absorb disturbances and still keep the same relationships between its parts. A useful picture is a ball in a landscape of valleys. Each valley is a *basin of attraction*; the ridges between valleys are *thresholds*; a push that carries the ball over a ridge leaves it in a different regime.

Walker, Holling, Carpenter and Kinzig (2004) gave resilience four aspects. Applied to PXS on 2026-10-06:

| Aspect | Meaning | PXS on chain |
|---|---|---|
| **Latitude** | How far the system can be pushed before it crosses a threshold | The collateral ratio can fall from about 804 to 4 before printing stops, and to 7/3 before the haircut starts |
| **Resistance** | How hard it is to push | The 84-hour median and the 3.5-day delay slow every push. The 5% fee and the print stop limit how fast holders and rewards can add PXS. |
| **Precariousness** | How close it already is to a threshold | Far on paper, but the distance is measured at a placeholder price, and 99.04% of all PXS sits in the treasury, outside the measure |
| **Panarchy** | How the systems above and below shape it | Above: the markets PIXA may trade on, The Economist's index, exchange rates, regulators. Below: the witnesses' operators, the app, the Hive codebase. |

The thresholds are on [Chain Parameters](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed); the numbers behind the first three rows are on [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#where-the-network-stands).

## One regime or two

**A defended peg has two basins.** In one, the peg holds. In the other, it has broken, and returning from there is costly when it is possible at all.

**PXS's conversion value has one.** Above a collateral ratio of 7/3, the haircut factor is 1. Below it, the factor falls in a straight line, and when the ratio recovers, it rises back along the same line. There is no separate state to fall into. The print stop is a step, not a slope, but it too reverses as soon as the debt ratio falls below 20%, because the chain recomputes the print rate in every block.

**A market price is another matter.** What the protocol defines is the conversion value. A market can still leave it far behind: SBD closed at 13.76 US dollars on 2017-12-19 and at 0.52 on 2019-11-13, while its conversion delivered about a dollar and about 70 cents ([From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md#sbd-in-practice)). A market can also lose its buyers. PXS has no market yet, so none of this has been observed for it.

## How much dilution the haircut allows

Conversions out of PXS create PIXA. Without a limit, converting every PXS after a collapse in PIXA's value would create PIXA in proportion to the collapse. The haircut limits each hour's price: at the corrected price, all PXS outside the treasury is worth exactly 3/7 of all PIXA ([the haircut](../05-pixa-supra/haircut-corridor-and-settlement.md#the-haircut)).

| Case | PIXA created if every PXS outside the treasury converted |
|---|---|
| Today: 2,414.312 PXS outside the treasury, at today's median | about 125,100 PIXA, 0.12% of all PIXA |
| If all 251,680.531 PXS were outside the treasury, at today's median | about 13.0 million PIXA, 13% of all PIXA |
| At the haircut's limit, at any time | 3/7 of all PIXA |

The limit applies to each hourly price. As conversions burn PXS and add PIXA, the next hour's limit relaxes. The haircut slows dilution and reduces its total; it does not end it.

## Self-organised criticality

Per Bak, Chao Tang and Kurt Wiesenfeld (1987) described systems that drive themselves to a critical state. Their example is a sandpile built one grain at a time. The pile steepens until it reaches a critical slope; from then on, a single grain can set off an avalanche of any size, and avalanche sizes follow a power law, with no typical size. Large events need no large cause. Bak and Kan Chen, whom the design notes cite, described the idea for a general audience in 1991.

The design draws a lesson from it: in a critical system you cannot prevent avalanches by hunting for triggers, because the triggers are ordinary grains. You manage the slope and the connectivity, which decide how far a disturbance travels before it dies out.

## The couplings

| Coupling | What it carries | On 2026-10-06 | What limits it |
|---|---|---|---|
| PXS to PIXA | Everything: PXS settles only in PIXA | total, by design | the haircut, for PIXA holders; nothing, for PXS holders |
| The feed to outside sources | The Economist's index; for the agnostic feed, ECB rates and exchange tickers | all nine feeds use the same index and placeholder | the medians; the agnostic feed publishes nothing when a source fails |
| The feeds to one another | Shared software and shared operators | one program; each update reached every witness then publishing within about a minute and a half | the median, only if the feeds become independent |
| The witnesses to their voters | Elections | six voting accounts on 2026-10-05 ([Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md)) | the 30-day delay on new stake; votes that expire after a year |
| The debt ratio to the treasury | PXS leaving the treasury enters the ratio | 99.04% of all PXS in the treasury | at most 1% of the fund a day, and only by vote |
| The app to its operator | The app and its account service | run by Pixa Rex S.A. ([Who Does What](../01-start-here/who-does-what.md)) | anyone can run a node or another app |

## Where the slope is steep

- **The placeholder.** Every distance to a threshold is computed from an assumed price. If PIXA comes to trade, its first market price may differ from the placeholder by any factor, and the collateral ratio will follow by the same factor within about two days of the witnesses switching to it.
- **The treasury's PXS.** 99.04% of all PXS sits outside the ratios. Paid out to proposals and held, all of it would bring the collateral ratio to about 7.7 at today's median, within a factor of two of the print stop at 4.
- **The allocations.** About 67.5% of all PIXA is stake that the two allocation accounts have still to distribute ([Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md)). How it reaches the market will shape PIXA's market value, and through it every ratio above.
- **Correlated failure.** One feed program, one placeholder and a small set of voters make the parts of the system fail together rather than independently.

## The design's claim, assessed

The design notes say the supra is "engineered not to be un-shockable, but to be non-cascading". Part by part:

| The claim | What the chain shows |
|---|---|
| No cliff: below the floor, the unit degrades continuously and reversibly | Holds for the conversion value: the haircut is linear in the collateral ratio and lifts when it recovers. It does not hold for a market price, which can gap. The print stop is a step, though a reversible one. |
| No chain of promises for a failure to travel down | Holds: there is no issuer, no reserve and no redemption desk. |
| Loose coupling through three separate entities | The entities are separate legal persons. On chain, the couplings that matter today are tight: one feed program, one placeholder, few voting accounts. |
| Failures stay gradual and local | Not yet tested: no disturbance has reached the system. Dilution is limited per hour, not in total. |

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Below the threshold | the haircut, continuous since Steem's hardfork 14 | same |
| Observed under stress | Steem, 2019-11-13: conversions delivered about 70% of a dollar, and SBD closed at about 52% | nothing yet |
| Feed sources | many witnesses reading different exchanges | one placeholder, today |

## Sources

- C. S. Holling, "Resilience and Stability of Ecological Systems", *Annual Review of Ecology and Systematics* 4 (1973), 1–23.
- B. Walker, C. S. Holling, S. R. Carpenter and A. Kinzig, "Resilience, Adaptability and Transformability in Social–ecological Systems", *Ecology and Society* 9(2): 5 (2004).
- P. Bak, C. Tang and K. Wiesenfeld, "Self-organized criticality: An explanation of the 1/f noise", *Physical Review Letters* 59 (1987), 381–384.
- P. Bak and K. Chen, "Self-Organized Criticality", *Scientific American* 264(1) (January 1991), 46–53.
- **PXS design notes** (Pixagram, June 2026), §3.2, §5.3, §5.4 and §8.1.
- **Live values,** read at block 917,250 on 2026-10-06: `condenser_api.get_dynamic_global_properties`, `condenser_api.get_feed_history`, `condenser_api.get_accounts`.
