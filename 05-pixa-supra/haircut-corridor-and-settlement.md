# Haircut, Corridor and Settlement

> **Status: Live.** PXS promises no price. The chain applies Hive's debt limits unchanged: PXS printing stops at a debt ratio of 20%, and the haircut starts above 30%. The corridor of about 3× to 10× in the PXS design notes is not in the code. On 2026-10-06, at block 917,250, neither limit was near: the collateral ratio was about 804×, measured at a placeholder price.

PXS promises no price. What the protocol has instead is a procedure: how a PXS converts into PIXA, and how much less it delivers when the PXS outside the treasury grows large against all PIXA. That reduction is the haircut. This page sets out the procedure in both directions, derives the haircut from the code, compares the design's corridor with the chain's thresholds, and shows how far the network stands from each.

## Three numbers decide everything

| Symbol | What it is | On 2026-10-06 |
|---|---|---|
| *P* | All PIXA, liquid and staked, including the reward fund | 100,675,253.214 PIXA |
| *S* | PXS outside the treasury | 2,414.312 PXS |
| *m* | The median feed, in PIXA per PXS | 51.833 |

*P* is `current_supply` in `condenser_api.get_dynamic_global_properties`. *S* is `current_pxs_supply` in the same call, less the `pxs_balance` of `pixa.omnibus` from `condenser_api.get_accounts`. *m* is `market_median_history` in `condenser_api.get_feed_history`, the median before any haircut.

Two ratios follow from them:

- **Collateral ratio** *R* = *P* ÷ (*S* × *m*): the value of all PIXA divided by the value of the PXS outside the treasury, both at the median feed. About **804** on 2026-10-06.
- **Debt ratio** *d* = 1 ÷ (1 + *R*): the PXS outside the treasury as a share of the combined value. **0.124%** on 2026-10-06.

The treasury's PXS counts in neither ratio. The chain leaves it out of the debt ratio ([database.cpp:2918-2941][db-calc]) and out of the haircut ([2502-2505][db-2502]). The thresholds themselves are on [Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed).

## Converting PXS into PIXA

`convert` takes the PXS from your balance at once. 3.5 days later, the chain burns it and pays you PIXA at the median feed in force at that moment, which already includes any haircut. There is no fee ([database_conversion.cpp:49-71][conv-49]).

- **The rate is fixed at the end, not at the start.** No one knows it when the request is made. This is deliberate: a converter cannot use news that the median has not absorbed yet. Steem's 2016 whitepaper gave the same reason for its one-week delay ([From SBD to PXS](from-sbd-to-pxs.md#sbd-as-designed-in-2016)).
- **A real conversion.** On 2026-09-30 at 15:53:03 UTC (block 752,436), an account asked to convert 31.334 PXS. The request settled on 2026-10-04 at 03:53:00 UTC (block 853,232) for 1,624.135 PIXA, which is 31.334 × 51.833.

## Converting PIXA into PXS

`collateralized_convert` works in two steps ([hive_evaluator_transfer.cpp:539-586][tr-539], [database_conversion.cpp:76-120][conv-76]):

1. **At once.** You lock an amount of PIXA as collateral. The chain converts half of it into PXS at whichever of the last 84 hourly samples gives the fewest PXS, less a 5% fee, and pays you the PXS immediately.
2. **3.5 days later.** The chain works out what your PXS cost at the market median then, plus the 5% fee. It burns that much PIXA and returns the rest of the collateral. The market median is the median without any haircut.

The chain refuses the conversion while printing is stopped, or if the new PXS would take the debt ratio past 20% ([hive_evaluator_transfer.cpp:551][tr-551], [579-580][tr-579]). If by then the market median is more than twice the sample used at the start, meaning PIXA has lost more than half its value against a Big Mac, the collateral no longer covers the cost: the chain keeps all of it and records a warning ([database_conversion.cpp:95-102][conv-95]).

**A real conversion.** On 2026-09-24 at 10:10:18 UTC (block 572,803), an account locked 230,769.130 PIXA and received 2,120.079 PXS at once: half the collateral, 115,384.565 PIXA, at 51.833 × 1.05 = 54.42465 PIXA per PXS. On 2026-09-27 at 22:10:15 UTC (block 673,588) the conversion settled. The chain burned 115,384.557 PIXA and returned 115,384.573.

## When printing stops

While the debt ratio is under 20%, the chain prints PXS: authors receive the PXS half of their rewards in PXS ([Posting and Rewards](../02-social-layer/posting-and-rewards.md#who-receives-what)). At 20% or above, it stops. That half is then paid in PIXA, and new PIXA → PXS conversions are refused ([database.cpp:2943-2964][db-2943], [965-1009][db-965]).

- **The switch is a step.** Hive's hardfork 26 placed the start and the end of the reduction both at 20%, so the print rate is either 100% or 0.
- **In collateral terms,** printing stops when *R* falls to 4.
- **The fund's share keeps arriving.** Each block's share for the [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md) is converted into PXS whatever the print rate ([database.cpp:1783-1787][db-1783]). It lands in the treasury, outside both ratios.
- **The fund keeps paying.** Approved proposals are paid in PXS from the treasury whatever the print rate ([dhf_processor.cpp:161-212][dhf-161]). Once paid out, that PXS counts in both ratios, so the PXS outside the treasury can keep growing while printing is stopped.

## The haircut

Every hour, after taking the new median, the chain asks whether the PXS outside the treasury would be worth more than 30% of the combined value at that median. If so, it replaces the median with the price at which that PXS is worth exactly 30% ([database.cpp:2480-2529][db-2480]):

```text
corrected price = 70 × S  PXS  per  30 × P  PIXA
```

One PXS then converts into 3*P* ÷ 7*S* PIXA, which is less than *m*. As a share of what the feed names:

```text
haircut factor = min( 1 , 3R ÷ 7 )
```

- **It is 1 while *R* is at least 7/3, about 2.33.** Below that it falls in a straight line toward zero: 0.86 at *R* = 2, 0.43 at *R* = 1.
- **It applies at settlement.** A `convert` requested before the haircut and settling while it is in force gets the corrected rate.
- **It applies wherever the chain uses the median:** `convert`, the fund's share of issuance, PIXA sent to the treasury, and the chain's own valuation of PXS. Only the second step of a PIXA → PXS conversion uses the market median without it.
- **It is not permanent.** The chain recomputes it every hour from the market median. When *R* rises above 7/3 again, the next sample removes it.

**What it limits.** At the corrected price, all PXS outside the treasury is worth exactly 3/7 of all PIXA, or 30% of the combined value. Conversions settling at that price can create at most 3*P* ÷ 7 PIXA. Each hour the chain recomputes the correction from the new *P* and *S*, and as conversions burn PXS and add PIXA it relaxes. The haircut therefore slows dilution and reduces its total, without ending it. The code states its purpose: to stop someone holding a large amount of the debt token from using "sharp decline in HIVE price" to convert into the liquid token "and take over the blockchain" ([database.cpp:2482-2486][db-2483]).

## Corridor and thresholds: design and chain

The PXS design notes describe three regimes of the collateral ratio, and a haircut that falls "linearly toward zero" below the lower edge. The chain enforces other numbers:

| Collateral ratio *R* | Design notes, June 2026 | Chain: PXS printing | Chain: haircut factor |
|---|---|---|---|
| 10 and above | "Deep capacity"; the corridor itself "becomes amendable by consensus" | on | 1 |
| 4 to 10 | "Viable corridor", target 5 to 7 | on above 4 | 1 |
| 3 to 4 | "Viable corridor" | off | 1 |
| 7/3 to 3 | "Stressed": the haircut is below 1 | off | 1 |
| below 7/3 | "Stressed" | off | 3*R* ÷ 7 |

Four differences matter:

- **The lower edge.** The design's haircut starts below 3. The chain's starts below 7/3, about 2.33.
- **The print stop.** At 4, the chain stops paying authors in PXS and refuses new conversions into PXS, inside what the design calls the viable corridor. The design notes do not mention it.
- **The upper edge.** The chain has none. Every threshold is a constant compiled into hived, which changes only by a hardfork, at any ratio ([Protocol Upgrades](../07-governance/protocol-upgrades.md)).
- **Thirty per cent of what.** The design says "the Supra's weight" must never exceed "~30% of the Atlas's strength", and calls this "exactly equivalent" to a ratio of 3. Thirty per cent of the Atlas is *R* = 3.33. The chain's 30% is a share of the combined value, *R* = 2.33.

The notes present the corridor as a change to Hive's machinery: "the fixed debt cap becoming a continuous haircut over a corridor". In the code, Hive's cap already is this haircut, continuous below its threshold. Pixa runs it unchanged ([From SBD to PXS](from-sbd-to-pxs.md#what-pixa-kept-and-changed)).

## Where the network stands

On 2026-10-06, *R* was about 804 and the debt ratio 0.124%: printing on, no haircut. Two facts qualify that distance.

**It is measured at a placeholder.** *R* moves in proportion to PIXA's value counted in Big Macs, and today that value comes from an agreed placeholder, not a market ([Oracle and Price Feed](oracle-and-price-feed.md#the-placeholder)). With today's supplies, printing would stop only if PIXA were worth about 200 times less, in Big Macs, than the placeholder assumes, and the haircut would start at about 345 times less.

**Almost all PXS sits in the treasury.** `pixa.omnibus` held 249,266.219 PXS, 99.04% of all PXS, and none of it counts in the ratios. PXS paid to proposals does count while its recipients hold it. If all of the treasury's PXS were outside it, *R* would be about 7.7 at today's median: printing would stop at about 1.9 times less value in Big Macs, and the haircut would start at about 3.3 times less. The fund pays at most 1% of its balance a day, and only to proposals that stakeholders approve ([Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md#how-it-pays)).

## How to tell whether the haircut applies

```bash
curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_feed_history","params":[],"id":1}'
```

- **The two medians.** The haircut is in force when `current_median_history` differs from `market_median_history`. The second is never corrected. On 2026-10-06 both were 51.833 PIXA per PXS.
- **The warning.** Each hour the correction applies, the chain records a `system_warning` virtual operation. Its text uses Hive's names: "HIVE price corrected upward due to 30% HBD cutoff rule, from … to …" ([database.cpp:2517-2524][db-2517]).
- **Printing.** `pxs_print_rate` in `condenser_api.get_dynamic_global_properties` is 10000 while printing is on and 0 while it is stopped.

## What the haircut does not do

- **It does not set a market price.** PXS has no market today. On Steem in 2019, SBD traded below even its reduced conversion value ([From SBD to PXS](from-sbd-to-pxs.md#sbd-in-practice)).
- **It does not protect PXS holders.** It protects PIXA holders against dilution by lowering what each PXS delivers.
- **It does not act on transfers or trades.** It changes what conversions at the median deliver, the fund's included, and the chain's own valuation of PXS.
- **It is not a reserve.** No assets are set aside, and nothing is bought or sold.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Printing limits | Steem, hardfork 14 (2016): reduced between debt ratios of 2% and 5%; hardfork 20 (2018): between 9% and 10%; Hive, hardfork 26 (2022): a step at 20% | Hive's hardfork 26 values |
| Haircut threshold | Steem, hardfork 14: 10%; Hive, hardfork 26: 30% | 30% |
| Treasury in the ratios | Hive: left out of printing since hardfork 24 and of the haircut since hardfork 25 | left out of both since genesis |
| Conversion from the liquid token | none on Steem; collateralized on Hive since hardfork 25 (2021) | collateralized, since genesis |
| What the feed refers to | one US dollar | one Big Mac |

## Sources

- **Code**, at commit [`48f75a2`][pixa-commit]:
  - the median and the haircut: [database.cpp:2418-2533][db-2418]
  - the debt ratio and the print rate: [database.cpp:2918-2964][db-2918]
  - printing in rewards: [database.cpp:965-1009][db-965]
  - conversions: [database_conversion.cpp:34-134][conv-34]; [hive_evaluator_transfer.cpp:523-586][tr-523]
  - the fee arithmetic: [asset.cpp:371-417][asset-371]
  - the constants: [config.hpp:199-202][cfg-199] and [365-372][cfg-365]
- **Live values,** read in one batch request at block 917,250 on 2026-10-06 09:14 UTC: `condenser_api.get_dynamic_global_properties`, `condenser_api.get_feed_history`, `condenser_api.get_accounts` for `pixa.omnibus`, `database_api.list_hbd_conversion_requests`.
- **Conversions:** `condenser_api.get_ops_in_block` for blocks 572,803, 673,588, 752,436 and 853,232.
- **Hardfork dates** for Steem and Hive: the `hardfork_operation` virtual operation in each activation block ([From SBD to PXS](from-sbd-to-pxs.md#sources)).
- **PXS design notes** (Pixagram, June 2026), §4.3, §4.4 and §4.6.

[pixa-commit]: https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443
[db-2418]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2418-L2533
[db-2480]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2480-L2529
[db-2483]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2482-L2486
[db-2502]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2502-L2505
[db-2517]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2517-L2524
[db-2918]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2918-L2964
[db-calc]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2918-L2941
[db-2943]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2943-L2964
[db-965]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L965-L1009
[db-1783]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1783-L1787
[conv-34]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_conversion.cpp#L34-L134
[conv-49]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_conversion.cpp#L49-L71
[conv-76]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_conversion.cpp#L76-L120
[conv-95]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_conversion.cpp#L95-L102
[tr-523]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L523-L586
[tr-539]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L539-L586
[tr-551]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L551
[tr-579]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L579-L580
[asset-371]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/asset.cpp#L371-L417
[dhf-161]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/dhf_processor.cpp#L161-L212
[cfg-199]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L199-L202
[cfg-365]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L365-L372
