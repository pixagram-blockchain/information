# Protocol Upgrades

> **Status: Live.** Hardfork 30 has been active since block 949,330 (2026-10-07 12:00 UTC); hardfork 29 since block 402,205 (2026-09-18). Last checked 2026-10-08.

Some of the Pixa chain's rules can change without new software, because witnesses set them by vote. Others are compiled into the node software and change only through a hardfork. This page explains the three kinds of change, how a hardfork activates, what hardforks 29 and 30 changed, and who takes part.

## Three kinds of change

| Kind | Examples | Who decides | How |
|---|---|---|---|
| Witness parameters | Account creation fee, maximum block size, subsidy for account tickets | The scheduled witnesses | Each publishes values; the chain uses their median |
| The price feed | PIXA per PXS | The scheduled witnesses | The chain takes the median feed once an hour, and conversions use the median of the last 84 hourly samples |
| Software outside consensus | API nodes, the Hivemind indexer behind communities and feeds, the app, the feed software | Whoever runs it | Each operator updates its own software; the chain is unaffected |
| Consensus rules | Issuance, rewards, limits, what each operation does | The witnesses, by running a new version | A hardfork |

## How a hardfork activates

1. **Release.** Developers publish a new version of `hived` that names the hardfork's number and its earliest time.
2. **Upgrade and signal.** Each witness that installs it reports in its blocks the version it runs and the hardfork it votes for, with that time.
3. **Quorum.** The chain counts the scheduled witnesses voting for the same hardfork and time. Once a supermajority agree, the hardfork is scheduled. If support falls below that before its time, it is unscheduled.
4. **Activation.** The hardfork applies in the first block whose timestamp is at or after its time.
5. **Nodes follow.** Every node running the new version applies the same change in the same block. A node left on the old version computes a different state from that block on and must upgrade to follow the chain.

The required share is read from the chain, not assumed: `get_witness_schedule` reports `hardfork_required_witnesses`.

## Hardfork 29

| Date (UTC) | Block | Event |
|---|---|---|
| 2026-09-16 | | The witnesses upgrade to 1.29.0 and signal HF29 for 2026-09-18 12:00. |
| 2026-09-16 09:48 | 342,000 | Enough witnesses have signalled to schedule it. |
| 2026-09-18 12:00 | 402,205 | HF29 applies, in a block produced by `nodeprime`. |

**What it changed**

- **The reward fund's denominator.** At genesis, Pixa applied Hive's hardfork 21 value for the total of recent claims: about 5.0 × 10¹⁷, a 2019 Steem figure. Every early payout fell below the 0.020 PXS minimum and was paid as nothing. Hardfork 29 lowered the total to at most 2.75 × 10¹³, about 18,000 times less. The first author reward was paid 110 blocks later ([Proof-of-Brain](../02-social-layer/proof-of-brain.md#what-pixa-changed)).
- **The hardfork quorum.** It records, where the API reports it, the number of witnesses a hardfork needs, so that a chain running fewer than a full set of witnesses can still upgrade.

## Hardfork 30

| Date (UTC) | Block | Event |
|---|---|---|
| 2026-10-06 08:11 to 08:50 | | The hardfork is written and reviewed (commits `eb4574a`, `d986a23`). |
| 2026-10-06 13:32 to 15:32 | 922,413 to 924,776 | The nine witnesses upgrade to 1.30.0 and signal HF30 for 2026-10-07 12:00, `initminer` first and `nodeprime` last. |
| 2026-10-07 12:00 | 949,330 | HF30 applies, in a block produced by `rex`. Every node applied it in the same second and stayed on one fork. |
| 2026-10-07 12:42 | | Release 1.30.0 is tagged (commit `746118e`), recording block 949,330. |

The release compiles in the activation time, and a node applies the hardfork only when the witnesses' vote names that same time, so a vote cannot move it earlier.

**What it changed**

- **Small votes count.** The dust deduction every vote pays fell from 50,000,000 to 50,000 rshares, so a full-strength vote counts from 2.5 Pixa Power instead of 2,500. A 100-Pixa-Power account, which could not move a reward before, now can ([Voting and Curation](../02-social-layer/voting-and-curation.md#from-vote-to-rshares)).
- **Witness pay is the nominal share.** Hive weights each block's pay to spread 21 blocks' worth over the witnesses present, so with 9 witnesses each block paid 21/9 of the share and the chain issued about 11.3% a year in PIXA-equivalent terms instead of 9.75%. Since HF30 every block pays the nominal 15% share while fewer than 21 witnesses are scheduled: about 0.141 instead of 0.329 PIXA a block ([Witnesses and DPoS](witnesses-and-dpos.md#how-witnesses-are-paid)).
- **The DPF receives its exact share.** Each block's share was converted to PXS and rounded down to 0.001, which at 51.833 PIXA per PXS paid 0.002 of the 0.0027 PXS due, about 11% of issuance instead of 15%. Since HF30 consecutive blocks pay the exact amount between them; hourly proposal payments stopped losing their rounding the same way, and the PIXA that does not fit into a whole 0.001 PXS when an author's reward is converted is paid to the author instead of burned ([Chain Parameters](../21-reference/chain-parameters.md#issuance)).
- **Custom operations are priced by size.** A `custom_json` or `custom` payload costs Resource Credits in proportion to its length, where a 64 KiB payload cost the same as a tiny one ([Resource Credits](../04-tokens-and-economy/resource-credits.md)).
- **A transaction carries at most 1,000 signatures**, checked before any is verified ([Transaction Lifecycle](../11-protocol-reference/transaction-lifecycle.md#3-signing)).
- **Owner-key history is recorded**, so that account recovery can undo an owner-key change made after 2026-10-07 12:00 UTC ([Keys and Recovery](../08-guides/keys-and-recovery.md)).
- **A witness needs approval from 1% of all stake to be scheduled** ([Witnesses and DPoS](witnesses-and-dpos.md#how-witnesses-are-elected)).

The release notes, [`doc/hf30-security-upgrade.md`](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/doc/hf30-security-upgrade.md), describe the changes and the review that preceded them; this page keeps to what a user of the chain sees.

Hardforks 1 to 28 are Hive's, with Pixa's own settings built in, such as its issuance split and reward curves, and all of them applied at block 1. [Chain Parameters](../21-reference/chain-parameters.md) lists every value that differs from Hive.

## Who takes part

| Who | Part |
|---|---|
| Pixagram SA | Develops the code and publishes releases at [github.com/pixagram-blockchain/pixagram](https://github.com/pixagram-blockchain/pixagram) |
| Anyone | Can read the code, report issues and propose changes there |
| Witnesses | Decide whether to run a release and vote for its hardfork |
| Stakeholders | Elect the witnesses, and can vote out a witness that runs a change they oppose |
| Node operators and apps | Decide whether to follow. A change nobody runs has no effect. |

**The last resort is a fork.** If part of the community rejects a change, it can keep running the old rules as a separate chain. Hive did this from Steem in 2020 ([From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split)).

**Today, few people take this decision.** The 8 witnesses were elected by the votes of seven accounts, five of them with stake ([Decentralization and Safeguards](decentralization-and-safeguards.md)).

## Check the state yourself

```bash
rpc() { curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"$1\",\"params\":$2,\"id\":1}"; }

rpc database_api.get_hardfork_properties '{}'      # last hardfork, and the next one with its time
rpc condenser_api.get_witness_schedule '[]'        # hardfork_required_witnesses, majority_version
```

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Hardfork quorum | a fixed supermajority of 21 witnesses | a supermajority of the scheduled witnesses |
| Hardforks applied | Hive: 28 by 2026 | 30: 1 to 28 at block 1, 29 at block 402,205, 30 at block 949,330 |
| Signalling and activation | Versions and votes in block headers; activation at a fixed time | same |

## Sources

- [Hive whitepaper](https://hive.io/whitepaper.pdf), §III.2.
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - activation: [database_hardfork.cpp:117-147](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L117-L147)
  - hardfork 29: [database_hardfork.cpp:525-561](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L525-L561) and [1_29.hf](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hardfork.d/1_29.hf)
- **Code**, at tag [`v1.30.0`](https://github.com/pixagram-blockchain/pixagram/tree/746118eb3b87dcca768b72fa262ad2aa63e1f177): [1_30.hf](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/hardfork.d/1_30.hf), the constants in [config.hpp:255-282](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/include/hive/protocol/config.hpp#L255-L282), and [`doc/hf30-security-upgrade.md`](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/doc/hf30-security-upgrade.md).
- **Live chain**: `condenser_api.get_block_header` for blocks 342,000, 402,205 and 949,330; `condenser_api.get_ops_in_block` for block 402,315, the first author reward; `block_api.get_block_range` over blocks 900,000 to 949,330 for the witnesses' `hardfork_version_vote` extensions.
