# Chain Parameters

> **Status: Live.** This page describes hived 1.29.0 (hardfork 29, active since block 402,205 on 2026-09-18). Last checked against the code and the live chain on 2026-10-05, at block 893,370.

This page is the reference for every protocol number in these pages. Other pages may quote a number when it helps the reader, but they link here, and this page wins if the two disagree. When the chain changes, it is corrected here first.

Each row gives the value in upstream Hive, the value on the Pixa chain, the kind of number it is, and its source. **Bold** marks a Pixa value that differs from Hive. Numbered notes follow each table.

| Kind | Meaning | How it changes |
|---|---|---|
| Consensus | Compiled into `hived`; every node enforces it. | Only by a hardfork. |
| Witness median | Each witness publishes a value; the chain uses the median across the scheduled witnesses. | When witnesses publish new values. |
| Genesis | Set once, at block 0. | Never. |
| State | Computed by the chain as it runs. | Continuously. Read it live with the calls in [Reading live values](#reading-live-values). |
| Software | A setting of a node, a service or an app. Consensus does not enforce it. | When that software's operator changes it. |

The Pixa code is cited at commit [`48f75a2`][pixa-commit] of `pixagram-blockchain/pixagram`. Paths are relative to `libraries/`, and `config.hpp` means `protocol/include/hive/protocol/config.hpp`. Hive values come from hived 1.28.7, the release Pixa is built on ([upstream `config.hpp`][hive-config]), or from the live Hive chain where marked. The live Pixa nodes report revision `c9f032d`, which differs from `48f75a2` only in comments and tests.

## Network identity

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Chain ID | `beeab0de…` | **`70697861…`** ¹ | Consensus | [config.hpp:145][cfg-145] |
| Public-key prefix | `STM` | **`PIX`** | Consensus | [config.hpp:215][cfg-215] |
| Liquid token | HIVE | **PIXA** | Consensus | [asset_symbol.hpp:44-45][sym-44] |
| Second token | HBD | **PXS** ² | Consensus | [asset_symbol.hpp:44-45][sym-44] |
| Staked unit | VESTS | VESTS ³ | Consensus | [asset_symbol.hpp:20-28][sym-20] |
| Asset ids (NAI) and decimals | `@@000000021` (3) · `@@000000013` (3) · `@@000000037` (6) | same | Consensus | [asset_symbol.hpp:20-28][sym-20] |
| Legacy symbol bytes | `STEEM` · `SBD` | **`PIXA` · `PXS`** ⁴ | Consensus | [asset_symbol.hpp:41-56][sym-41] |
| Genesis | 2016-03-24 16:00 UTC | **2026-09-04 12:00 UTC** ⁵ | Genesis | [config.hpp:155][cfg-155] |
| Release | 1.28.7 | **1.29.0** | Software | [config.hpp:143][cfg-143] |
| Hardforks | 28 | **29** ⁶ | Consensus | `get_hardfork_properties` |

1. The ASCII bytes of `pixagram`, zero-padded to 32 bytes.
2. Pixa Supra. PXS promises no price; its rules are in [Pixa Supra (PXS) and the price feed](#pixa-supra-pxs-and-the-price-feed).
3. Called Pixa Power (PXP) in prose.
4. These are the symbol bytes in the legacy, pre-NAI wire format. Clients that hard-code Steem's bytes produce invalid signatures.
5. A new chain: no balances were carried over from Steem or Hive. What genesis created is in [Genesis](#genesis).
6. Hardforks 1–28 all applied at block 1; hardfork 29 applied at block 402,205.

## Genesis

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Liquid tokens at genesis | — | **0 PIXA** | Genesis | [database_init.cpp:386-421][init-386] |
| Stake at genesis | — | **100,000,000 VESTS**, backed by 100,000,000 PIXA | Genesis | [database_init.cpp:386-421][init-386] |
| `pixa.rex` | — | **75,000,000 VESTS** | Genesis | [database_init.cpp:390-392][init-390] |
| `pixa.team` | — | **25,000,000 VESTS** | Genesis | [database_init.cpp:390-392][init-390] |
| `pixa.omnibus` (treasury) | — | **245,098.039 PXS** ¹ | Genesis | [database_init.cpp:390-392][init-390] |
| Airdrop or mining | — | none | Genesis | — |

1. 25,000,000 PIXA ÷ 102, the genesis feed of 102 PIXA per PXS. The accounts and their rules are on [System Accounts](system-accounts.md).

## Blocks and witnesses

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Block interval | 3 s | 3 s | Consensus | [config.hpp:59][cfg-59] |
| Witness slots per round | 21 (20 elected + 1 timeshare) | same | Consensus | [config.hpp:65][cfg-65], [230-232][cfg-230] |
| Witnesses scheduled | 21 | 9 on 2026-10-05 | State | `get_witness_schedule` |
| Witnesses to run the chain | — | up to 21 elected, 1 required | Consensus | [config.hpp:65][cfg-65] |
| Irreversibility | a supermajority of scheduled witnesses | same | Consensus | [config.hpp:407][cfg-407] |
| Hardfork activation | a supermajority of scheduled witnesses | same | Consensus | `get_witness_schedule` |
| Witness votes per account | 30 | 30 | Consensus | [config.hpp:256][cfg-256] |
| Proxy chain depth | 4 | 4 | Consensus | [config.hpp:238][cfg-238] |

## Transaction and block size

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Maximum block size, allowed range | 64 KiB – 2 MiB | **128 KiB – 2 MiB** | Consensus | [config.hpp:391-392][cfg-391] |
| Maximum block size, live median | 65,536 bytes | **2,097,152 bytes** | Witness median | `get_chain_properties` |
| Largest transaction | 65,280 bytes ¹ | **2,096,896 bytes** ¹ | Witness median | [database.cpp:576-582][db-580] |
| `HIVE_MAX_TRANSACTION_SIZE` | 64 KiB | **128 KiB** ² | Consensus | [config.hpp:390][cfg-390] |
| `custom` / `custom_json` payload | 8 KiB | **64 KiB** | Consensus | [config.hpp:452][cfg-452] |
| Post body | no own limit ³ | no own limit ³ | Consensus | [hive_operations.cpp:123-138][ops-123] |
| Request size at `api.pixagram.com` | — | about 1 MiB ⁴ | Software | measured 2026-10-05 |
| Transaction expiry | up to 24 h ahead | up to 24 h ahead ⁵ | Consensus | [config.hpp:235-236][cfg-235], [database.cpp:2552-2557][db-2552] |

1. The live maximum block size minus 256 bytes, checked when a node accepts a transaction.
2. Despite its name, this constant only sets the smallest block size witnesses may vote for ([config.hpp:391][cfg-391], [hive_operations.cpp:312-325][ops-312]). It does not cap transactions.
3. The body must be non-empty UTF-8; otherwise only the transaction limit applies. Artwork posts published from 2026-09-04 to 2026-10-04 had a median body of about 26 kB, and the largest so far is 497,479 bytes (block 65,406).
4. Larger requests are refused with HTTP 413.
5. Since hardfork 28, a transaction may name an expiry up to 24 hours ahead. A node drops a transaction that is still unconfirmed 1 hour after it first saw it.

## Accounts and keys

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Account name length | 3–16 | 3–16 | Consensus | [config.hpp:374-375][cfg-374] |
| Account creation fee, floor | 0.001 HIVE | 0.001 PIXA | Consensus | [config.hpp:167][cfg-167] |
| Account creation fee, live median | 3.000 HIVE | **20.000 PIXA** ¹ | Witness median | `get_chain_properties` |
| Free account tickets | subsidy budget 797, decay 347,321 | same ² | Witness median | [config.hpp:443-445][cfg-443] |
| Owner-key recovery window | 30 days | 30 days | Consensus | [config.hpp:170][cfg-170] |
| Recovery request lifetime | 1 day | 1 day | Consensus | [config.hpp:171][cfg-171] |
| Owner-key changes | 2 per 60 min | 2 per 60 min | Consensus | [config.hpp:172][cfg-172], [owner_update_limit_mgr.cpp:15-25][own-15] |
| Owner-key history recorded from | block 3,186,477 | block 3,186,477, **about 2026-12-24** ³ | Consensus | [config.hpp:173][cfg-173] |
| Keys and accounts per authority | 40 | 40 | Consensus | [config.hpp:401][cfg-401] |
| Memo size | under 2,048 bytes | under 2,048 bytes | Consensus | [config.hpp:237][cfg-237] |

1. The fee is burned: it is paid to `null` ([hive_evaluator_account.cpp:193][acc-193]).
2. Tickets are claimed with Resource Credits instead of a fee.
3. Account recovery needs this history ([database.cpp:1694-1699][db-1694], [hive_evaluator_account.cpp:578][acc-578]). On Pixa, no recovery request can succeed until about 2026-12-24.

## Posts and comments

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Payout window | 7 days | 7 days | Consensus | [config.hpp:160][cfg-160] |
| Title | under 256 bytes | same | Consensus | [config.hpp:454][cfg-454] |
| Permlink | under 256 bytes | same | Consensus | [config.hpp:378][cfg-378] |
| Beneficiaries per post | 8 ¹ | 8 ¹ | Software | [config.hpp:302][cfg-302], [453][cfg-453] |
| Reply depth | 255 ¹ | 255 ¹ | Software | [config.hpp:300-301][cfg-300] |
| Interval between top-level posts | 5 min | 5 min | Consensus | [config.hpp:45][cfg-45] |
| Interval between replies, and between edits | 3 s | 3 s | Consensus | [config.hpp:46-47][cfg-45] |
| Minimum payout | 0.020 HBD | 0.020 PXS | Consensus | [config.hpp:363][cfg-363] |
| Late-vote damping | last 12 h | last 12 h ² | Consensus | [config.hpp:164][cfg-164], [hive_evaluator_social.cpp:713-718][soc-713] |

1. The limit that nodes apply when accepting transactions. Consensus allows up to 127 beneficiaries and a reply depth of 65,535.
2. Votes are accepted until payout, but in the last 12 hours each vote's rshares, up or down, are multiplied by the time left ÷ 12 hours.

## Voting and curation

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Voting mana recharge | 5 days | 5 days | Consensus | [config.hpp:246][cfg-246] |
| Cost of a full-strength vote | 2% of full mana | 2% of full mana ¹ | Consensus | [database_hardfork.cpp:311][hf-311], [hive_evaluator_social.cpp:663-690][soc-663] |
| Downvote mana | 25% of voting mana | same | Consensus | [config.hpp:251][cfg-251] |
| Vote dust deduction | 50,000,000 rshares | same ² | Consensus | [config.hpp:250][cfg-250] |
| Curation share of post rewards | 50% | **40%** | Consensus | [database_hardfork.cpp:451][hf-451] |
| Author reward curve | linear | **convergent linear** | Consensus | [database_hardfork.cpp:494-496][hf-494] |
| Curation reward curve | linear | **convergent square root** ³ | Consensus | [database_hardfork.cpp:494-496][hf-494] |
| Content constant *s* | 2,000,000,000,000 | **2,500** | Consensus | [config.hpp:271][cfg-271] |
| Curation weight by vote age | full · ½ after 24 h · ⅛ after 72 h | same | Consensus | [config.hpp:189-190][cfg-189] |
| Reverse auction | none | none | Consensus | [config.hpp:188][cfg-188] |
| Claims decay | 15 days | 15 days | Consensus | [config.hpp:324][cfg-324] |
| Reward-fund reset | — | **at most 2.75 × 10¹³** ⁴ | Consensus | [config.hpp:273-294][cfg-294] |

1. Since hardfork 28, the cost is a share of the full mana bar, whatever is left: 50 full-strength votes empty a full bar, and a vote's strength does not shrink as mana runs down.
2. Every vote loses this amount ([hive_evaluator_social.cpp:710-711][soc-710]). On Pixa 1 VESTS ≈ 1 PIXA, against about 1,608 VESTS per HP on Hive, so a full-strength vote needs **more than 2,500 Pixa Power to count at all**. On Hive the same threshold is about 1.6 HP.
3. Earlier votes earn more than later votes of equal weight.
4. Hardfork 29 lowered the reward fund's `recent_claims` to at most this value ([database_hardfork.cpp:525-561][hf-525]). The value inherited from Hive had made early payouts too small to pay.

## Pixa Power (staking)

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| VESTS per liquid token | about 1,608, falling | **1, flat** ¹ | Genesis / State | [config.hpp:53][cfg-53] |
| Reward for holding stake | 15% of issuance | **0** | Consensus | [database_hardfork.cpp:430-432][hf-430] |
| Power-down | 13 weekly instalments | same | Consensus | [config.hpp:240-241][cfg-240] |
| Power-down routes | 10 | 10 | Consensus | [config.hpp:242][cfg-242] |
| Delegation return | 5 days | 5 days | Consensus | [config.hpp:417][cfg-417] |
| Governance weight of new stake, rewards excepted | after 30 days | after 30 days | Consensus | [config.hpp:185][cfg-185] |

1. 1 VESTS was worth 1 PIXA at genesis, and the ratio stays flat because nothing is added to the vesting fund without issuing VESTS (live: 1 VESTS = 1.0000000072 PIXA). On Hive the vesting reward adds HIVE to the fund without new VESTS, so each VESTS is worth more over time. The Hive figure is from 2026-10-05.

## Issuance

New PIXA is created in every block. The yearly rate depends only on the block number *h*:

```
rate(h) = max( 9.78% − 0.01 percentage points × floor(h / 250,000) , 0.95% )
```

The constants are Hive's ([config.hpp:260-262][cfg-260], [database.cpp:1732-1737][db-1732]). Pixa counts *h* from its own genesis, so it restarted Hive's schedule at the top.

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Rate today | 5.36% | **9.75%** | State | formula, at the live block |
| Floor of 0.95% reached | block 220,750,000 | same, **about 2047** | Consensus | formula |
| Base | supply + non-treasury debt token at the median ¹ | same | Consensus | [database.cpp:1740-1752][db-1740] |
| Split: content / stake / fund / witnesses | 65 / 15 / 10 / 10% | **70 / 0 / 15 / 15%** | Consensus | [config.hpp:267-268][cfg-267], [database_hardfork.cpp:430-432][hf-430] |
| Witness share per block | nominal ² | **larger while fewer than 21 run** ² | Consensus | [database.cpp:1762-1779][db-1762] |
| Fund share per block | converted to HBD, rounded down ³ | **converted to PXS**, rounded down ³ | Consensus | [database.cpp:1783-1787][db-1783] |

1. On Pixa: the PIXA supply plus the PXS outside the treasury, valued at the median feed.
2. Each block pays its producer a share of the nominal witness amount. With a full schedule this averages to the nominal share; while fewer witnesses run, each active witness receives more, so on 2026-10-05 a block paid about 2.33 times the nominal share.
3. Rounded down to 0.001 of the token in every block. The rule is Hive's; on Pixa the share per block is small enough for the rounding to matter.

**What this means today.** In block 892,950 the nominal issuance was 0.934 PIXA:

- **Content:** 0.653 PIXA to the reward fund.
- **DPF:** its 0.140 PIXA came to 0.0027 PXS at 51.833 PIXA per PXS. It was rounded down to 0.002 PXS, about 74% of its share.
- **Witnesses:** about 0.329 PIXA, paid as Pixa Power, while 9 witnesses run.

Together the chain issues about **1.16 times the nominal amount**, or about 11.3% a year in PIXA-equivalent terms while 9 witnesses run. The witness part falls to its nominal share as the count approaches 21. The DPF's rounding loss remains, and its size depends on the feed price.

## Pixa Supra (PXS) and the price feed

PXS promises no price. It has no peg, cannot be redeemed for money and pays no interest, and no one stands behind its value. The rows below are the rules the chain applies to it.

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| What a feed states | HIVE per HBD (US dollar) | **PIXA per PXS (one Big Mac)** ¹ | Software | [bigmac-feed-agnostic][feed] |
| Feed sample | hourly, middle feed | same | Consensus | [config.hpp:192][cfg-192] |
| Feeds needed for a sample | 7 | a quorum of the scheduled witnesses ² | Consensus | [database.cpp:2445-2447][db-2445] |
| Feed lifetime | 7 days | 7 days | Consensus | [config.hpp:195][cfg-195] |
| Median in force | last 84 samples (3.5 days) | same | Consensus | [config.hpp:194][cfg-194] |
| Genesis median | none | **102 PIXA per PXS** | Genesis | [database_init.cpp:433-441][init-433] |
| Live median | — | 51.833 PIXA per PXS ³ | State | `get_current_median_history_price` |
| Interest | savings only; witness median, 10% live | **0, liquid or in savings, enforced** ⁴ | Consensus | [hive_operations.cpp:329-336][ops-329] |
| Printing stops at debt ratio | 20% | 20% ⁵ | Consensus | [config.hpp:369-370][cfg-369] |
| Haircut starts at debt ratio | 30% | 30% ⁶ | Consensus | [config.hpp:372][cfg-372] |
| Conversion PXS → PIXA | 3.5 days, at the median | same ⁶ | Consensus | [config.hpp:199][cfg-199] |
| Conversion PIXA → PXS | 200% collateral, 5% fee, 3.5 days | same ⁷ | Consensus | [config.hpp:201-202][cfg-201] |
| Savings withdrawal | 3 days | 3 days | Consensus | [config.hpp:204][cfg-204] |

1. With the agnostic feed, each witness enters the price of a Big Mac where it operates. On 2026-10-05 every witness published 51.833, the value `bigmac-feed` v1.0.3 computes from the US price ([Become a Witness](../10-node-operators/become-a-witness.md#5-publish-the-price-feed)). The feed software is not part of consensus.
2. The chain takes no sample in an hour when too few witnesses have a current feed; the median in force then stays as it was. `get_config` still prints `HIVE_MIN_FEEDS: 7`; the runtime check differs.
3. On 2026-10-05. See the placeholder note below.
4. Witnesses cannot publish any other value ([hive_operations.hpp:432][opsh-432]).
5. The debt ratio is the value of the PXS outside the treasury as a share of that PXS plus all PIXA. While it is under 20%, part of each author reward is paid in PXS. At or above 20%, that part is paid in PIXA ([database.cpp:2943-2964][db-2943]).
6. Above 30%, one PXS converts to at most **3P ÷ 7S PIXA**, where P is the PIXA supply and S the PXS outside the treasury ([database.cpp:2500-2528][db-2500]).
7. Refused if PXS would pass 20% ([hive_evaluator_transfer.cpp:579-580][tr-579]).

**The live median is a placeholder, not a market reading.** As of 2026-10-05, every witness publishes 6.22 USD (a US Big Mac) ÷ 0.12 USD, and 0.12 USD is an agreed placeholder price for PIXA. PIXA does not trade on any market yet. The feed in use, `bigmac-feed` v1.0.3, always divides by the placeholder; its successor, the agnostic feed, reads market prices and uses the placeholder only when told to with `--token-price`. Once a market exists, a witness's feed reads it only after the witness runs the agnostic feed without that setting ([Become a Witness](../10-node-operators/become-a-witness.md#5-publish-the-price-feed)).

**The same thresholds as collateral ratios.** Let R be the value of all PIXA divided by the value of the PXS outside the treasury, both at the median feed. The debt ratio d and R are linked by R = 1/d − 1. This gives:

- PXS printing stops at R ≤ **4×**.
- The haircut starts at R < **2.33×**. Below that, a PXS settles for the factor **min(1, 3R ÷ 7)** of its feed value.
- On 2026-10-05, R was about 845×.
- The protocol has no upper threshold.

The PXS design notes describe a corridor of "roughly 3× to 10×"; the numbers on this page are the ones the chain enforces ([the two compared](../05-pixa-supra/haircut-corridor-and-settlement.md#corridor-and-thresholds-design-and-chain)).

## Decentralized Pixa Fund (DPF)

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Treasury account | `hive.fund` | **`pixa.omnibus`** ¹ | Consensus | [config.hpp:482-483][cfg-482] |
| Daily budget | 1% of treasury, paid hourly | same | Consensus | [dhf_processor.cpp:153-158][dhf-153] |
| Liquid tokens in the treasury | converted to HBD | converted to PXS ² | Consensus | [hive_evaluator_transfer.cpp:266-285][tr-266] |
| Proposal fee | 10 HBD + 1 per day beyond 60 | 10 PXS + 1 per day beyond 60 | Consensus | [config.hpp:490-496][cfg-490] |
| Proposal subject | 80 bytes | 80 bytes | Consensus | [config.hpp:491][cfg-491] |
| Governance vote lifetime | 365 days | 365 days | Consensus | [config.hpp:178][cfg-178] |
| Return proposal | id 0 | **id 2** ³ | State | `list_proposals` |

1. On both chains `steem.dao` also counts as treasury. On Pixa, `pixa.omnibus` has no keys.
2. PIXA transferred to the treasury is converted at once, at the median. Any PIXA balance it holds converts at 0.05% per day ([config.hpp:497][cfg-497], [dhf_processor.cpp:342][dhf-342]).
3. A proposal id is chain data, not a constant.

## Resource Credits

| Parameter | Hive 1.28.7 | Pixa 1.29.0 | Kind | Source |
|---|---|---|---|---|
| Recharge | 5 days | 5 days | Consensus | [config.hpp:509][cfg-509] |
| Cost of an operation | set by network load | same | State | `rc_api.get_resource_pool`, `rc_api.get_rc_stats` |

## Reading live values

Every call below works against any public node; `api.pixagram.com` is the default. That endpoint renames Hive's `hbd_*` fields to `pxs_*` (for example `pxs_balance` and `current_pxs_supply`); `hived` itself keeps Hive's field names.

```bash
rpc() { curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"$1\",\"params\":$2,\"id\":1}"; }

rpc condenser_api.get_dynamic_global_properties '[]'   # supply, issuance split, block size, fund ledger
rpc database_api.get_config '{}'                        # compiled constants
rpc condenser_api.get_chain_properties '[]'             # witness medians: account fee, block size
rpc condenser_api.get_witness_schedule '[]'             # scheduled witnesses, hardfork quorum
rpc condenser_api.get_feed_history '[]'                 # 84 hourly samples and the median in force
rpc condenser_api.get_reward_fund '["post"]'            # curation share, curves, recent_claims
rpc database_api.get_hardfork_properties '{}'           # last and next hardfork
rpc database_api.list_proposals '{"start":[""],"limit":50,"order":"by_creator","order_direction":"ascending","status":"all"}'
```

## Figures you may meet elsewhere

| You may read | What the chain does |
|---|---|
| "72 kB posts" | No such limit exists. Posts are bounded by the transaction limit and, through the public endpoint, by its request size ([table](#transaction-and-block-size)). |
| "128 KiB transaction limit" | 128 KiB is only the smallest block size witnesses may vote for. |
| "1,000+ transactions per second" | That is capacity, not a measurement. A 2 MiB block every 3 seconds can carry far more small operations, and no load test of Pixa has been published. |
| "21 witnesses" | Up to 21 are elected and 1 is required. Read the live count from `get_witness_schedule`. |
| "Deflationary" | PIXA is issued in every block ([Issuance](#issuance)). The burns today are the account creation fee, the PIXA used up by PIXA → PXS conversions (5% fee included), and anything sent to `null`. |
| "17.5% of inflation to the DPF" | 15% nominal, reduced by rounding ([Issuance](#issuance)). |
| "PXS is pegged" | Nothing defends a PXS price. Witnesses report a Big Mac reference, and conversions settle at the median within the [haircut](#pixa-supra-pxs-and-the-price-feed). |
| "Zero fees" | Most operations carry no fee and consume Resource Credits instead. Three cost a fee: opening an account (or a ticket claimed with Resource Credits), creating a DPF proposal, and converting PIXA to PXS. |

[pixa-commit]: https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443
[hive-config]: https://github.com/openhive-network/hive/blob/1.28.7/libraries/protocol/include/hive/protocol/config.hpp
[feed]: https://github.com/pixagram-blockchain/bigmac-feed-agnostic
[cfg-45]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L45-L47
[cfg-53]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L53
[cfg-59]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L59
[cfg-65]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L65
[cfg-143]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L143
[cfg-145]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L145
[cfg-155]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L155
[cfg-160]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L160
[cfg-167]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L167
[cfg-170]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L170
[cfg-171]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L171
[cfg-172]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L172
[cfg-173]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L173
[cfg-178]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L178
[cfg-185]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L185
[cfg-188]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L188
[cfg-189]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L189-L190
[cfg-192]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L192
[cfg-194]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L194
[cfg-195]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L195
[cfg-199]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L199
[cfg-201]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L201-L202
[cfg-204]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L204
[cfg-215]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L215
[cfg-230]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L230-L232
[cfg-234]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L234
[cfg-235]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L235
[cfg-237]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L237
[cfg-238]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L238
[cfg-240]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L240-L241
[cfg-242]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L242
[cfg-246]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L246
[cfg-250]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L250
[cfg-251]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L251
[cfg-256]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L256
[cfg-260]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L260-L262
[cfg-267]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L267-L268
[cfg-271]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L271
[cfg-294]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L273-L294
[cfg-300]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L300-L301
[cfg-302]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L302
[cfg-363]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L363
[cfg-369]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L369-L370
[cfg-372]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L372
[cfg-374]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L374-L375
[cfg-378]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L378
[cfg-390]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L390-L391
[cfg-391]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L391-L392
[cfg-407]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L407
[cfg-417]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L417
[cfg-443]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L443-L445
[cfg-452]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L452
[cfg-453]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L453
[cfg-454]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L454
[cfg-482]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L482-L483
[cfg-490]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L490-L496
[cfg-491]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L491
[cfg-497]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L497
[cfg-509]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L509
[sym-20]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/asset_symbol.hpp#L20-L28
[sym-41]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/asset_symbol.hpp#L41-L56
[ops-123]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L123-L138
[ops-312]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L312-L325
[ops-329]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L329-L336
[opsh-432]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/hive_operations.hpp#L432
[db-580]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L576-L582
[db-1694]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1694-L1699
[db-1740]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1740-L1752
[db-1762]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1762-L1779
[db-1783]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1783-L1787
[db-2445]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2445-L2447
[db-2500]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2500-L2528
[db-2943]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2943-L2964
[hf-430]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L430-L432
[hf-451]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L451
[hf-494]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L494-L496
[hf-525]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L525-L561
[wsh-30]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/include/hive/chain/witness_schedule.hpp#L30-L39
[soc-710]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L710-L711
[acc-193]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L193
[acc-578]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_account.cpp#L578
[tr-266]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L266-L285
[tr-579]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L579-L580
[dhf-153]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/dhf_processor.cpp#L153-L158
[dhf-342]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/dhf_processor.cpp#L342
[sym-44]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/asset_symbol.hpp#L44-L45
[init-386]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_init.cpp#L386-L421
[init-433]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_init.cpp#L433-L441
[ws-207]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/witness_schedule.cpp#L207-L226
[ws-383]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/witness_schedule.cpp#L383-L387
[db-2552]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2552-L2557
[db-1732]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1732-L1737
[own-15]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/owner_update_limit_mgr.cpp#L15-L25
[cfg-401]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L401
[cfg-164]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L164
[soc-713]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L713-L718
[soc-663]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_social.cpp#L663-L690
[hf-311]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L311
[cfg-324]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L324
[init-390]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_init.cpp#L390-L392
