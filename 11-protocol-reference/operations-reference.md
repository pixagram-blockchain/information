# Operations Reference

> **Status: Live.** hived 1.30.0: 50 operations (ids 0 to 49) and 43 virtual operations (50 to 92), the same list as Hive's. Rules unchanged since 1.29.0 cite commit `48f75a2`; rules hardfork 30 changed cite tag `v1.30.0`. Live values were read on 2026-10-08.

Every change to the Pixa chain is one of 50 operations, signed by an account and carried in a transaction ([Transaction Lifecycle](transaction-lifecycle.md)). Where PXS appears below, PXS promises no price: it is a unit the chain converts to PIXA at the witnesses' median feed, and nothing defends its value. This page lists them all: what each does, which key signs it, its fields and limits, what it changes, what it costs in Resource Credits, and where Pixa differs from Hive. It ends with the 43 virtual operations the chain writes itself. Constants are quoted from [Chain Parameters](../21-reference/chain-parameters.md), which wins if they disagree.

## How to read this page

- **Signs with** is the authority an operation needs: **posting** (content and social actions), **active** (anything that moves tokens, votes in governance or changes keys below owner) or **owner** (the owner key itself and recovery). Since Hive's hardfork 28, which Pixa carries from block 1, the level is strict: an active key does not stand in for a posting key ([Transaction Lifecycle](transaction-lifecycle.md#3-signing)).
- **Resources** are the Resource Credit meters an operation runs ([Resource Credits](../04-tokens-and-economy/resource-credits.md)): every transaction pays **H** (history: its size in bytes) and **E** (execution time, including signature checks); some operations add **S** (state the node must keep), **M** (market: the size counted a second time) or **N** (a new account). Costs in credits move every block; the Resource Credits page gives measured figures.
- **Pixa change** says *same as Hive* where only the token names differ. Three Pixa rules apply across operations and are not repeated in every row:
  - `pixa.rex` and `pixa.team` are restricted to transferring VESTS and updating their own keys and metadata; every other operation they sign fails with `This account is restricted to VESTS transfers only.` ([`database.cpp:2762-2792`][restricted], [System Accounts](../21-reference/system-accounts.md#restricted-accounts-pixarex-and-pixateam)).
  - Interest on PXS is 0 and cannot be set otherwise ([`hive_operations.hpp:432`][ops-hpp-432]).
  - `custom`, `custom_json` and `custom_binary` payloads may be 65,536 bytes, eight times Hive's 8,192 ([`config.hpp:484`][cfg-484]).
- Hive's names are kept everywhere: in operation and field names (`hbd_amount` for a PXS amount, `reward_hive` for PIXA), in error texts and in `get_config`. The public nodes' gateway renames some fields on the way in and out ([Differences from Hive](../09-developers/differences-from-hive.md#field-renames)).

## The 50 operations

| Id | Operation | Signs with | Does | Pixa change |
|---|---|---|---|---|
| 0 | `vote` | posting | Votes on a post or comment with a weight from -100% to 100% | Dust threshold 50,000 rshares since HF30 |
| 1 | `comment` | posting | Publishes or edits a post, an artwork or a comment | Payload size: see [Transaction Lifecycle](transaction-lifecycle.md#1-construction) |
| 2 | `transfer` | active | Sends PIXA or PXS with an optional memo | May carry VESTS from `pixa.rex` and `pixa.team` |
| 3 | `transfer_to_vesting` | active | Powers up PIXA into Pixa Power, for oneself or another account | same as Hive |
| 4 | `withdraw_vesting` | active | Starts, changes or cancels a power-down | same |
| 5 | `limit_order_create` | active | Places an order on the internal PIXA/PXS market | same; unused by the app |
| 6 | `limit_order_cancel` | active | Cancels an order | same |
| 7 | `feed_publish` | active | A witness publishes its PIXA price of one PXS | The feed states a Big Mac, not a dollar |
| 8 | `convert` | active | Converts PXS into PIXA after 3.5 days | same |
| 9 | `account_create` | active | Opens an account for a fee | same |
| 10 | `account_update` | owner or active | Changes keys, the memo key or `json_metadata` | same |
| 11 | `witness_update` | active | Registers or updates a witness | same |
| 12 | `account_witness_vote` | active | Approves or withdraws approval of a witness | same |
| 13 | `account_witness_proxy` | active | Names an account to vote in one's place | same |
| 14 | `pow` | — | Mining; disabled since Steem's hardfork 13 | same |
| 15 | `custom` | active | Carries binary data for applications | 64 KiB; priced by size since HF30 |
| 16 | `witness_block_approve` | witness | Never valid in a block | same |
| 17 | `delete_comment` | posting | Removes a post or comment that has no replies and no positive votes | same |
| 18 | `custom_json` | active or posting | Carries JSON for applications: follows, reblogs, communities, credit delegation | 64 KiB; priced by size since HF30 |
| 19 | `comment_options` | posting | Sets a post's payout options and beneficiaries | same |
| 20 | `set_withdraw_vesting_route` | active | Routes part of a power-down to another account | same |
| 21 | `limit_order_create2` | active | Places an order with an exchange rate | same; unused by the app |
| 22 | `claim_account` | active | Buys an account ticket with the fee or with credits | same |
| 23 | `create_claimed_account` | active | Opens an account with a ticket | same |
| 24 | `request_account_recovery` | active, of the recovery partner | Starts a recovery | Owner history recorded from HF30 |
| 25 | `recover_account` | the new and a recent owner authority | Completes a recovery | Owner history recorded from HF30 |
| 26 | `change_recovery_account` | owner | Names a new recovery partner, effective after 30 days | same |
| 27 | `escrow_transfer` | active | Puts PIXA or PXS in escrow with an agent | same |
| 28 | `escrow_dispute` | active | Raises a dispute | same |
| 29 | `escrow_release` | active | Releases escrowed funds | same |
| 30 | `pow2` | — | Mining; disabled since Steem's hardfork 17 | same |
| 31 | `escrow_approve` | active | Approves or rejects an escrow | same |
| 32 | `transfer_to_savings` | active | Moves PIXA or PXS into savings | same |
| 33 | `transfer_from_savings` | active | Withdraws from savings after 3 days | same |
| 34 | `cancel_transfer_from_savings` | active | Cancels a pending withdrawal | same |
| 35 | `custom_binary` | — | Disabled | same |
| 36 | `decline_voting_rights` | owner | Gives up voting for ever, after 30 days | same |
| 37 | `reset_account` | — | Placeholder; always invalid | same |
| 38 | `set_reset_account` | — | Placeholder; always invalid | same |
| 39 | `claim_reward_balance` | posting | Moves pending rewards into the balances | same |
| 40 | `delegate_vesting_shares` | active | Lends Pixa Power to another account | same |
| 41 | `account_create_with_delegation` | active | Disabled since Steem's hardfork 20 | same |
| 42 | `witness_set_properties` | the witness signing key | Updates a witness's properties one at a time | Interest must stay 0 |
| 43 | `account_update2` | owner, active or posting | Changes keys or metadata; the posting level can change `posting_json_metadata` alone | same |
| 44 | `create_proposal` | active | Proposes a daily payment from the DPF | Paid to the treasury `pixa.omnibus` in PXS |
| 45 | `update_proposal_votes` | active | Approves or withdraws approval of proposals | same |
| 46 | `remove_proposal` | active | Removes one's own proposals | same |
| 47 | `update_proposal` | active | Lowers a proposal's pay or shortens it | same |
| 48 | `collateralized_convert` | active | Converts PIXA into PXS at once, against collateral | same |
| 49 | `recurrent_transfer` | active | Sets up, changes or cancels a repeating transfer | same |

Operation ids are the position in this list; the binary serialization writes the id before each operation ([Transaction Lifecycle](transaction-lifecycle.md#2-serialization)).

## Content and voting

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `vote` (0) | `voter`, `author`, `permlink`, `weight` (-10000 to 10000, in hundredths of a percent) | The voter has not declined voting rights. The post is not paid out; a vote on a paid-out post is accepted and does nothing ([`ev_soc:624-627`][vote-paid]). A new vote cannot have weight 0, and a changed vote must differ from the current one ([`ev_soc:642-647`][vote-rules]). The vote spends voting mana: `ceil(E × |weight| × 86,400 / 10,000 / 4,320,000)`, where E is the voter's effective Pixa Power in VESTS; a full vote spends 2% of the bar ([`ev_soc:660-706`][vote-mana]). **Since HF30** the rshares are the mana spent less 50,000; before, less 50,000,000, which silenced every account below 2,500 Pixa Power ([`ev_soc:710`][vote-dust]). In the last 12 hours before payout the rshares shrink in proportion to the time left ([`ev_soc:713-718`][vote-dust]). | Adds the rshares to the post's `net_rshares`; records the vote with its curation weight, which depends on the post's rshares before it and on the vote's age: full in the first 24 hours, halved to 72 hours, an eighth after ([`ev_soc:784-831`][vote-weight]; [Voting and Curation](../02-social-layer/voting-and-curation.md)). Emits `effective_comment_vote`. | H, E, S (the vote, kept until payout) |
| `comment` (1) | `parent_author` (empty for a post), `parent_permlink` (the category for a post; the parent's permlink for a comment), `author`, `permlink`, `title`, `body`, `json_metadata` | Title under 256 bytes; body not empty; both UTF-8 ([`ops.cpp:123-138`][comment-val]). Permlink up to 256 characters from `a-z`, `0-9` and `-` ([`ev_soc:36-48`][permlink]). `json_metadata` empty or valid JSON. One post every 5 minutes, one comment every 3 seconds, one edit per author per block ([`ev_soc:214-216, 284`][comment-rate]). Comments at most 255 deep ([`ev_soc:189-193`][comment-depth]). An edit may change everything except the parent, and is allowed after payout ([`ev_soc:296-306`][comment-edit]). The whole operation must fit the transaction size, about 2 MiB. | Creates the post in the state with a payout 7 days ahead, or edits it. After payout the text moves to the comment archive ([Data Model](data-model.md#derived-the-hived-state)). | H, E, S (the post object and its permlink, until payout) |
| `delete_comment` (17) | `author`, `permlink` | No replies; not paid out; `net_rshares` not positive ([`ev_soc:56-70`][delete]). | Removes the post and its votes from the state; a delete on a post with positive rshares is rejected (`Cannot delete a comment with net positive votes.`). The block log keeps every version of every post regardless ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)). | H, E |
| `comment_options` (19) | `author`, `permlink`, `max_accepted_payout` (PXS; default 1,000,000.000), `percent_hbd` (default 10000), `allow_votes`, `allow_curation_rewards`, `extensions` (beneficiaries) | Not after payout. `max_accepted_payout` and `percent_hbd` can only go down, and votes and curation rewards cannot be re-enabled ([`ev_soc:150-162`][options]). Beneficiaries: 1 to 8 accounts in ascending order, weights summing to at most 100%, only before any vote and only once ([`ops.cpp:150-175`][benef-val], [`ev_soc:118-131`][benef]). | Fixes how the payout is split ([Posting and Rewards](../02-social-layer/posting-and-rewards.md)). | H, E, S (beneficiaries) |
| `claim_reward_balance` (39) | `account`, `reward_hive`, `reward_hbd`, `reward_vests` | At least one amount positive; none above the pending balance ([`ev_tr:691-712`][claim]). The gateway accepts `reward_pixa` and `reward_pxs`. | Moves the amounts from the reward balances to the account's balances. | H, E |

**Why posts are not operations of their own.** Hive has no `post` operation: a post is a `comment` with an empty `parent_author`. An artwork is a post whose body holds the image ([Artwork Encoding Spec](../09-developers/artwork-encoding-spec.md)).

## Custom data

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `custom` (15) | `required_auths`, `id` (16-bit), `data` (bytes) | 1 to 40 accounts, each signing with the active key; `data` up to 65,536 bytes ([`ops.cpp:407-414`][custom-val], [`ev:350-358`][custom-ev]). | None on the chain's state. Indexers may read it. | H, E (**since HF30**, grows with the payload: the base cost times `1 + bytes / 8,192` [`resource_count.cpp:434-441`][rc-custom]) |
| `custom_json` (18) | `required_auths`, `required_posting_auths`, `id` (up to 32 characters), `json` | 1 to 40 accounts in all; accounts in `required_auths` sign with the active key, those in `required_posting_auths` with the posting key ([`ops.cpp:416-429`][cjson-val]). `json` valid JSON, up to 65,536 bytes; from 1.30.0 the length is checked before the JSON is parsed ([`ops.cpp:425-430` at v1.30.0][cjson-130]). At most 5 custom operations per account in a node's pending list at a time ([Transaction Lifecycle](transaction-lifecycle.md#5-the-nodes-checks)). | None on the chain's state, with one exception the chain reads itself: `id` `rc` with `delegate_rc` lends Resource Credits ([Resource Credits](../04-tokens-and-economy/resource-credits.md#how-credits-are-counted)). Hivemind reads `follow`, `reblog`, `community` and `notify` ([Feed and Discovery](../14-product/feed-and-discovery.md#following)). | H, E (**since HF30** grows with the payload, as for `custom`) |
| `custom_binary` (35) | `required_owner_auths`, `required_active_auths`, `required_posting_auths`, `required_auths`, `id`, `data` | Always rejected: `Operation disallowed.` ([`ev:403-412`][cbin]). | None. | — |

## Transfers, savings and escrow

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `transfer` (2) | `from`, `to`, `amount`, `memo` | Amount positive, in PIXA or PXS; memo up to 2,047 bytes of UTF-8, and public ([`ops.cpp:241-249`][transfer-val]). To the treasury `pixa.omnibus` only PXS or PIXA, and PIXA sent there is converted to PXS at the median at once ([`ev_tr:261-290, 345`][transfer-ev]). **Pixa:** `pixa.rex` and `pixa.team` may transfer VESTS, which Hive forbids; the stake must not be delegated, powering down or still maturing ([`ev_tr:291-343`][transfer-vests]). | Moves the balance. A VESTS transfer moves stake directly, with no power-down. PIXA into the treasury emits `dhf_conversion`. | H, E, M |
| `transfer_to_savings` (32) | `from`, `to`, `amount`, `memo` | PIXA or PXS; not to the treasury ([`ev_tr:644-655`][savings]). | Moves the amount into `to`'s savings. | H, E |
| `transfer_from_savings` (33) | `from`, `request_id`, `to`, `amount`, `memo` | At most 100 pending withdrawals per account; the balance must cover it ([`ev_tr:657-676`][savings]). | Schedules the payment for 3 days later; `fill_transfer_from_savings` when it is paid. | H, E, S (the request) |
| `cancel_transfer_from_savings` (34) | `from`, `request_id` | The request exists. | Returns the amount to savings. | H, E |
| `recurrent_transfer` (49) | `from`, `to`, `amount`, `memo`, `recurrence` (hours), `executions`, `extensions` (optional `pair_id`) | Every 24 hours or more; at least 2 executions; the whole schedule within 730 days; at most 255 open per sender; the first payment needs the balance now ([`ops.cpp:802-820`][recur-val], [`ev_tr:982-1035`][recur-ev]). Amount 0 cancels an existing one. | Pays at once, then on schedule: `fill_recurrent_transfer` for each payment, `failed_recurrent_transfer` when the balance is short; after 10 consecutive failures the transfer is removed ([`config.hpp:245`][cfg-245]). | H, E, M, S (for the schedule's lifetime) |
| `escrow_transfer` (27) | `from`, `to`, `agent`, `escrow_id`, `hbd_amount`, `hive_amount`, `fee`, `ratification_deadline`, `escrow_expiration`, `json_meta` | A positive amount; the agent is neither party; the deadline before the expiration and both in the future; at most 255 open escrows per sender ([`ops.cpp:659-679`][escrow-val], [`ev_tr:76-107`][escrow-ev]). | Locks the funds and the fee. | H, E, S |
| `escrow_approve` (31) | `from`, `to`, `agent`, `who`, `escrow_id`, `approve` | `who` is `to` or the agent, before the deadline. A rejection, or a missed deadline, returns everything ([`ev_tr:109-176`][escrow-ev]). | When both have approved, the agent receives the fee: `escrow_approved`. Otherwise `escrow_rejected`. | H, E |
| `escrow_dispute` (28) | `from`, `to`, `agent`, `who`, `escrow_id` | By `from` or `to`, after approval, before expiration ([`ev_tr:178-197`][escrow-ev]). | Only the agent may release from then on. | H, E |
| `escrow_release` (29) | `from`, `to`, `agent`, `who`, `receiver`, `escrow_id`, `hbd_amount`, `hive_amount` | Before a dispute: `from` may release to `to`, `to` may release to `from`; after expiration, either may release to either; under dispute, only the agent ([`ev_tr:199-259`][escrow-ev]). | Pays the receiver. | H, E |

## Staking

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `transfer_to_vesting` (3) | `from`, `to` (empty means `from`), `amount` in PIXA | Positive; not to the treasury ([`ev_tr:352-388`][vest]). | Converts at the current VESTS price, about 1 to 1 on Pixa ([Pixa Power](../04-tokens-and-economy/pixa-power.md)). Emits `transfer_to_vesting_completed`; the stake votes in governance after 30 days (`delayed_voting`). | H, E, M, S |
| `withdraw_vesting` (4) | `account`, `vesting_shares` | At most the account's own stake not delegated; 0 cancels; a new amount must change the rate ([`ev_tr:390-455`][powerdown]). | Pays the amount back as PIXA in 13 weekly instalments, each `fill_vesting_withdraw`. | H, E |
| `set_withdraw_vesting_route` (20) | `from_account`, `to_account`, `percent`, `auto_vest` | Up to 10 routes, summing to at most 100%; not to the treasury ([`ev_tr:457-521`][route]). | Sends that share of each instalment to `to_account`, as PIXA or, with `auto_vest`, as Pixa Power. | H, E, S |
| `delegate_vesting_shares` (40) | `delegator`, `delegatee`, `vesting_shares` | Not to oneself. At least the account creation fee ÷ 3 in VESTS, about 6.67 Pixa Power at the live fee; a change of at least the fee ÷ 30; only stake not already delegated, not powering down and covered by the delegator's current voting and downvoting mana ([`ev_tr:750-930`][delegate]). 0 removes the delegation. | The delegatee's effective stake rises at once; removed or reduced stake returns to the delegator after 5 days with `return_vesting_delegation` ([Delegation](../04-tokens-and-economy/pixa-power.md#delegation)). | H, E, S |

## PXS and the internal market

PXS promises no price. These operations move between PIXA and PXS at the witnesses' median feed, reduced by the haircut when collateral is thin ([Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md)).

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `convert` (8) | `owner`, `requestid`, `amount` in PXS | A positive PXS amount; the id unused by this account ([`ev_tr:523-537`][convert]). Cannot be cancelled. | PXS leaves the balance at once; 3.5 days later `fill_convert_request` pays PIXA at the median of that moment. | H, E, S |
| `collateralized_convert` (48) | `owner`, `requestid`, `amount` in PIXA | PXS printing must be on (`pxs_print_rate` above 0) and the new PXS within the stop limit ([`ev_tr:539-586`][cconvert]). Cannot be cancelled. | Locks the PIXA as collateral and issues PXS at once: `collateralized_convert_immediate_conversion`. 3.5 days later `fill_collateralized_convert_request` settles at the market median plus the 5% fee and returns the rest of the collateral; a shortfall is logged as `system_warning` and the collateral is kept. | H, E, S |
| `limit_order_create` (5) | `owner`, `orderid`, `amount_to_sell`, `min_to_receive`, `fill_or_kill`, `expiration` | One side PIXA and the other PXS; expiration within 28 days; `fill_or_kill` fails if not filled at once ([`ops.cpp:596-614`][order-val], [`ev_tr:588-613`][order-ev]). | Trades against the book: `fill_order` for each match; the rest stays until filled, cancelled or expired (`limit_order_cancelled`). | H, E, M, S |
| `limit_order_create2` (21) | `owner`, `orderid`, `amount_to_sell`, `exchange_rate`, `fill_or_kill`, `expiration` | The same, with a price instead of a minimum. | The same. | H, E, M, S |
| `limit_order_cancel` (6) | `owner`, `orderid` | The order exists. | Returns the unsold amount; `limit_order_cancelled`. | H, E |

The internal market exists because Hive's does. The app does not use it, and `market_history_api` showed no trades on 2026-10-08.

## Accounts and keys

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `account_create` (9) | `fee`, `creator`, `new_account_name`, `owner`, `active`, `posting`, `memo_key`, `json_metadata` | Name 3 to 16 characters in Hive's format. Each authority up to 40 keys and accounts ([`ops.cpp:45-66`][create-val]). The fee must equal the median account creation fee exactly, 20.000 PIXA on 2026-10-08 (`condenser_api.get_chain_properties`), and the creator pays it ([`ev_acc:156-208`][create-ev]). | Creates the account with no stake; the fee is sent to `null` and burned. Emits `account_created`. | H, E, S (the account and its keys) |
| `claim_account` (22) | `creator`, `fee`, `extensions` (empty) | Either the exact median fee, burned, or a fee of 0, which takes a ticket from the subsidy pool and is charged in credits; a ticket can be claimed only in a block whose producer has subsidy left ([`ev_acc:402-462`][claim-acc]). | Adds one to the creator's `pending_claimed_accounts`. | H, E, N (with fee 0) |
| `create_claimed_account` (23) | `creator`, `new_account_name`, `owner`, `active`, `posting`, `memo_key`, `json_metadata`, `extensions` (empty) | The creator holds a ticket ([`ev_acc:464-497`][claim-create]). | Creates the account and spends the ticket. Emits `account_created`. | H, E, S |
| `account_update` (10) | `account`, `owner`, `active`, `posting`, `memo_key`, `json_metadata` | Owner changes need the owner key and are allowed twice an hour ([`ev_acc:286-358`][update]). A new authority may not reference an account that does not exist. | Replaces the authorities given; records the previous owner authority in the owner history (see recovery). | H, E, S (new authorities) |
| `account_update2` (43) | as above, plus `posting_json_metadata` | The level depends on what changes: owner for `owner`; active for `active`, `posting`, `memo_key` or `json_metadata`; posting when only `posting_json_metadata` changes ([`hive_operations.hpp:74-110`][update2-hpp]). The app writes profiles this way ([Account Settings](../14-product/account-settings.md#your-profile)). | As `account_update`; `posting_json_metadata` is stored separately. | H, E, S |
| `change_recovery_account` (26) | `account_to_recover`, `new_recovery_account`, `extensions` | The new partner must exist. | Takes effect 30 days later: `changed_recovery_account` ([`ev_acc:589-615`][change-rec]). | H, E, S |
| `request_account_recovery` (24) | `recovery_account`, `account_to_recover`, `new_owner_authority`, `extensions` | Signed by the account's recovery partner; the new authority must be usable and not open ([`ev_acc:499-552`][req-rec]). | Opens a request that expires after 1 day. | H, E, S |
| `recover_account` (25) | `account_to_recover`, `new_owner_authority`, `recent_owner_authority`, `extensions` | Signed by both authorities; the new one matches the request; the recent one appears in the account's owner history ([`ev_acc:554-587`][rec-acc]). **Pixa:** the chain records owner history from hardfork 30, 2026-10-07 12:00 UTC; an owner change made before then cannot serve as the recent authority ([`database.cpp:1733`][owner-hist]; [Keys and Recovery](../08-guides/keys-and-recovery.md)). Once an hour per account. | Sets the new owner authority. | H, E, S |
| `decline_voting_rights` (36) | `account`, `decline` | One request at a time; `decline: false` cancels it before it takes effect ([`ev_acc:617-643`][decline]). | After 30 days the account can never vote again: `declined_voting_rights`, and `proxy_cleared` if it had a proxy. | H, E, S |

## Witnesses and feeds

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `witness_update` (11) | `owner`, `url`, `block_signing_key`, `props` (`account_creation_fee`, `maximum_block_size`, `hbd_interest_rate`), `fee` | URL 1 to 2,048 bytes; block size between 128 KiB and 2 MiB; interest 0 ([`ops.cpp:276-285`][wit-val], [`ev:71-120`][wit-ev]). The fee field is ignored. | Registers the account as a witness, or updates its key, URL and the parameters it votes for ([Become a Witness](../10-node-operators/become-a-witness.md)). | H, E, S |
| `witness_set_properties` (42) | `owner`, `props` (a map; `key` required), `extensions` | `key` must be the witness's current signing key, and the transaction is signed with it. Properties: `account_creation_fee`, `maximum_block_size`, `hbd_interest_rate` (must be 0), `account_subsidy_budget`, `account_subsidy_decay`, `new_signing_key`, `hbd_exchange_rate`, `url` ([`ops.cpp:287-391`][wsp-val], [`ev:122-226`][wsp-ev]). | Updates the properties given, including the price feed. Values are serialized, so libraries must encode them ([SDKs and Libraries](../09-developers/sdks-and-libraries.md)). | H, E |
| `feed_publish` (7) | `publisher`, `exchange_rate` (`base` in PXS, `quote` in PIXA) | The publisher is a witness; the price has PXS as base and PIXA as quote, for example `{"base":"1.000 PXS","quote":"51.833 PIXA"}` ([`ev:638-653`][feed-ev]). | Sets the witness's feed and its time; the chain takes the median of the scheduled witnesses' feeds every hour ([Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md)). | H, E |
| `account_witness_vote` (12) | `account`, `witness`, `approve` | At most 30 witnesses; not while a proxy is set; the account can vote ([`ev:284-348`][wvote]). | Adds or removes the account's full governance weight for that witness ([Witnesses and DPoS](../07-governance/witnesses-and-dpos.md#how-witnesses-are-elected)). | H, E, S |
| `account_witness_proxy` (13) | `account`, `proxy` (empty removes it) | Not oneself; no loops; at most 4 levels; must change ([`ev:228-282`][proxy]). | The proxy votes with the account's weight for witnesses and proposals; the account's own witness votes are cleared. | H, E |

## The Decentralized Pixa Fund

| Operation | Fields | Rules and limits | Effects | Resources |
|---|---|---|---|---|
| `create_proposal` (44) | `creator`, `receiver`, `start_date`, `end_date`, `daily_pay` in PXS, `subject`, `permlink`, `extensions` | Subject up to 80 bytes; the permlink names a post by the creator or the receiver; the end date in the future. Fee 10.000 PXS, plus 1.000 PXS for each day beyond 60, paid to the treasury ([`dhf:32-100`][prop-create]). | Creates the proposal; `proposal_fee`. Approved proposals are paid hourly while the fund lasts ([Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md)). | H, E, S (for the proposal's lifetime) |
| `update_proposal` (47) | `proposal_id`, `creator`, `daily_pay`, `subject`, `permlink`, `extensions` (optional new `end_date`) | Only the creator; pay can only go down and the end date only earlier ([`dhf:103-153`][prop-update]). | Changes the proposal. | H, E |
| `update_proposal_votes` (45) | `voter`, `proposal_ids` (up to 5), `approve`, `extensions` | The voter can vote; the proposals exist and have not ended ([`dhf:155-211`][prop-vote]). | Adds or removes the voter's full weight on each proposal. | H, E, S |
| `remove_proposal` (46) | `proposal_owner`, `proposal_ids` (up to 5), `extensions` | Only one's own proposals. | Removes them and their votes. | H, E |

## Disabled or unusable

| Operation | State | Source |
|---|---|---|
| `pow` (14), `pow2` (30) | Mining ended with Steem's hardforks 13 and 17, both applied at Pixa's block 1 | [`ev:535-545`][pow] |
| `witness_block_approve` (16) | Rejected from blocks: `Operation excluded from blocks.` | [`ev:656-661`][wba] |
| `custom_binary` (35) | Rejected: `Operation disallowed.` | [`ev:403-412`][cbin] |
| `reset_account` (37), `set_reset_account` (38) | Placeholders whose `validate()` always fails | [`ops.cpp:769-777`][reset] |
| `account_create_with_delegation` (41) | Rejected since Steem's hardfork 20 | [`ev_acc:210-213`][acwd] |

## Virtual operations

The chain writes these itself when a rule applies. They have no signature and carry no authority; `account_history_api` and `condenser_api.get_ops_in_block` with `only_virtual` return them ([Transaction Lifecycle](transaction-lifecycle.md#7-applied-in-a-block)).

| Id | Virtual operation | Written when |
|---|---|---|
| 50 | `fill_convert_request` | A `convert` settles, 3.5 days after it was sent |
| 51 | `author_reward` | A post pays out: the author's PXS, PIXA and Pixa Power |
| 52 | `curation_reward` | A post pays out: one per curator, in Pixa Power |
| 53 | `comment_reward` | A post pays out: the totals |
| 54 | `liquidity_reward` | Never since Steem's hardfork 12 |
| 55 | `interest` | Hive pays interest on HBD held in savings; Pixa never does, its rate being fixed at 0 |
| 56 | `fill_vesting_withdraw` | A weekly power-down instalment is paid |
| 57 | `fill_order` | Two orders match on the internal market |
| 58 | `shutdown_witness` | An event in witness scheduling, not described here |
| 59 | `fill_transfer_from_savings` | A savings withdrawal completes |
| 60 | `hardfork` | A hardfork applies: block 402,205 for HF29, block 949,330 for HF30 |
| 61 | `comment_payout_update` | A post's payout state changes |
| 62 | `return_vesting_delegation` | Removed delegated stake returns to the delegator after 5 days |
| 63 | `comment_benefactor_reward` | A post pays out: one per beneficiary |
| 64 | `producer_reward` | Every block, to its producer |
| 65 | `clear_null_account_balance` | Balances sent to `null` are burned |
| 66 | `proposal_pay` | A proposal receives its hourly payment |
| 67 | `dhf_funding` | Every hour, at maintenance: the treasury's share of issuance accumulated since the last one, in PXS; the per-block share is exact since HF30 ([`dhf_funding.hpp`][dhf-funding], [`dhf_processor.cpp:326-338`][dhf-vop]) |
| 68 | `hardfork_hive` | Hive's 2020 split; never on Pixa |
| 69 | `hardfork_hive_restore` | Hive's 2020 split; never on Pixa |
| 70 | `delayed_voting` | Powered-up stake matures and gains governance weight, 30 days after the power-up |
| 71 | `consolidate_treasury_balance` | The treasury's balances are consolidated at maintenance |
| 72 | `effective_comment_vote` | Every vote: its rshares, weight and the post's totals |
| 73 | `ineffective_delete_comment` | Never on Pixa: it recorded a delete that could not take effect before Steem's hardfork 19, and since then such a delete is rejected instead ([`ev_soc:69-76`][delete-ineff]) |
| 74 | `dhf_conversion` | PIXA the treasury holds or receives is converted to PXS |
| 75 | `expired_account_notification` | An account's governance votes expire after 365 days without a governance action |
| 76 | `changed_recovery_account` | A recovery partner change takes effect, 30 days after the request |
| 77 | `transfer_to_vesting_completed` | A power-up completes, with the VESTS received |
| 78 | `pow_reward` | Mining; never on Pixa |
| 79 | `vesting_shares_split` | Steem's 2016 split; never on Pixa |
| 80 | `account_created` | An account is created |
| 81 | `fill_collateralized_convert_request` | A `collateralized_convert` settles and returns the excess collateral |
| 82 | `system_warning` | The chain corrects something and says so: a conversion short of collateral, a median price corrected by the hard limit, and conditions in witness scheduling |
| 83 | `fill_recurrent_transfer` | A recurring payment is made |
| 84 | `failed_recurrent_transfer` | A recurring payment fails for lack of funds |
| 85 | `limit_order_cancelled` | An order is cancelled or expires |
| 86 | `producer_missed` | A scheduled witness did not produce its block |
| 87 | `proposal_fee` | A proposal is created |
| 88 | `collateralized_convert_immediate_conversion` | A `collateralized_convert` issues PXS at once |
| 89 | `escrow_approved` | Both parties approved an escrow; the agent is paid |
| 90 | `escrow_rejected` | An escrow was rejected or its deadline passed |
| 91 | `proxy_cleared` | A proxy is removed by the chain, at vote expiry or when voting rights are declined |
| 92 | `declined_voting_rights` | A decline takes effect |

## Compared with Hive

| | Hive | Pixa |
|---|---|---|
| Operation list | 50 operations, 43 virtual | identical |
| Custom payloads | 8,192 bytes, flat cost | 65,536 bytes; cost grows with size since HF30 |
| Vote dust threshold | 50,000,000 rshares, about 1.6 Hive Power | 50,000 rshares since HF30, 2.5 Pixa Power; before HF30 the same 50,000,000, 2,500 Pixa Power |
| VESTS in `transfer` | never | from `pixa.rex` and `pixa.team` only |
| Interest on HBD / PXS | witnesses vote the rate | fixed at 0 |
| Treasury | `hive.fund`, paid in HBD | `pixa.omnibus`, paid in PXS |
| Owner authority history | since block 3,186,477 of the Steem chain (2016) | from hardfork 30, block 949,330 |

## Sources

- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443) unless marked v1.30.0. Abbreviations: `ops.cpp` = `libraries/protocol/hive_operations.cpp`; `ev` = `libraries/chain/hive_evaluator.cpp`; `ev_acc`, `ev_soc`, `ev_tr` = `hive_evaluator_account.cpp`, `hive_evaluator_social.cpp`, `hive_evaluator_transfer.cpp`; `dhf` = `dhf_evaluator.cpp`. The operation list: [`operations.hpp:21-129`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/operations.hpp#L21-L129). Resource counting: [`resource_count.cpp:198-560` at v1.30.0](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/rc/resource_count.cpp#L198-L560).
- **Hardfork 30:** [Protocol Upgrades](../07-governance/protocol-upgrades.md#hardfork-30) and [`1_30.hf`](https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/hardfork.d/1_30.hf).
- **Live chain**, 2026-10-08: `condenser_api.get_chain_properties` (fee 20.000 PIXA), `condenser_api.get_dynamic_global_properties`, `market_history_api.get_recent_trades`, and the `effective_comment_vote` of a 50-VESTS account's vote after HF30 (950,000 rshares).
- [Hive developer portal](https://developers.hive.io/): "Broadcast Ops" and "Virtual Ops".

[restricted]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2762-L2792
[ops-hpp-432]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/hive_operations.hpp#L432
[cfg-484]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/include/hive/protocol/config.hpp#L484
[cfg-245]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/include/hive/protocol/config.hpp#L245
[vote-paid]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L624-L627
[vote-rules]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L642-L647
[vote-mana]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L660-L706
[vote-dust]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/hive_evaluator_social.cpp#L708-L718
[vote-weight]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L784-L831
[comment-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L123-L138
[permlink]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L36-L48
[comment-rate]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L214-L216
[comment-depth]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L189-L193
[comment-edit]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L296-L306
[delete]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L56-L70
[delete-ineff]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L69-L76
[dhf-vop]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/util/dhf_processor.cpp#L326-L338
[options]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L150-L162
[benef-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L150-L175
[benef]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L118-L131
[claim]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L691-L712
[custom-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L407-L414
[custom-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L350-L358
[rc-custom]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/rc/resource_count.cpp#L434-L449
[cjson-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L416-L429
[cjson-130]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/protocol/hive_operations.cpp#L425-L434
[cbin]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L403-L412
[transfer-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L241-L249
[transfer-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L261-L350
[transfer-vests]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L291-L343
[savings]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L644-L689
[recur-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L802-L820
[recur-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L982-L1035
[escrow-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L659-L713
[escrow-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L76-L259
[vest]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L352-L388
[powerdown]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L390-L455
[route]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L457-L521
[delegate]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L750-L930
[convert]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L523-L537
[cconvert]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L539-L586
[order-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L596-L640
[order-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L588-L642
[create-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L45-L66
[create-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L156-L208
[claim-acc]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L402-L462
[claim-create]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L464-L497
[update]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L286-L358
[update2-hpp]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/hive_operations.hpp#L74-L110
[change-rec]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L589-L615
[req-rec]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L499-L552
[rec-acc]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L554-L587
[owner-hist]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/database.cpp#L1733
[decline]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L617-L643
[wit-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L276-L285
[wit-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L71-L120
[wsp-val]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L287-L391
[wsp-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L122-L226
[feed-ev]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L638-L653
[wvote]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L284-L348
[proxy]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L228-L282
[prop-create]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/dhf_evaluator.cpp#L32-L100
[prop-update]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/dhf_evaluator.cpp#L103-L153
[prop-vote]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/dhf_evaluator.cpp#L155-L211
[pow]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L535-L545
[wba]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator.cpp#L656-L661
[reset]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L769-L777
[acwd]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L210-L213
[dhf-funding]: https://github.com/pixagram-blockchain/pixagram/blob/746118eb3b87dcca768b72fa262ad2aa63e1f177/libraries/chain/include/hive/chain/util/dhf_funding.hpp
