# Viable System Model

> **Status: Live.** The mechanisms mapped here run on mainnet. The Viable System Model is the PXS design notes' way of describing them, not part of the code. Last checked 2026-10-06.

PXS promises no price. The design notes argue that it is nonetheless a coherent system, and they make the argument with Stafford Beer's Viable System Model: a description of the functions any system needs in order to keep its identity in a changing environment. This page summarises the model, sets the design's mapping against the running chain, and says where the correspondence is exact and where it is still a metaphor.

## The model in brief

Stafford Beer, in *Brain of the Firm* (1972) and *The Heart of Enterprise* (1979), argued that every viable system, from a cell to a company, performs five functions:

| System | Function | What it does |
|---|---|---|
| 1 | Operations | The units that do the work and meet the environment |
| 2 | Coordination | Damps oscillation between the operating units |
| 3 | Control | Allocates resources and keeps operations within bounds, here and now. Its audit channel, 3\*, checks what operations actually do. |
| 4 | Intelligence | Looks outward and ahead, at the environment and the future |
| 5 | Policy | Holds the system's identity: what it is for |

Two more ideas complete it:

- **Recursion.** Every viable system contains viable systems and is contained in one.
- **Algedonic signals.** Pain or pleasure signals that bypass the normal channels when something goes badly wrong, so the whole system hears at once.

The model rests on Ashby's law of requisite variety: a regulator must be able to respond in as many ways as the disturbances it faces ([Variety and Regulation](variety-and-regulation.md)).

## The design's mapping, set against the chain

| System | In the design notes | On chain | How close |
|---|---|---|---|
| 1 · Operations | The Atlas: PIXA and Pixa Power, the activity that bears the load | `current_supply`; publishing, curating and producing blocks. Buying and selling artworks is planned for 2027. | Exact for the base. The activity behind it is young. |
| 2 · Coordination | The 13-week power-down; the block cadence and the median window damp clashing reports | 13 weekly instalments, 3-second blocks, the 84-sample median, the 3.5-day conversion delay | Exact |
| 3 · Control | The haircut over a corridor; the audit is the chain's continuous reading of the collateral ratio | The print stop at a debt ratio of 20% and the haircut above 30%. The chain recomputes the debt ratio every block for printing and every hour for the haircut. | Exact in mechanism. The corridor is not in the code. |
| 4 · Intelligence | The Oracle reads the real-goods environment and reports which way to lean | The witnesses' feeds. Today every feed is the same placeholder. | A channel without a signal yet |
| 5 · Policy | Binding witness consensus holds the identity: PXS measures purchasing power, not a fiat number | The Big Mac reference lives in the feed software and the documentation. The code still names the unit HBD and accepts any feed. Rules change by hardfork. | Weakest: the identity is a convention, not a rule |
| Algedonic alert | The haircut switching on at the corridor's edge | Each hour the haircut applies, the chain records a `system_warning` operation | Exact in mechanism: the chain emits the alarm itself, though below 7/3 rather than at the design's 3 |

## System by system

### 1 · Operations: the Atlas

The chain counts the Atlas exactly: *P*, all PIXA, liquid and staked. What it does not yet contain is the economy the design describes. On 2026-10-06 about 67.5% of all PIXA was stake still held by the two allocation accounts ([The Four Components](../05-pixa-supra/the-four-components.md#atlas-the-collateral-base)), and the marketplace for artworks is planned for 2027 ([Roadmap](../01-start-here/roadmap.md)). The operations exist; their weight is still mostly an allocation waiting to be distributed.

### 2 · Coordination

Several rules damp oscillation, each at the price of a slower response:

- **Stake leaves in 13 weekly instalments,** so a voter stays exposed to the result of its vote for months ([Pixa Power](../04-tokens-and-economy/pixa-power.md#power-down)).
- **New stake waits 30 days** before it counts in governance ([Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md#safeguards-in-the-protocol)). The design notes do not name this rule, but it does System 2's work.
- **The feed passes through two medians,** across witnesses and over 84 hours ([Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#from-the-witnesses-feeds-to-the-median)).
- **Conversions wait 3.5 days,** and settle at the median at the end ([Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#converting-pxs-into-pixa)).

### 3 · Control, and its audit

Control has two instruments on chain, where the design names one:

- **A gate.** At a debt ratio of 20%, PXS printing stops: author rewards stop creating PXS and new conversions into PXS are refused. The fund's share of issuance and proposal pay continue.
- **A rate.** Above 30%, the haircut lowers what each PXS converts into.

Both thresholds are on [Chain Parameters](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed).

The audit channel, 3\*, is public. The chain recomputes the debt ratio in every block, after updating the median ([database.cpp:2349-2361][db-2349]), and anyone can read the inputs with `condenser_api.get_dynamic_global_properties`, `condenser_api.get_feed_history` and, for the treasury's balance, `condenser_api.get_accounts`.

### 4 · Intelligence: the Oracle

System 4 looks outward and ahead. On chain, it looks outward through the witnesses' feeds, and today it sees a constant: every feed divides by the same placeholder, so the system has no reading of PIXA's market ([the placeholder](../05-pixa-supra/oracle-and-price-feed.md#the-placeholder)). Nothing on chain looks ahead. Anticipation happens off chain, in people: witnesses who change their software, and developers who propose hardforks.

### 5 · Policy

The design gives policy to "binding witness consensus" and names the identity it holds: PXS measures an ideal of purchasing power, not a fiat number. The chain holds less than that:

- **The identity is not encoded.** The code calls the unit HBD internally, and accepts any price a witness publishes. That the price refers to a Big Mac is a convention of the feed software and of this documentation.
- **Changes need the witnesses.** A rule changes only by hardfork, approved by a supermajority of the scheduled witnesses ([Protocol Upgrades](../07-governance/protocol-upgrades.md)).
- **The witnesses answer to few voters.** On 2026-10-05, six accounts, five of them with stake, had elected all nine ([Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md)).

In Beer's terms, System 5 exists, but it is narrow, and it rests on practice rather than on rules.

### The algedonic alert

When the haircut applies, the chain records a `system_warning` virtual operation every hour, reading in Hive's words "HIVE price corrected upward due to 30% HBD cutoff rule" ([database.cpp:2517-2524][db-2517]). A PIXA → PXS conversion whose collateral falls short records another ([Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#converting-pixa-into-pxs)). Any node, app or person watching the chain receives both at once. The print stop raises no such signal: it changes one field, `pxs_print_rate`.

## Recursion

PXS's four parts sit inside the Pixa network, which can be read as a viable system of its own:

- **Operations:** publishing, curating and producing blocks.
- **Coordination:** the witness schedule and the medians.
- **Control:** the reward rules and the [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md).
- **Intelligence:** the witnesses, and the developers who propose changes.
- **Policy:** the stakeholders and, off chain, the three entities that develop, steward and operate the project ([Who Does What](../01-start-here/who-does-what.md)).

The network in turn sits inside larger systems: the markets PIXA may trade on, the jurisdictions its entities answer to, and the Hive codebase it follows.

## What the mapping shows, and what it cannot

**It shows** what each mechanism is for. The haircut is a control function, not a guarantee. The medians are coordination. The feed is a sensor, and today a sensor that reads nothing.

**It locates the gaps.** Intelligence has no signal yet, policy rests on few hands, and the base is mostly undistributed.

**It cannot prove viability.** Beer's model lists the functions a viable system needs; having them does not make a system survive. A mapping like this one can be drawn for almost any organisation. Its value lies in the gaps it reveals, not in the fit it claims.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| How the debt-style token is described | a convertible note aimed at one US dollar | a viable system of four parts |
| Who corrects course under stress | in Steem's 2016 whitepaper, witnesses adjusting interest and feeds by hand; in the code since hardfork 14, an automatic limit | the automatic limit; there is no interest to adjust |
| Control instruments | print limits and the haircut | the same, with Hive's 2022 thresholds |

## Sources

- Stafford Beer, *Brain of the Firm* (Allen Lane, 1972; second edition, Wiley, 1981) and *The Heart of Enterprise* (Wiley, 1979).
- W. Ross Ashby, *An Introduction to Cybernetics* (Chapman & Hall, 1956).
- **PXS design notes** (Pixagram, June 2026), §3.2, §5.1 and the glossary.
- **Code**, at commit [`48f75a2`][pixa-commit]: the order of the per-block updates, [database.cpp:2349-2361][db-2349]; the warning, [2517-2524][db-2517].

[pixa-commit]: https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443
[db-2349]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2349-L2361
[db-2517]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2517-L2524
