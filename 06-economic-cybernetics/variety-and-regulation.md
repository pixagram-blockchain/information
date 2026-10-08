# Variety and Regulation

> **Status: Live.** The rules discussed here run on mainnet. The vocabulary is W. Ross Ashby's, as the PXS design notes use it. Last checked 2026-10-06.

PXS promises no price. The design notes defend that choice with a law from cybernetics: only variety can absorb variety. This page explains the law, lists the disturbances PXS faces and the responses the chain has to them, and shows where the variety the law demands actually comes from.

## The law

*Variety* is the number of distinguishable states something can be in. A regulator tries to keep an essential variable within bounds while disturbances push it about. W. Ross Ashby's law of requisite variety (1956) says that the variety of the outcome can be reduced only by variety in the regulator: "only variety can destroy variety". A regulator with fewer distinct responses than there are distinct disturbances cannot hold the outcome to one value.

A designer has three ways to satisfy the law:

1. **Give the regulator more variety:** more kinds of response, or faster ones.
2. **Attenuate:** filter the disturbances before they reach the regulator.
3. **Widen the goal:** accept a band of outcomes instead of a single point.

## Two ways to pick the goal

**A defended peg picks a point:** one unit, one dollar. Its regulator is a reserve that buys and sells, and it must answer every disturbance in size and in time. The design notes call this "a minimum-variety regulator pointed at a high-variety environment": it holds until a disturbance exceeds the reserve.

**PXS picks a band.** Its essential variable is the collateral ratio, not a price. While the ratio is healthy, the regulator does nothing. When it is not, the regulator lets the outcome move with the disturbance: the print stop halts new PXS from author rewards and conversions, and the haircut lowers what each PXS delivers ([Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md)).

**What the band does, stated plainly.** Widening the goal from a point to a band lowers the variety the regulator needs. The part of the disturbance that the regulator no longer absorbs passes to the holder, as variation in what a PXS delivers. In the law's own terms, PXS meets requisite variety partly by accepting more variety in its outcome. The design notes' phrase for this is "Risk is relocated, not removed."

## The disturbances

| Disturbance | How it reaches PXS | On 2026-10-06 |
|---|---|---|
| PIXA's market value moves | through the feeds into the median, and so into the collateral ratio | no market; every feed uses the placeholder |
| The price of a Big Mac moves | through each witness's input; The Economist publishes its index twice a year | 6.22 USD, the July 2026 US price, in every feed |
| Exchange rates move | through the agnostic feed's conversion between currencies | the agnostic feed is not in use |
| A witness errs or misbehaves | through its feed | all nine feeds equal |
| Holders convert | each conversion creates PIXA or PXS | four conversions pending, 1,046.854 PXS in all |
| The fund pays out | PXS leaving the treasury enters the debt ratio | one funded proposal, on 2026-10-05 |
| The allocations are distributed | stake reaching the market changes the supply of PIXA for sale | about 67.5% of all PIXA still in the allocation accounts |

## The chain's responses

| Response | Triggered by | What it changes |
|---|---|---|
| **Stop printing** | a debt ratio of 20% | Author rewards stop creating PXS; conversions into PXS are refused. |
| **Haircut** | a debt ratio above 30% | Each PXS converts into less PIXA, in proportion to the shortfall. |
| **Delay** | every conversion | 3.5 days, settled at the median at the end. |
| **Fee** | every PIXA → PXS conversion | 5%. |

The values are on [Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed). On chain, then, the regulator has one switch, one continuous lever and two fixed frictions. Its further responses are made by people: witnesses change their software or their feeds, stakeholders change witnesses, and witnesses adopt hardforks that change the thresholds. Those responses take hours to weeks.

## Attenuators

An attenuator reduces the variety that reaches a regulator. The chain and the feed software have five:

| Attenuator | What it filters | What it costs |
|---|---|---|
| The median across witnesses | one wrong or dishonest feed: alone, it can shift the sample at most to a neighbouring feed, and not at all while the others agree | nothing, if the feeds are independent; if they are not, it filters nothing |
| The median over 84 hours | changes lasting less than about 42 hours | real changes reach conversions about 42 hours late |
| The median across market pairings, in the agnostic feed | one bad trade on a thin market | needs more than one market |
| The ±50% limit per publish, in the agnostic feed | a single absurd reading | a large real move takes several hours to pass through each witness |
| The 3.5-day conversion delay | conversions timed on news | the converter carries the price risk for 3.5 days |

**Attenuation needs independence.** A median across nine feeds filters errors only if the feeds can err independently. On 2026-10-06 the nine feeds were one computation made nine times: the same index, the same placeholder and the same software, and each update reached every witness then publishing within about a minute and a half ([feed history](../05-pixa-supra/oracle-and-price-feed.md#what-it-has-read-since-genesis)). The agnostic feed is designed to restore independence: each witness reports the Big Mac it observes, in its own currency, from markets of its choice.

## Feedback orders

The design notes, following Beer, describe a ladder of control:

- **First order** pursues a goal set from outside. A defended peg's "one unit, one dollar" is first-order.
- **Second order** chooses how to pursue its goal. The haircut chooses to deliver less rather than to spend a reserve.
- **Third order** chooses the goal itself. The notes argue that the replaceable basket and the amendable corridor make PXS third-order.

On chain, each order has a definite owner:

| Order | What changes | Who changes it | How |
|---|---|---|---|
| Second | what a PXS delivers under stress | the code | automatically, every hour |
| Third | the reference: what the feed measures | each witness, in its own software | no vote is needed; the median decides how much one witness's change matters |
| Third | the thresholds | the witnesses together | a hardfork, approved by a supermajority of the scheduled witnesses ([Protocol Upgrades](../07-governance/protocol-upgrades.md)) |

Third-order change is not peculiar to PXS: on any chain of this family the witnesses can change the rules by hardfork. As on Steem and Hive, the reference itself sits outside consensus, so it can change without the agreement the word "consensus" suggests. What is new on Pixa is that the design means the reference to vary by place and to be replaceable.

## Acting only on a flow

System dynamics separates stocks, which accumulate, from flows, which change them. The design notes hold that PXS acts only on a flow: "the Atlas is a stock and cannot be commanded, supply is a stock and is never minted or burned to chase a price, the Supra is definitional — only the Macro flows, and the haircut moves it."

The chain bears this out. It never trades and never touches a balance to steer a price. The print stop closes the inflows from author rewards and conversions, and the haircut lowers the rate at which the flow out of PXS becomes PIXA; the fund's share and proposal pay continue under both. Every other change in the stocks comes from rules that do not aim at a price: issuance, rewards and conversions that holders choose to make.

## What has been tested

- **The sensor has passed no variety.** Since genesis the feed has changed twice, each time by a software update ([Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#what-it-has-read-since-genesis)).
- **The regulator has never acted.** Printing has been on since genesis, and no haircut has applied.
- **So no disturbance has tested the system yet.** How it behaves under stress is known from its code and from the record of SBD and HBD, which ran the same machinery ([From SBD to PXS](../05-pixa-supra/from-sbd-to-pxs.md)), not from its own history.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Essential variable | in the 2016 whitepaper, the debt token's price near one US dollar; in the code, the debt ratio | the collateral ratio; no target price |
| Responses | interest set by witnesses, print limits, the haircut | print stop and haircut; no interest |
| Independence of the feeds | each witness reads exchanges of its choice | one placeholder today; the agnostic feed is designed for independent readings |

## Sources

- W. Ross Ashby, *An Introduction to Cybernetics* (Chapman & Hall, 1956), chapter 11, "Requisite Variety".
- Stafford Beer, *Brain of the Firm* (Allen Lane, 1972) and *The Heart of Enterprise* (Wiley, 1979).
- **PXS design notes** (Pixagram, June 2026), §3.2, §5.2 and §5.5.
- **Rules and code:** [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#sources) and [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#sources).
- **Live values,** read on 2026-10-06: `condenser_api.get_feed_history`, `database_api.list_hbd_conversion_requests`, `condenser_api.get_accounts`.
