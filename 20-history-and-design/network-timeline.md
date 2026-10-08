# Network Timeline

> **Status: Live.** Dated from the chain's blocks, the repositories' commits and the published documents. Last entry 2026-10-08.

Every dated fact about the Pixa network in one place: what happened, when, and where the date comes from. Each entry is a block timestamp, a commit, a release or a document, so it can be checked. Events that are only planned are on the [Roadmap](../01-start-here/roadmap.md); the Steem and Hive history that leads up to genesis is on [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md).

Times are UTC. Blocks come every 3 seconds, but a slot is missed now and then, so a block's time is read from `condenser_api.get_block_header`, not computed from its number: by 2026-10-08 the head block, 979,867, sat 1,075 slots, about 54 minutes, behind where an unbroken sequence would put it. Where PXS is mentioned, PXS promises no price; the feed figures are the witnesses' reference, not a market.

## Before genesis

| Date | Event | Source |
|---|---|---|
| 2016-07-06 | Daniel Larimer publishes the three-phase plan for Steem that Pixagram's design answers | [The Plan Revisited](the-plan-revisited.md) |
| 2020-03-20 | Hive forks from Steem; Pixa's code descends from Hive's | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split) |
| 2025-11-19 | Hive's hardfork 28, the last one Pixa inherits; hived 1.28.7 is the release Pixa forks | [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md) |
| 2025-12-20 | Pixagram's essay "How Pixagram Completes the Vision for Blockchain World Domination" | [Essays](essays.md) |
| 2026-05-01 | `@pixagram/dpixa` 1.5.4, the JavaScript library, at its last commit | [SDKs and Libraries](../09-developers/sdks-and-libraries.md) |
| August 2026 | Pixa Rex S.A. replaces Pixa Operations S.A. as the operator | [Who Does What](../01-start-here/who-does-what.md) <!-- retired-ok --> |
| 2026-08-18 to 08-28 | PAPH 3.0.0 to 5.3.0, the perceptual hash library | [PAPH](../15-search-and-indexing/paph.md) |

## 2026-09: genesis and hardfork 29

| Date and time | Block | Event | Source |
|---|---|---|---|
| 2026-09-04 12:00:00 | 0 | **Genesis.** Three balances written: 75,000,000 VESTS to `pixa.rex`, 25,000,000 VESTS to `pixa.team`, backed by 100,000,000 PIXA in the vesting fund, and the fund's seed, 245,098.039 PXS, to `pixa.omnibus`. Hive's hardforks 1 to 28 apply at block 1. The feed starts at 102.000 PIXA per PXS, set by the code. | [Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md); `get_block_header [1]` |
| 2026-09-04 12:00:03 | 1 | The first block, produced by `initminer` | `condenser_api.get_block_header` |
| 2026-09-04 17:39 | | The witnesses' first feed: 51.000 PIXA per PXS, from the January 2026 Big Mac index at a 0.12 USD placeholder for PIXA | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#what-it-has-read-since-genesis) |
| 2026-09-04 18:32 to 18:40 | | `pixa.team` distributes 16,510,000 VESTS to six accounts | [Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md) |
| 2026-09-05 | | pixa.org publishes the node operator guide, version 1.0 | [Become a Witness](../10-node-operators/become-a-witness.md) |
| 2026-09-05 18:12 | | `pixa.rex` distributes 15,750,000 VESTS to the operator's working account `pixa` and two others | [Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md) |
| 2026-09-07 12:37 | | The feed moves to 51.833 PIXA per PXS: the July 2026 index edition, 6.22 USD | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#what-it-has-read-since-genesis) |
| 2026-09-12 | | The first communities; 12 by 2026-10-04, including the Proposals, Governance and Development portals | [Roadmap](../01-start-here/roadmap.md) |
| 2026-09-13 11:18 | | Proposal 0, the first DPF proposal, by `matias`: a one-day test of the fund's threshold | `database_api.list_proposals` |
| 2026-09-16 | | The witnesses upgrade to 1.29.0 and signal hardfork 29 for 2026-09-18 12:00 | [Protocol Upgrades](../07-governance/protocol-upgrades.md#hardfork-29) |
| 2026-09-16 09:48 | 342,000 | Enough witnesses have signalled; hardfork 29 is scheduled | `get_block_header [342000]` |
| 2026-09-18 12:00:00 | 402,205 | **Hardfork 29.** The reward fund's denominator is reset, so payouts stop rounding to nothing; the hardfork quorum scales to the witnesses present. Block produced by `nodeprime`. | [Protocol Upgrades](../07-governance/protocol-upgrades.md#hardfork-29) |
| 2026-09-18 12:05:30 | 402,315 | The first author reward ever paid | [Roadmap](../01-start-here/roadmap.md#sources) |
| 2026-09-18 12:17 | | Commit `48f75a2` merges the hardfork-29 branch and records block 402,205 in the code | [`pixagram` repository](https://github.com/pixagram-blockchain/pixagram/commit/48f75a28840c24e5a5b42ccb4f94dc8668ecb443) |
| 2026-09-24 10:37 | | Proposal 2, the return proposal of `pixa.omnibus`: 1,000,000 PXS a day until 2036-09-24, the threshold below which no proposal is paid | [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md) |
| 2026-09-24 10:54 | | Proposal 1, by `rex`: 110.000 PXS a day until 2026-12-31 to cover account creation | [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md) |

## 2026-10: hardfork 30

| Date and time | Block | Event | Source |
|---|---|---|---|
| 2026-10-04 | | The app's code at commit `ca1d157`, version 2.0.0, from which the product pages are described | [`pixagram-ui-dev`](https://github.com/pixagram-blockchain/pixagram-ui-dev/commit/ca1d15762b52ec08f33c69ca9afa34bb78c0df52) |
| 2026-10-05 23:36:12 | 905,693 | Hivemind stops multiplying vote rshares by a million: votes before this block weigh a million times votes after it in Hot and Trending until the older posts pay out, around 2026-10-12. An inherited indexer rule, not a chain event. | [Feed and Discovery](../14-product/feed-and-discovery.md#how-hot-and-trending-are-ranked) |
| 2026-10-06 08:11 to 08:50 | | Commits `eb4574a` and `d986a23`: hardfork 30 written and reviewed | [`pixagram` repository](https://github.com/pixagram-blockchain/pixagram/commits/v1.30.0) |
| 2026-10-06 13:32 to 15:32 | 922,413 to 924,776 | The nine witnesses upgrade to 1.30.0 and signal hardfork 30 for 2026-10-07 12:00, `initminer` first and `nodeprime` last | Block headers' `hardfork_version_vote` extensions |
| 2026-10-07 12:00:00 | 949,330 | **Hardfork 30.** The vote dust threshold falls from 50,000,000 to 50,000 rshares; witness pay per block is the nominal share while fewer than 21 witnesses run; DPF funding and proposal pay stop truncating; custom operations are priced by size; a transaction may carry at most 1,000 signatures; owner-key history is recorded from here on. Block produced by `rex`. | [Protocol Upgrades](../07-governance/protocol-upgrades.md#hardfork-30) |
| 2026-10-07 12:42 | | Tag `v1.30.0`, commit `746118e`, merges the branch and records block 949,330 | [`pixagram` repository](https://github.com/pixagram-blockchain/pixagram/releases/tag/v1.30.0) |
| 2026-10-08 | | 8 witnesses scheduled, all on 1.30.0; 6 public API nodes | `condenser_api.get_witness_schedule`, `get_witnesses_by_vote` |

## Figures over time

Values a reader may want to compare with today's. Each is the value at the date given; the live value is one call away ([Chain Parameters](../21-reference/chain-parameters.md#reading-live-values)).

| Figure | 2026-09-04 | 2026-10-05 | 2026-10-08 | Call |
|---|---|---|---|---|
| Median feed, PIXA per PXS | 102.000, then 51.000 | 51.833 | 51.833 | `get_current_median_history_price` |
| Scheduled witnesses | 1 (`initminer`) | 9 | 8 | `get_witness_schedule` |
| Witness pay per block | | 0.329 PIXA | 0.141 PIXA | `producer_reward` operations |
| Vote dust deduction | 50,000,000 rshares | 50,000,000 | 50,000 | code |
| Smallest full vote that counts | 2,500 Pixa Power | 2,500 | 2.5 | code |
| Reward fund balance | 0 | 481,746.405 PIXA | 517,193.258 PIXA | `get_reward_fund` |
| Accounts | 9, three of them with balances | 83 | 100 | `get_account_count` |
| PIXA supply | 100,000,000 | | 100,778,228.955 | `get_dynamic_global_properties` |
| PXS supply | 245,098.039 | | 250,870.204 | `get_dynamic_global_properties` |

## How to date something yourself

```bash
rpc() { curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"$1\",\"params\":$2,\"id\":1}"; }

rpc condenser_api.get_block_header '[949330]'            # the timestamp and producer of a block
rpc database_api.get_hardfork_properties '{}'            # last hardfork and its block
rpc account_history_api.get_ops_in_block '{"block_num":949330,"only_virtual":true}'   # the hardfork operation
```

A transaction's block is in its account history (`condenser_api.get_account_history`); a post's creation time is in `bridge.get_post`.

## Sources

- **Chain:** `condenser_api.get_block_header` for blocks 1, 342,000, 402,205, 864,000, 905,693 and 949,330; `block_api.get_block_range` over blocks 900,000 to 949,330 for the `hardfork_version_vote` extensions; `database_api.list_proposals`; `condenser_api.get_witness_schedule` and `get_witnesses_by_vote` on 2026-10-05 and 2026-10-08; `get_dynamic_global_properties` and `get_reward_fund` on 2026-10-08.
- **Repositories:** [`pixagram`](https://github.com/pixagram-blockchain/pixagram) commit dates for `48f75a2`, `eb4574a`, `d986a23`, `8e50002` and `746118e`; [`pixagram-ui-dev`](https://github.com/pixagram-blockchain/pixagram-ui-dev) commit `ca1d157`; [`dpixa`](https://github.com/pixagram-blockchain/dpixa) commit `fddb47d`; [`paph-js`](https://github.com/pixagram-blockchain/paph-js) CHANGELOG.
- **Documents:** pixa.org's node operator guide, version 1.0 of 2026-09-05; the essays listed on [Essays](essays.md).
- The other pages cited in each row hold the detail and their own sources.
