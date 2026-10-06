# Supracoin vs Stablecoin <!-- retired-ok -->

> **Status: Live.** PXS promises no price. The mechanisms compared here run on mainnet; *supracoin* is the PXS design notes' name for the category they place PXS in. This page compares mechanisms and states no legal classification. Last checked 2026-10-06.

A common question about PXS is whether it is a stablecoin. <!-- retired-ok -->
The PXS design notes answer that the question starts from the wrong ruler: it measures PXS against a fiat currency, when PXS is built to stand beside one. This page sets out that answer through the mechanisms, so that a reader can check it: what a defended unit relies on, what PXS has instead, and where the risk ends up.

## What PXS promises

PXS promises no price. It has no peg, cannot be redeemed for money and pays no interest, and no one stands behind its value. A PXS converts into newly created PIXA at the median of the witnesses' feeds, less the haircut. Everything below follows from these facts, not from the name given to them.

## What a defended unit relies on

A unit aimed at one unit of a fiat currency usually combines three mechanisms:

1. **A target price** that it defends: one unit of the currency.
2. **Redemption** at that price, by an issuer, typically on demand.
3. **A reserve** that the issuer holds to pay redemptions.

When the reserve or the issuer gives way, the unit breaks from its target. PXS has none of the three:

| | A unit aimed at a fiat currency | PXS |
|---|---|---|
| Target price | one unit of the currency, defended | none: what a conversion delivers varies, and falls under stress |
| Redemption | at par, from the issuer | none: the protocol converts PXS into PIXA at the median feed, less the haircut |
| Reserve | held by the issuer to pay redemptions | none: the PIXA a conversion pays is created for it |
| Where the risk sits | in the reserve and the issuer's solvency | in the honesty of the witnesses' feeds and in PIXA's market value; PIXA holders carry the dilution, within the haircut's limit |

## Money and currency

The design notes borrow two ideas from writers on money.

- **Currency is not money.** In Mike Maloney's distinction, a currency is a medium of exchange and a unit of account: portable, durable, divisible and fungible. Money is all of that and also a store of value over long periods. On this view, a unit tied to a fiat currency is currency, not money.
- **Money pays no yield.** Alan Hibbard argues that money pays no yield because it is a store of value rather than a risk position; yield comes from taking risk. The design gives this as the reason PXS pays no interest.

The design places PXS at neither pole. It orients toward the property that separates money from currency, purchasing power, and declines money's guarantee. Orientation is not a promise: a PXS can deliver more or less than a Big Mac's worth of PIXA, and under stress it delivers less.

## Four kinds of monetary unit

| | Fiat currency | Commodity money | Stablecoin | Supracoin (PXS) <!-- retired-ok --> |
|---|---|---|---|---|
| Reference | the issuing state's decision | its own substance | a fiat currency | a Big Mac, read by the witnesses |
| What it rests on | confidence in the issuer | the commodity itself | a reserve held by the issuer | nothing set aside: it settles in PIXA that each conversion creates |
| Behaviour of its value | loses purchasing power as its supply grows | follows the commodity | follows its currency while the reserve holds | follows what the feed and PIXA's market make of it, less the haircut under stress |
| Issuer | a central bank | none | the issuer | none; created by protocol rules |
| Typical failure | debasement | loss or theft | the reserve or the issuer fails, and the unit breaks from its reference | PIXA loses value, and conversions deliver less |

Adapted from the design notes, figure 6. The last column describes the chain as it runs today.

## What a holder holds

The design's image is a chain of claim checks. A unit referenced to a fiat currency is a claim on an issuer's reserve, and the reserve is usually a claim on a bank or a state. Each link is a promise resting on the one before, and a failure anywhere travels forward along the chain.

A PXS is not on that chain. It is a balance that the protocol converts into PIXA, which it creates for the purpose. There is no counterparty to fail and no reserve to run on. That does not make PXS independent:

- **The conversion depends on the feed,** which today is a placeholder ([Oracle and Price Feed](oracle-and-price-feed.md#the-placeholder)).
- **What the PIXA is worth depends on PIXA's market,** which does not exist yet.
- **Conversions dilute PIXA holders.** The haircut limits how fast ([Haircut, Corridor and Settlement](haircut-corridor-and-settlement.md#the-haircut)).

The design notes put it in one line: "Risk is relocated, not removed."

## The design's test, applied to the chain

The design notes propose a test. If the four terms *Oracle, Atlas, Supra* and *Macro* describe a unit completely, and the four terms *peg, reserve, defence* and *issuer* cannot describe it at all, the unit is a supracoin and not a stablecoin. <!-- retired-ok -->
Applied to the running chain:

| Term | On the Pixa chain |
|---|---|
| Peg | None. No code targets a PXS price. The feed is an input to conversions, not a target. |
| Reserve | None. The treasury's 249,266.219 PXS are PXS, spent on proposals, not assets held behind PXS. |
| Defence | None. The chain never buys or sells PXS. When PXS grows large, it stops printing at a debt ratio of 20%, then cuts what each PXS delivers above 30% ([thresholds](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). It adjusts; it does not defend. |
| Issuer | None in the protocol. PXS is created by fixed rules: author rewards, the fund's share of issuance and conversions. The 245,098.039 PXS seeded at genesis were set by the chain's code. No account can change these rules alone: a change needs a hardfork that the witnesses adopt, and on 2026-10-05 six accounts, five of them with stake, had elected all nine witnesses ([Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md)). |

The protocol has no issuer; who elects the witnesses decides how far that holds in practice.

## What the word does not change

- **Safety.** Calling PXS a supracoin makes it no safer. What PXS is follows from its mechanism, not from its name ([Style Guide](../13-about/style-guide.md#writing-about-pxs), statement 4).
- **Where the risk goes.** Risk is moved, not removed. It sits with PXS holders, who carry the feed's errors, the haircut and the need to find a buyer for the PIXA they receive; with PIXA holders, who carry the dilution; and with the honesty of the witnesses.
- **The reference.** A Big Mac is a direction, never a destination. Under stress, a PXS settles for less than the reference names.
- **Legal status.** This page compares mechanisms. It states no legal classification of PXS or of any other token.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| How the unit was described | "Steem Dollars": a convertible note aimed at one US dollar | a supracoin that promises no price |
| Reference | one US dollar | one Big Mac |
| Interest | yes; on Hive, in savings only | none |
| Under stress | the debt limit cuts what a conversion delivers, as on Steem in 2019 | the same rule, presented as the mechanism itself |

## Sources

- **PXS design notes** (Pixagram, June 2026), Parts II, III and VI, and §8.1.
- Mike Maloney, *Hidden Secrets of Money*, episode 1 (2013).
- Alan Hibbard, *Hidden Secrets of Value*, ["Saving vs. Investing"](https://goldsilver.com/hidden-secrets-of-value/savings-vs-investing/), GoldSilver.
- [Steem whitepaper, March 2016 edition](https://web.archive.org/web/20160815131730/https://steem.io/SteemWhitePaper.pdf), "Steem Dollars (SMD)".
- The mechanism and its code: [Haircut, Corridor and Settlement](haircut-corridor-and-settlement.md#sources); Steem in 2019: [From SBD to PXS](from-sbd-to-pxs.md#sbd-in-practice).
