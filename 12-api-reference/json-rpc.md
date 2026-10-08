# JSON-RPC Surface

> **Status: Live.** Six public nodes running hived 1.30.0, Hivemind at commit `5765e21` and the gateway at commit `4a271e8`. Methods and limits were checked on `api.pixagram.com` on 2026-10-08.

The Pixa chain's API is Hive's JSON-RPC over HTTPS, so Hive's method documentation at [developers.hive.io](https://developers.hive.io/) applies with PIXA for HIVE and PXS for HBD. This page records what the public nodes actually serve: the endpoints, the namespaces and methods, how a call is routed, batches, limits, errors, the field renames, and what is not served. [Differences from Hive](../09-developers/differences-from-hive.md) explains the differences for a programmer; [Developer Quickstart](../09-developers/developer-quickstart.md) shows first calls.

## Endpoints

| Endpoint | Registered by | Notes |
|---|---|---|
| `https://api.pixagram.com` | the operator, Pixa Rex S.A. | The app's default |
| `https://pixarex.net` | the witness `rex` | Did not accept a connection from the network used for the 2026-10-08 check; it did on 2026-10-05 |
| `https://merlion.surf` | the witness `merlion` | |
| `https://blockforge.lol` | the witness `blockforge` | |
| `https://boitata.quest` | the witness `boitata` | |
| `https://pixa-dubai.xyz` | the witness `nodeprime` | |

All six run the same stack ([Architecture](../18-infrastructure/architecture.md)) and serve the same chain; a program may use any and should fall back to another on failure, as the app does ([Account Settings](../14-product/account-settings.md#endpoint)). Each answers `GET /health` with `{"status":"ok"}` from the gateway, which says nothing about whether hived behind it is in sync; for that, compare `head_block_number` from `get_dynamic_global_properties` with the clock.

Every call is an HTTPS `POST` to the root path with a JSON-RPC 2.0 body:

```bash
curl -s https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_dynamic_global_properties","params":[],"id":1}'
```

`GET` requests other than `/health`, and other paths, are not an API.

## Namespaces and methods

The gateway in front of each node routes a call by its method name to one of two programs ([Routing](#routing)). `jsonrpc.get_methods` lists hived's 139 methods; Hivemind has no equivalent call, so its 66 are listed here from its code.

### Served by hived (139 methods)

| Namespace | Methods | What for |
|---|---|---|
| `condenser_api` | 62 | The legacy, array-parameter API most libraries use: accounts, witnesses, blocks, broadcast, conversions, delegations, proposals, market, Resource Credits. 23 further `condenser_api` names are routed to Hivemind (below). |
| `database_api` | 51 | The same state with object parameters and the HF26 operation form: `find_*` by key, `list_*` by index, `get_config`, `get_hardfork_properties`, `verify_authority`, `verify_signatures` |
| `account_history_api` | 4 | `get_account_history`, `get_ops_in_block`, `get_transaction`, `enum_virtual_ops`; irreversible blocks only |
| `block_api` | 3 | `get_block`, `get_block_header`, `get_block_range` |
| `rc_api` | 7 | `find_rc_accounts`, `list_rc_accounts`, `list_rc_direct_delegations`, `get_resource_params`, `get_resource_pool`, `get_rc_stats`, `get_rc_operation_stats` |
| `market_history_api` | 7 | The internal PIXA/PXS market: ticker, volume, order book, trades, buckets |
| `network_broadcast_api` | 1 | `broadcast_transaction` in the HF26 form |
| `account_by_key_api` | 1 | `get_key_references`: which accounts a public key belongs to |
| `reputation_api` | 1 | `get_account_reputations`, computed by hived; the only real reputation figure on the public nodes ([Hivemind differences](#what-hivemind-reports-differently)) |
| `jsonrpc` | 2 | `get_methods`, `get_signature` |

The full list is one call away:

```bash
curl -s https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"jsonrpc.get_methods","params":{},"id":1}'
curl -s https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"jsonrpc.get_signature","params":{"method":"database_api.find_accounts"},"id":1}'
```

### Served by Hivemind (66 methods)

| Namespace | Methods | What for |
|---|---|---|
| `bridge` | 25 | The app's API: `get_ranked_posts`, `get_account_posts`, `get_account_posts_by_tag`, `get_post`, `get_post_header`, `get_discussion`, `normalize_post`, `get_profile`, `get_profiles`, `get_relationship_between_accounts`, `get_follow_list`, `does_user_follow_any_lists`, `account_notifications`, `post_notifications`, `unread_notifications`, `get_community`, `get_community_context`, `list_communities`, `list_pop_communities`, `list_community_roles`, `list_subscribers`, `list_all_subscriptions`, `get_trending_topics`, `get_payout_stats`, `list_muted_reasons_enum` |
| `condenser_api` (23 names routed by the gateway) | 21 working | `get_content`, `get_content_replies`, `get_discussions_by_trending`, `_by_hot`, `_by_created`, `_by_blog`, `_by_feed`, `_by_comments`, `_by_author_before_date`, `get_replies_by_last_update`, `get_post_discussions_by_payout`, `get_comment_discussions_by_payout`, `get_followers`, `get_following`, `get_follow_count`, `get_blog`, `get_blog_entries`, `get_reblogged_by`, `get_active_votes`, `get_trending_tags`, `get_account_reputations`. The other two routed names, `get_discussions_by_promoted` and `get_account_votes`, fail ([What is not served](#what-is-not-served)). |
| `follow_api` | 7 | `get_followers`, `get_following`, `get_follow_count`, `get_blog`, `get_blog_entries`, `get_reblogged_by`, `get_account_reputations` |
| `tags_api` | 11 | `get_discussion`, `get_content_replies` and the `get_discussions_by_*` and `_discussions_by_payout` family |

Hivemind also implements `database_api.find_comments`, `find_votes` and `list_votes`, `hive.get_info`, `hive.db_head_state` and a `search-api.find_text`, but the public nodes' gateway does not route any of them to it ([What is not served](#what-is-not-served)). Its dispatcher also names `condenser_api.get_state` and `get_account_votes`, only to answer that they are not supported.

## Routing

The gateway reads the `method` of each request ([`nginx.conf:18-51, 160-200`][nginx]):

1. The 23 `condenser_api` names above go to Hivemind.
2. Any method whose namespace is `bridge`, `follow_api` or `tags_api` goes to Hivemind.
3. Everything else goes to hived, after the gateway renames 19 Pixa field names in the body to Hive's ([Field renames](#field-renames)).

Two consequences of how it reads the body:

- **Two routed names fail.** `condenser_api.get_discussions_by_promoted` is on the gateway's Hivemind list but this Hivemind has no promoted sort, and `condenser_api.get_account_votes` is routed to Hivemind, which answers that it is no longer supported. `condenser_api.get_state`, which Hive front ends once used, is not on the list and reaches hived, which does not have it either.
- **A body larger than the gateway's buffer, about 10 KiB, is not read.** It goes to hived unrouted and unrenamed. A large `bridge` call therefore fails with `Could not find API bridge`, and a large broadcast keeps the bytes you signed, which is why the rename defect does not affect big artworks ([Differences from Hive](../09-developers/differences-from-hive.md#known-issue-renames-inside-text)).

## Batches

A JSON array of calls is passed through as one request, so it is routed by its **first** call:

| Batch | Result |
|---|---|
| All calls to hived | Works; one array of replies, in order |
| First call to hived, a later one to Hivemind | The Hivemind call fails inside the array with `Could not find API bridge` |
| First call to Hivemind | Hivemind takes one call per request and answers `id required` |

Send social calls one at a time, and batch only chain calls.

## Limits

| | Value on 2026-10-08 | Where it comes from |
|---|---|---|
| Request body | about 1 MiB; above it HTTP 413 | nginx's default `client_max_body_size` in the gateway |
| Time per request | 30 seconds; above it HTTP 504 | `proxy_read_timeout` ([`nginx.conf:200`][nginx]) |
| Results per `bridge` call | `limit` 1 to 20; 21 is rejected | Hivemind's `max_posts_per_call`; the app pages in 20s ([Feed and Discovery](../14-product/feed-and-discovery.md#paging)) |
| `account_history_api.get_account_history` | 1,000 operations per call | hived |
| `block_api.get_block_range` | 1,000 blocks per call | hived |
| `condenser_api.lookup_accounts` and other `lookup_*` | 1,000 names per call | hived |
| Rate limits | none | No limiter is configured; be considerate, the nodes are few |
| Signatures per transaction | 1,000 | hived 1.30.0 ([Transaction Lifecycle](../11-protocol-reference/transaction-lifecycle.md#3-signing)) |

## Headers, compression and CORS

- Send `Content-Type: application/json`. The gateway sets it on the way to the backends regardless.
- Responses are compressed with zstd or gzip when the client's `Accept-Encoding` allows ([`Caddyfile:31`][caddy]).
- `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, POST, OPTIONS`, `Access-Control-Allow-Headers: Content-Type` on every response, and `OPTIONS` answered with 204, so a browser page on any origin may call the API directly, as the app does ([`nginx.conf:205-217`][nginx]). A custom header other than `Content-Type` fails the browser's preflight.
- Because the gateway rewrites bodies, responses have no `Content-Length`; they are chunked.

## Errors

Both programs answer a failed call with a JSON-RPC error object. Their shapes differ:

```json
{"jsonrpc":"2.0","error":{"code":-32003,"message":"Assert Exception:... You may only post once every 5 minutes.","data":{"code":10,"name":"assert_exception","message":"Assert Exception","stack":[...]}},"id":1}
```

| From | `code` | `message` | `data` |
|---|---|---|---|
| hived, a rule or check failed during the call | `-32003` | The assertion text, which is the message quoted on [Operations Reference](../11-protocol-reference/operations-reference.md) and [Transaction Lifecycle](../11-protocol-reference/transaction-lifecycle.md) | an object with `code`, `name`, `message` and a `stack` of frames |
| hived, parameters that do not parse | `-32002` | `Parse Error` | the same shape |
| hived, no `params` member | `-32001` | `A member "params" does not exist` | |
| hived, unknown method or namespace | `-32601` | `Could not find method <name>` or `Could not find API <namespace>` | |
| hived, malformed request | `-32600` | `jsonrpc value is not "2.0"`, `A member "method" does not exist`, or a bad `id` | |
| hived, body that is not JSON | `-32700` | `Parse Error` | |
| hived, busy | `-32003` | `Unable to acquire database lock`, which a client should retry | |
| hived, other server error | `-32000` | `Array is invalid`, `Unknown error - parsing rpc message failed` | |
| Hivemind | `-32602`, `-32601`, `-32000` | `Invalid parameters`, `Method not found`, or the error text | Often a plain string |

Two more differences: hived returns `id` as sent, Hivemind returns it as a string (`"1"` for `1`); and HTTP status is 200 for every JSON-RPC error, so a client must inspect the body. Only the gateway's own failures carry an HTTP status: 413, 504, or 502 when a backend is down.

## Field renames

In responses from hived, the gateway renames 28 Hive field names to Pixa's; in requests to hived, 19 of them the other way ([the table](../09-developers/differences-from-hive.md#field-renames)). Hivemind's responses are not renamed, and neither program's **operation** or **method** names change: `database_api.find_hbd_conversion_requests` keeps its name, `author_reward` keeps `hbd_payout`, and `get_config` prints `HIVE_` constants. The renames apply to the whole body, including text, and only to bodies under about 10 KiB; a program that must see the bytes hived stores reads from its own node.

## What is not served

| Not available | Detail | Instead |
|---|---|---|
| WebSockets or any streaming | The gateway and Caddy serve HTTPS only | Poll: `get_dynamic_global_properties` every 3 seconds for new blocks, `block_api.get_block_range` to catch up |
| `wallet_bridge_api` | Not loaded on the public nodes, so `cli_wallet` cannot connect to them ([CLI Wallet](../10-node-operators/cli-wallet.md)) | Your own node, or a library |
| `transaction_status_api` | Not loaded | `database_api.is_known_transaction`, then `condenser_api.get_transaction` once irreversible ([Transaction Lifecycle](../11-protocol-reference/transaction-lifecycle.md#8-irreversible)) |
| HAF and HAfAH | Installed behind Hivemind but not routed; `account_history_api` is hived's own plugin | hived's `account_history_api` |
| Hivemind's `database_api.find_comments`, `find_votes`, `list_votes`, `hive.*`, `search-api.find_text` | Routed to hived, which does not have them | `bridge.get_post`, `bridge.get_discussion`, `condenser_api.get_active_votes` |
| `condenser_api.get_discussions_by_promoted`, `get_account_votes`, `get_state` | The first has no sort behind it, the second Hivemind refuses as no longer supported, the third reaches hived, which lacks it | `bridge.get_ranked_posts` (there is no promoted sort, [Feed and Discovery](../14-product/feed-and-discovery.md#the-four-sorts)); `account_history_api` for an account's votes |
| A search API | The app's search calls a separate service run by the operator, with no published API ([Search](../14-product/search.md)) | `condenser_api.lookup_accounts`, `bridge.list_communities`, `bridge.get_trending_topics` |
| OpenAPI document | hived ships one in its source; no node serves it | [developers.hive.io](https://developers.hive.io/) and `jsonrpc.get_signature` |
| A test network | None is public | A local node with `--chain-id` of your own ([Run a Node](../10-node-operators/run-a-node.md)) |

## What Hivemind reports differently

Three things a program must know when it reads social data from the public nodes:

- **Reputation is empty.** The tracker that computes it for Hivemind does not run on the public nodes, so `condenser_api.get_account_reputations` as routed to Hivemind returns 0 for every account, and `bridge.get_profile`, `bridge.get_account_posts` and `bridge.get_ranked_posts` return 25, the bottom of Hivemind's display scale, for everyone. hived's `reputation_api.get_account_reputations` has the real figures ([Data Model](../11-protocol-reference/data-model.md#derived-haf-and-hivemind)).
- **Vote `rshares` are a million times the chain's** for votes cast before block 905,693 and equal to the chain's after ([Differences from Hive](../09-developers/differences-from-hive.md#hivemind)).
- **Posts are Hivemind's copies.** hived serves no post text, and the gateway sends `get_content` and `get_active_votes` to Hivemind, although hived could answer the second from its own state ([Data Model](../11-protocol-reference/data-model.md#derived-the-hived-state)).

## Compared with Hive

| | Hive public nodes | Pixa public nodes |
|---|---|---|
| Protocol | JSON-RPC 2.0 over HTTPS; some nodes also WebSockets | HTTPS only |
| Gateway | Jussi (Python), routing by method with caching and per-method limits | an OpenResty configuration: routing and field renames, no cache, no rate limits |
| `bridge` result limit | 100 on most nodes | 20 |
| Hivemind reputation | computed | not computed on the public nodes: 0 or 25 for everyone |
| Account history | HAfAH on most nodes | hived's `account_history_rocksdb` plugin |
| Field names | Hive's | Pixa's through the gateway, Hive's from hived |

## Sources

- **Gateway:** [`jussi/nginx.conf`][nginx] at commit `4a271e8`: Hivemind namespaces and the 23 methods at lines 18-51, request renames 63-85, response renames 87-117, the server block 157-245; [`ssl-proxy/Caddyfile`][caddy].
- **hived** at tag [`v1.30.0`](https://github.com/pixagram-blockchain/pixagram/tree/746118eb3b87dcca768b72fa262ad2aa63e1f177): the plugins an API node loads, [Run an API Node](../10-node-operators/run-an-api-node.md#sources); the shipped OpenAPI document, [`libraries/plugins/apis/documentation/openapi.json`](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/plugins/apis/documentation/openapi.json).
- **Hivemind** at commit [`5765e21`](https://github.com/pixagram-blockchain/hivemind/tree/5765e2113da3c2c3da3c056d7d795c51e925711a): the method dispatcher, [`hive/db/sql_scripts/postgrest/utilities/dispatch.sql`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/db/sql_scripts/postgrest/utilities/dispatch.sql) and [`get_api_method.sql`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/db/sql_scripts/postgrest/utilities/get_api_method.sql); the result limit, [`api_limits.sql`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/db/sql_scripts/postgrest/utilities/api_limits.sql).
- **Live checks**, 2026-10-05 and 2026-10-08, against the six endpoints: `jsonrpc.get_methods` (139), `GET /health`, batches in the three shapes, a 1 MiB and a 1.1 MiB body, `bridge.get_ranked_posts` with `limit` 20 and 21, `OPTIONS` preflight, response headers, `bridge.get_profile` and `reputation_api.get_account_reputations` for the same accounts.

[nginx]: https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/jussi/nginx.conf
[caddy]: https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/ssl-proxy/Caddyfile
