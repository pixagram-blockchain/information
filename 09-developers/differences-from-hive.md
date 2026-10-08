# Differences from Hive

> **Status: Live.** Compared with hived 1.28.7, the release Pixa forks. Checked against the Pixa code at tag `v1.30.0`, the gateway at commit `4a271e8` and the public nodes on 2026-10-05 and 2026-10-08.

Pixa runs Hive's code and speaks Hive's JSON-RPC, so Hive's documentation applies here with PIXA for HIVE and PXS for HBD. This page lists everything else that changes how you write code: the chain's identity, what the public API does to requests and responses, what Hivemind reports, and the protocol rules that differ. Every protocol value is on [Chain Parameters](../21-reference/chain-parameters.md); this page says what the values mean for a program.

## Summary

| Area | What differs | Details |
|---|---|---|
| Identity | Chain ID, key prefix `PIX`, symbols PIXA and PXS | [Identity and assets](#identity-and-assets) |
| Public API | A gateway renames 28 field names in responses and 19 in requests, and routes social calls to Hivemind | [The public API](#the-public-api) |
| Your own node | Hive's field names; Pixa's are ignored without an error | [Talking to hived directly](#talking-to-hived-directly) |
| Hivemind | Vote rshares a million times the chain's for votes before block 905,693; reputation not computed; 20 results per `bridge` call; community names start with `portal-` | [Hivemind](#hivemind) |
| Protocol | No interest, no stake reward, restricted genesis accounts, a vote dust threshold a thousand times smaller than Hive's since hardfork 30 | [Protocol rules that change code](#protocol-rules-that-change-code) |
| Libraries | Hive libraries sign amounts with Hive's symbol bytes | [Libraries](#libraries) |

## Identity and assets

| | Hive | Pixa |
|---|---|---|
| Chain ID | `beeab0de` followed by zeros | `706978616772616d` followed by zeros: the ASCII word `pixagram` |
| Public-key prefix | `STM` | `PIX` |
| Liquid token | HIVE, `@@000000021`, 3 decimals | PIXA, same NAI and decimals |
| Second token | HBD, `@@000000013`, 3 decimals | PXS, same NAI and decimals |
| Staked unit | VESTS, `@@000000037`, 6 decimals | same |
| Symbol bytes in the legacy wire format | `STEEM`, `SBD` | `PIXA`, `PXS` |
| VESTS per liquid token | about 1,608, falling | about 1, flat |

- **Write amounts with Pixa's symbols:** `"1.000 PIXA"`, `"0.020 PXS"`, `"1000.000000 VESTS"`. A library that serializes Hive's symbol bytes produces signatures the chain rejects. hived checks a signature against both the legacy and the HF26 serialization of a transaction, so a client that signs the HF26 form, which identifies assets by NAI, avoids symbol bytes altogether.
- **Never hard-code Hive's VESTS ratio.** On Pixa one VESTS is worth about one PIXA, against about 1,608 VESTS per HIVE on Hive, and the ratio stays flat because no issuance goes to stakers. Compute it from `total_vesting_fund_pixa ÷ total_vesting_shares` ([Pixa Power](../21-reference/chain-parameters.md#pixa-power-staking)).

## The public API

All six public nodes run the same gateway: Caddy, then an OpenResty configuration named Jussi, in front of hived and Hivemind ([Chain Architecture](chain-architecture.md)).

### Routing

| Calls | Answered by |
|---|---|
| `bridge.*`, `follow_api.*`, `tags_api.*` | Hivemind |
| 23 `condenser_api` calls: `get_followers`, `get_following`, `get_follow_count`, `get_content`, `get_content_replies`, `get_discussions_by_trending`, `…_by_hot`, `…_by_created`, `…_by_promoted`, `…_by_blog`, `…_by_feed`, `…_by_comments`, `…_by_author_before_date`, `get_replies_by_last_update`, `get_blog`, `get_blog_entries`, `get_active_votes`, `get_reblogged_by`, `get_account_votes`, `get_trending_tags`, `get_post_discussions_by_payout`, `get_comment_discussions_by_payout`, `get_account_reputations` | Hivemind; of these, `get_discussions_by_promoted` and `get_account_votes` fail, because Hivemind has no promoted sort and no longer supports account votes ([JSON-RPC Surface](../12-api-reference/json-rpc.md#what-is-not-served)) |
| Everything else: 139 methods in `account_by_key_api`, `account_history_api`, `block_api`, `condenser_api`, `database_api`, `jsonrpc`, `market_history_api`, `network_broadcast_api`, `rc_api` and `reputation_api` | hived |

Not served by any of the six: websockets, `wallet_bridge_api` (needed by the [CLI wallet](../10-node-operators/cli-wallet.md)) and `transaction_status_api`. To learn whether a transaction is in a block, call `database_api.is_known_transaction`, then `condenser_api.get_transaction` with its id once the block is irreversible; before that, `get_transaction` answers `Unknown Transaction` ([Transaction Lifecycle](../11-protocol-reference/transaction-lifecycle.md#8-irreversible)). The whole surface is on [JSON-RPC Surface](../12-api-reference/json-rpc.md).

### Field renames

The gateway renames Hive's field names in every response, and the names marked *both* also in requests to hived. Requests to Hivemind are not renamed.

| Hive name | Pixa name | Direction |
|---|---|---|
| `hbd_balance` | `pxs_balance` | both |
| `savings_hbd_balance` | `savings_pxs_balance` | both |
| `hbd_seconds`, `hbd_seconds_last_update`, `hbd_last_interest_payment` | `pxs_seconds`, `pxs_seconds_last_update`, `pxs_last_interest_payment` | both |
| `savings_hbd_seconds`, `savings_hbd_seconds_last_update`, `savings_hbd_last_interest_payment` | `savings_pxs_seconds`, `savings_pxs_seconds_last_update`, `savings_pxs_last_interest_payment` | both |
| `reward_hbd_balance`, `reward_hive_balance`, `reward_vesting_hive` | `reward_pxs_balance`, `reward_pixa_balance`, `reward_vesting_pixa` | both |
| `reward_hbd`, `reward_hive` (in `claim_reward_balance`) | `reward_pxs`, `reward_pixa` | both |
| `percent_hbd` (in `comment_options` and posts) | `percent_pxs` | both |
| `hbd_amount`, `hive_amount` (in escrow operations) | `pxs_amount`, `pixa_amount` | both |
| `hbd_exchange_rate`, `last_hbd_exchange_update` (witnesses) | `pxs_exchange_rate`, `last_pxs_exchange_update` | both |
| `hbd_interest_rate` | `pxs_interest_rate` | both |
| `current_hbd_supply`, `init_hbd_supply` | `current_pxs_supply`, `init_pxs_supply` | responses only |
| `hbd_print_rate`, `hbd_start_percent`, `hbd_stop_percent` | `pxs_print_rate`, `pxs_start_percent`, `pxs_stop_percent` | responses only |
| `total_vesting_fund_hive`, `total_reward_fund_hive`, `pending_rewarded_vesting_hive` | `total_vesting_fund_pixa`, `total_reward_fund_pixa`, `pending_rewarded_vesting_pixa` | responses only |
| `dhf_interval_ledger` | `dpf_interval_ledger` | responses only |

**Every other name stays Hive's.** For example, `author_reward` operations keep `hbd_payout` and `hive_payout`, `collateralized_convert_immediate_conversion` keeps `hbd_out`, the treasury's funding operation is still called `dhf_funding`, and `database_api.get_config` still prints `HIVE_` constants. Operation and API names are all Hive's.

**Amounts inside responses.** hived itself writes PIXA and PXS. The gateway also rewrites any amount followed by `TESTS`, `TBD` or `HBD`, such as `"1.000 HBD"`, to PIXA or PXS wherever it appears in a response, text included.

### Batches, ids and limits

| | Behaviour on 2026-10-05 |
|---|---|
| Batch requests | Allowed when every call goes to hived. The gateway routes a batch by its *first* call: a batch starting with a chain call fails its social calls with `Could not find API bridge`, and a batch starting with a social call fails with `id required`, because Hivemind takes one call per request. |
| The `id` in replies | hived returns it as sent; Hivemind returns it as a string (`"7"` for `7`). |
| Request size | Up to about 1 MiB; larger requests get HTTP 413. Requests above about 10 KiB are passed to hived without routing or renaming, so a large `bridge` call fails and a large broadcast keeps its bytes. |
| Results per `bridge` call | `limit` 1 to 20; Hivemind rejects 21 ([Feed and Discovery](../14-product/feed-and-discovery.md#paging)). |
| Browser access | `Access-Control-Allow-Origin: *` on every node. |
| Compression | zstd or gzip, as the client accepts. |
| Busy node | A call can fail with `Unable to acquire database lock`; retry it. |

### Known issue: renames inside text

The gateway applies its renames to the whole body of a request or response, not only to field names. On 2026-10-05, a transaction whose post text contained `pxs_balance` reached hived from all six public nodes as `hbd_balance`.

- **Writing.** If any text you sign, whether a title, body, `json_metadata`, memo or `custom_json` payload, contains one of the 19 Pixa names marked *both* above, and the request is under about 10 KiB, hived receives different bytes from the ones you signed. The transaction fails with `missing required posting authority` (or *active* authority). Larger requests pass the gateway untouched, which is why artworks are unaffected. Until the gateway is fixed, keep these names out of signed text, or broadcast through a node without the gateway.
- **Reading.** Text in responses that contains a Hive name from the table, or an amount followed by `TESTS`, `TBD` or `HBD`, is shown renamed. A program that re-serializes a transaction from a response to check its signature can fail for the same reason.

### Talking to hived directly

Your own node, including a witness node, has no gateway. hived reads and writes Hive's field names only, and it ignores a name it does not know **without an error**. Sent to hived directly, `"percent_pxs": 5000` in a `comment_options` operation was read as the default 10000.

dpixa writes Pixa's names in five operations: `claim_reward_balance`, `comment_options`, `escrow_transfer`, `escrow_release` and `witness_update`. Sent to hived directly, those fields fall back to their defaults. That is harmless when a field holds its default anyway, such as `pxs_interest_rate: 0` or `percent_pxs: 10000`; otherwise hived reconstructs a different transaction and rejects its signature. Broadcast these operations through a public node. Every other operation works either way.

## Hivemind

- **rshares are scaled for old votes.** Hivemind multiplies the chain's `rshares` by one million for votes in blocks before 905,693, an inherited rule from Steem's early chain, and keeps the chain's value for later votes. One vote on 2026-10-05: 16,180,769,231,000,000 in `bridge.get_ranked_posts` and `condenser_api.get_active_votes`, 16,180,769,231 in the chain's `effective_comment_vote` operation. The chain crossed block 905,693 on 2026-10-05 23:36 UTC, so until the posts voted before then pay out, Hivemind's Trending and Hot weigh those votes a million times the newer ones ([Feed and Discovery](../14-product/feed-and-discovery.md#how-hot-and-trending-are-ranked)). Do reward arithmetic with hived's values.
- **Reputation is not computed.** Hivemind's reputation tracker does not run on the public nodes, so the `condenser_api.get_account_reputations` that the gateway routes to Hivemind returns 0 for every account, and `bridge.get_profile` and the post lists return 25, the bottom of Hivemind's display scale, for everyone. hived's `reputation_api.get_account_reputations` has the real figures.
- **Twenty results per call.** `bridge.get_ranked_posts` and the other list calls accept `limit` up to 20, not Hive's 100.
- **Community names** are `portal-` followed by digits, where Hive uses `hive-` ([Communities](../02-social-layer/communities.md)).
- **Social methods are Hive's.** Feeds, posts, communities and notifications use the same calls and shapes, with the renamed fields above.

## Protocol rules that change code

| Rule | On Pixa | What it means for code |
|---|---|---|
| Interest on PXS | Always 0; witnesses cannot publish another value | Do not offer interest on savings. `pxs_interest_rate` is 0. |
| Reward for holding stake | None ([Issuance](../21-reference/chain-parameters.md#issuance)) | VESTS do not grow in value. Rewards come from publishing, curating and producing blocks. |
| Content constant and dust | A vote loses 50,000 rshares since hardfork 30 (50,000,000 before), so a full-strength vote counts from 2.5 Pixa Power ([Voting and Curation](../21-reference/chain-parameters.md#voting-and-curation)) | Compute rshares as `mana spent − 50,000`; a post still pays nothing under 0.020 PXS, about 1,000 Pixa Power of votes today. |
| Custom operation cost | Resource Credits grow with the payload since hardfork 30 ([Chain Parameters](../21-reference/chain-parameters.md#transaction-and-block-size)) | Budget a 64 KiB `custom_json` at nine times a small one's execution cost. |
| Signatures | At most 1,000 per transaction since 1.30.0 | No real transaction approaches it. |
| Curation share | 40% of post rewards | Use 40%, not Hive's 50%, when estimating payouts. |
| Genesis accounts | `pixa.rex` and `pixa.team` can only transfer VESTS ([System Accounts](../21-reference/system-accounts.md#restricted-accounts-pixarex-and-pixateam)) | A `transfer` can carry a VESTS amount, which Hive forbids. Parse VESTS in transfers. |
| Treasury | `pixa.omnibus`, paid in PXS; the return proposal is id 2 ([DPF](../21-reference/chain-parameters.md#decentralized-pixa-fund-dpf)) | Do not assume `hive.fund` or proposal id 0. |
| Hardfork quorum | Not Hive's fixed 17 of 21 ([Protocol Upgrades](../07-governance/protocol-upgrades.md#how-a-hardfork-activates)) | Read `hardfork_required_witnesses` from `get_witness_schedule`; do not hardcode 17. |
| Size limits | Transactions up to the voted block size less 256 bytes, about 2 MiB; `custom_json` up to 64 KiB ([sizes](../21-reference/chain-parameters.md#transaction-and-block-size)) | An artwork fits in one `comment` operation; the public gateway stops at about 1 MiB per request. |
| Account creation fee | 20.000 PIXA median on 2026-10-08 | Read it from `get_chain_properties`. |
| Account recovery | Owner-key history is recorded since hardfork 30, block 949,330 ([accounts](../21-reference/chain-parameters.md#accounts-and-keys)) | A recovery can undo only owner-key changes made after 2026-10-07 12:00 UTC. |

## Libraries

| Library | Reads | Signs operations without amounts | Signs operations with amounts |
|---|---|---|---|
| `@pixagram/dpixa` 1.5.4 | yes | yes | yes, through a public node |
| `@hiveio/dhive` 1.3.2, with `chainId` and `addressPrefix: "PIX"` | yes; helpers that parse amounts fail with `Invalid asset symbol: PXS` | yes | **no**: it serializes Hive's symbol bytes |
| `cli_wallet` in the node image | yes | yes | yes; it uses Hive's field names, such as `convert_hbd` |

[SDKs and Libraries](sdks-and-libraries.md) has the details and the tests.

## Sources

- **Gateway:** [`jussi/nginx.conf`](https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/jussi/nginx.conf) at commit `4a271e8` (unchanged since `7e57cca`): routing at lines 18-51, request renames at 63-85, response renames at 87-117, amount rewriting at 119-154, whole-body application at 189-193 and 219-233. Compression: [`ssl-proxy/Caddyfile`](https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/ssl-proxy/Caddyfile).
- **Tests on 2026-10-05:** `jsonrpc.get_methods`, batch requests, request sizes, response headers and `condenser_api.get_transaction_hex` with a body containing `pxs_balance`, against all six public nodes; `percent_pxs` sent to a local hived 1.29.0; rshares compared between `bridge.get_ranked_posts` and the voter's `effective_comment_vote` in `condenser_api.get_account_history`. **On 2026-10-08:** `bridge.get_profile` against `reputation_api.get_account_reputations`; `bridge.get_ranked_posts` with `limit` 20 and 21; `get_transaction` on a reversible block; the rshares of votes before and after block 905,693.
- **Code** at tag [`v1.30.0`](https://github.com/pixagram-blockchain/pixagram/tree/746118eb3b87dcca768b72fa262ad2aa63e1f177) for the hardfork-30 rules, through [Chain Parameters](../21-reference/chain-parameters.md); at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443): asset symbols in [`asset_symbol.hpp:41-56`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/asset_symbol.hpp#L41-L56); the witness property names the chain reads in [`hive_evaluator.cpp:160-188`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L160-L188); everything else through [Chain Parameters](../21-reference/chain-parameters.md).
- **dpixa** at commit [`fddb47d`](https://github.com/pixagram-blockchain/dpixa/tree/fddb47d677bf6b2364c1a7bcaba704208432071c): Pixa field names in [`src/chain/serializer.ts`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/chain/serializer.ts#L228-L232).
- **Hive:** [developers.hive.io](https://developers.hive.io/); Hive whitepaper (2020), §II.1 "Assets".
