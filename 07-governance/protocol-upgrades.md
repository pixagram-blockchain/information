# Protocol Upgrades

> **Status: Live.** Hardfork 29 has been active since block 402,205 (2026-09-18 12:00 UTC). Last checked 2026-10-06.

Some of the Pixa chain's rules can change without new software, because witnesses set them by vote. Others are compiled into the node software and change only through a hardfork. This page explains the three kinds of change, how a hardfork activates, what hardfork 29 changed, and who takes part.

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

Hardforks 1 to 28 are Hive's, with Pixa's own settings built in, such as its issuance split and reward curves, and all of them applied at block 1. [Chain Parameters](../11-reference/chain-parameters.md) lists every value that differs from Hive.

## Who takes part

| Who | Part |
|---|---|
| Pixagram SA | Develops the code and publishes releases at [github.com/pixagram-blockchain/pixagram](https://github.com/pixagram-blockchain/pixagram) |
| Anyone | Can read the code, report issues and propose changes there |
| Witnesses | Decide whether to run a release and vote for its hardfork |
| Stakeholders | Elect the witnesses, and can vote out a witness that runs a change they oppose |
| Node operators and apps | Decide whether to follow. A change nobody runs has no effect. |

**The last resort is a fork.** If part of the community rejects a change, it can keep running the old rules as a separate chain. Hive did this from Steem in 2020 ([From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split)).

**Today, few people take this decision.** The 9 witnesses were elected by the votes of five accounts with stake ([Decentralization and Safeguards](decentralization-and-safeguards.md)).

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
| Hardforks applied | Hive: 28 by 2026 | 29: 1 to 28 at block 1, 29 at block 402,205 |
| Signalling and activation | Versions and votes in block headers; activation at a fixed time | same |

## Sources

- [Hive whitepaper](https://hive.io/whitepaper.pdf), §III.2.
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - activation: [database_hardfork.cpp:117-147](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L117-L147)
  - hardfork 29: [database_hardfork.cpp:525-561](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L525-L561) and [1_29.hf](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hardfork.d/1_29.hf)
- **Live chain**: `condenser_api.get_block_header` for blocks 342,000 and 402,205; `condenser_api.get_ops_in_block` for block 402,315, the first author reward.
