# From SBD to PXS

> **Status: Historical**, with market and chain figures checked on 2026-10-06. Hardfork dates come from each chain's activation blocks; market prices come from CoinMarketCap and CoinGecko.

PXS promises no price. Its machinery is older than its name: Steem launched a dollar-convertible token in 2016, Hive inherited it in 2020, and Pixa runs Hive's version. This page follows that token through ten years: what it was designed to do, what happened when markets tested it, and what Pixa kept and changed.

## SBD as designed in 2016

Steem's whitepaper of March 2016 introduced *Steem Dollars*, written SMD in that edition and SBD on the chain:

- **A convertible note.** The whitepaper compared it to the convertible notes that fund start-ups: debt that converts into ownership. One SBD converted into a US dollar's worth of STEEM.
- **One direction only.** Holders could convert SBD into STEEM, never STEEM into SBD, and the chain alone decided when to create SBD. Two-way conversion, the whitepaper argued, would let traders exploit the chain's rate.
- **Delays.** The rate was the median of the witnesses' feeds over a week, and every conversion waited a week, so that "neither the traders nor the blockchain has any information advantage regarding the price at the time the conversion is executed."
- **Interest.** SBD paid interest, at a rate set by the witnesses who published the feeds.
- **A debt target.** The whitepaper aimed at a debt-to-ownership ratio of about 5%. If SBD traded below a dollar while the ratio was above 10%, it said, the feeds "should be adjusted upward give more STEEM per SMD": parity was to be defended by diluting STEEM.
- **Its limits, stated.** It cited the impossible trinity: a unit tied to the dollar cannot have a stable exchange rate, free capital movement and an independent monetary policy at once.

## SBD in practice

| Date (UTC) | Event |
|---|---|
| 2016-09-20 15:00 | **Steem hardfork 14** (block 5,137,542). SBD printing is reduced as the debt ratio rises from 2% to 5%, and stops above that. Above 10%, the chain values STEEM higher for conversions, so each SBD converts into fewer STEEM: the haircut. |
| 2016-12-06 16:00 | **Hardfork 16** (block 7,353,249). The conversion delay and the window of the median shrink from a week to 3.5 days. |
| 2017-12-19 | SBD closes at 13.76 USD, with an intraday high of 16.17 USD. With conversion in one direction only, nothing could create SBD to meet demand. |
| 2018 | SBD's average daily close falls from 6.96 USD in January to 0.99 USD in September. |
| 2018-09-25 15:00 | **Hardfork 20** (block 26,256,743). The printing reduction moves to between 9% and 10%. |
| 2019-11-13 | SBD closes at 0.517 USD. Conversions settling from 2019-11-12 to 2019-11-14 paid 4.972 STEEM per SBD. The witnesses' feeds put STEEM at 0.140 USD, so a converted SBD delivered about 0.70 USD: the haircut was in force, and the market priced SBD lower still. |

Hardfork 14 reversed the whitepaper's plan. Where the whitepaper would have given more STEEM per SBD to restore parity, the code gives fewer and lets SBD settle for less. Since hardfork 14, the code's debt limit has adjusted under stress rather than defended the dollar. Other tools did push toward the dollar: interest, set by the witnesses on Steem and on Hive, and on Hive a trading account, the HBD stabilizer, paid for by Hive's fund.

## HBD on Hive

| Date (UTC) | Event |
|---|---|
| 2020-03-20 | Hive launches as a fork of Steem, and SBD balances become HBD ([From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split)). |
| 2020-04-06 | HBD at its lowest recorded price, 0.42 USD. |
| 2020-10-14 | **Hive hardfork 24.** The treasury's HBD leaves the debt ratio that governs printing. |
| 2021-01-31 | HBD at its highest recorded price, 3.97 USD. |
| 2021-06-30 14:00 | **Hardfork 25** (block 55,235,767). HIVE can be converted into HBD, against collateral and a 5% fee. The treasury's HBD leaves the haircut calculation. Interest is paid only on HBD in savings. |
| 2022-10-11 12:00 | **Hardfork 26** (block 68,676,505). The haircut threshold rises from 10% to 30%, and printing stops at 20%. |
| 2025-10-07 to 2026-10-02 | HBD's daily price ranges from 0.83 to 1.10 USD. It is within 5% of one dollar on 180 of the 285 days with data. |

## What the record shows

1. **One-way conversion cannot cap a premium.** In 2017 nothing could create SBD to meet demand, and its price rose to 13 times its reference.
2. **Under stress, the limit delivers less, and the market can price the unit lower still.** On 2019-11-13, a converted SBD delivered about 70% of its dollar, and SBD closed at about 52%.
3. **Conversion both ways, interest and active trading narrowed the band without fixing a point.** Since 2021 HBD has had conversion in both directions, as well as interest on savings and the stabilizer. In the last year it stayed between 17% below and 10% above its dollar. PXS has only the conversion.
4. **The haircut is not new.** It has been in the code since 2016.

## What Pixa kept and changed

**Kept, unchanged.** Conversion into the liquid token after 3.5 days at the median, less the haircut; the haircut above a debt ratio of 30% and the print stop at 20% (Hive's hardfork 26); collateralized conversion from the liquid token (hardfork 25); hourly samples and their 84-sample median; the treasury's exclusion from both ratios ([Haircut, Corridor and Settlement](haircut-corridor-and-settlement.md)).

**Changed:**

- **Interest** is fixed at zero by consensus. Witnesses cannot publish another rate ([Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)).
- **The feed quorum** is a quorum of the scheduled witnesses, rather than Hive's fixed number.
- **Genesis** set a median of 102 PIXA per PXS and seeded the treasury with 245,098.039 PXS ([System Accounts](../21-reference/system-accounts.md#genesis-allocation)).
- **The reference** is one Big Mac instead of one US dollar. It lives in the witnesses' feed software, not in the chain's code, and while PIXA does not trade on any market, every feed divides by an agreed placeholder price for PIXA ([Oracle and Price Feed](oracle-and-price-feed.md#the-placeholder)).
- **The words.** The unit is called Pixa Supra, it is described without a peg, and the haircut is presented as the mechanism itself rather than as a failure of it ([Style Guide](../22-about/style-guide.md#writing-about-pxs)).

**The design's account.** The PXS design notes describe two "mutations" of the inherited machinery. The first, "the reference moves from a fiat unit to a purchasing-power ideal", is real, and it lives in the feed software. The second, "peg-defence is replaced by honest signalling — the fixed debt cap becoming a continuous haircut over a corridor", describes Hive's code as it already was. The continuous haircut dates from Steem's hardfork 14, and the corridor of 3× to 10× is not in Pixa's code.

## Inherited → changed

| | Steem at launch (2016) | Steem, hardfork 14 to 2020 | Hive, since hardfork 26 (2022) | Pixa (2026) |
|---|---|---|---|---|
| Reference | one US dollar | one US dollar | one US dollar | one Big Mac |
| Into the liquid token | after a week | after a week; 3.5 days from hardfork 16 | after 3.5 days | after 3.5 days |
| From the liquid token | not possible | not possible | with collateral and a 5% fee | same as Hive |
| Interest | set by witnesses | set by witnesses | savings only, set by witnesses | none, fixed by consensus |
| Printing limit | none in the code | reduced from 2% to 5%; from 9% to 10% after hardfork 20 | stops at 20% | stops at 20% |
| Haircut | none in the code | above 10% | above 30% | above 30% |
| Feeds needed for a sample | 7 | 7 | 7 | a quorum of the scheduled witnesses |

## Sources

- **Whitepaper:** [Steem whitepaper, March 2016 edition](https://web.archive.org/web/20160815131730/https://steem.io/SteemWhitePaper.pdf), sections "Steem Dollars (SMD)", "Minimizing Fraudulent Feeds", "Mitigating Timing Attacks", "Minimizing Abuse of Conversions", "Sustainable Debt to Ownership Ratios", "Interest" and "Setting Price Feeds".
- **Hardfork activations:** the `hardfork_operation` virtual operation in each activation block, read with `account_history_api.enum_virtual_ops` on `api.hive.blog`, whose history includes Steem's up to block 41,818,752. Hardfork 24's activation time, 2020-10-14 19:31:24 UTC, is recorded in Hive's [`1_24.hf`](https://github.com/openhive-network/hive/blob/1.28.7/libraries/protocol/hardfork.d/1_24.hf).
- **The rules by hardfork:** Pixa's code keeps each hardfork's branch, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443): [config.hpp:365-372](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L365-L372), [database_hardfork.cpp:345-355](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L345-L355) and [506-512](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L506-L512), [database.cpp:2480-2529](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2480-L2529) and [2918-2964](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2918-L2964).
- **Steem in November 2019:** `fill_convert_request_operation` in blocks 38,110,213 to 38,177,929, twelve conversions all paid between 4.9718 and 4.9726 STEEM per SBD; `feed_publish` operations in blocks 38,124,000 to 38,126,400, from 44 witnesses, median 0.140 USD per STEEM. Both read from `api.hive.blog`.
- **Market prices:** [CoinMarketCap, SBD historical data](https://coinmarketcap.com/currencies/steem-dollars/historical-data/), daily closes from 2017-11-01 to 2020-01-01; [CoinGecko, Hive Dollar](https://www.coingecko.com/en/coins/hive_dollar), all-time high and low, and daily prices from 2025-10-07 to 2026-10-02, read on 2026-10-06.
- **The HBD stabilizer:** ["HBD stabilizer algorithm"](https://hive.blog/hbd/@smooth/hbd-stabilizer-algorithm) and ["HBD stabilizer proposal August 2025"](https://inleo.io/@smooth/hbd-stabilizer-proposal-august-2025), by @smooth.
- **PXS design notes** (Pixagram, June 2026), §4.6.
