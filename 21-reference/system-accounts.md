# System Accounts

> **Status: Live.** Balances shown are a snapshot from block 893,370 (2026-10-05). For current figures, run the calls in [Check them yourself](#check-them-yourself).

A few accounts were created at genesis (block 0, and block 1 for `steem.dao`) and follow rules no ordinary account has. Three hold the genesis allocation: two stake allocations and the treasury. The others are placeholders inherited from Hive's code. This page explains what each account is for, what the protocol allows it to do, and how to verify it.

## At a glance

| Account | Role | At genesis | 2026-10-05 | Keys | Rules |
|---|---|---|---|---|---|
| `pixa.rex` | Operator allocation, held for Pixa Rex S.A. | 75,000,000 VESTS | 59,500,000 VESTS | 3-of-3 multisig | [Restricted](#restricted-accounts-pixarex-and-pixateam): may only move VESTS and update its own keys |
| `pixa.team` | Team and contributor allocation | 25,000,000 VESTS | 8,490,000 VESTS | 3-of-3 multisig | [Restricted](#restricted-accounts-pixarex-and-pixateam), same rules |
| `pixa.omnibus` | Treasury of the Decentralized Pixa Fund | 245,098.039 PXS | 249,310.119 PXS | none | [Keyless](#the-treasury-pixaomnibus); pays only proposals that stakeholders approve |
| `steem.dao` | Old treasury name inherited from Hive | created empty at block 1 | empty | none | Still counts as a treasury; anything sent to it is moved to `pixa.omnibus` |
| `initminer` | First block producer | nothing | 43,141.908819 VESTS | single key | Ordinary account, registered as a witness; not among the scheduled witnesses on 2026-10-08 |
| `null` | Burn address | — | — | none | Everything sent here is destroyed in the same block |
| `temp` | Open placeholder | — | — | threshold 0 | **Anyone can spend from it.** Never send it anything. |
| `miners` | Placeholder from Steem's mining era | — | — | none | Unused |
| `steem` | Placeholder from Steem's genesis | — | — | none | Unused |

VESTS are Pixa Power, the staked form of PIXA. On this chain 1 VESTS has stayed worth almost exactly 1 PIXA since genesis ([Chain Parameters](chain-parameters.md#pixa-power-staking)).

## Genesis allocation

Block 0 created 100,000,000 VESTS, backed by 100,000,000 PIXA in the vesting fund, plus 245,098.039 PXS ([figures and sources](chain-parameters.md#genesis)):

| Holder | Allocation | Share of PIXA supply at genesis |
|---|---|---|
| `pixa.rex` | 75,000,000 VESTS | 75% |
| `pixa.team` | 25,000,000 VESTS | 25% |
| `pixa.omnibus` | 245,098.039 PXS: 25,000,000 PIXA ÷ 102, the genesis feed of 102 PIXA per PXS | none (it holds PXS, not PIXA) |

There was no liquid PIXA at genesis, no airdrop and no mining. All liquid PIXA since then has come from three sources:

- per-block [issuance](chain-parameters.md#issuance)
- stake that left these accounts and was powered down
- PXS converted into PIXA

These balances were written straight into the initial state ([database_init.cpp:386-421][init-386]). No operation records them, so tools that rebuild balances by adding up operations will not see them.

## Restricted accounts: pixa.rex and pixa.team

The protocol locks both allocation accounts down to one job: holding stake and handing it out.

**What they can do**

- **Transfer VESTS directly to another account.** This is a `transfer` operation with a VESTS amount, and no other account can send one ([hive_operations.cpp:245][ops-245]). The stake arrives in the recipient's Pixa Power at once, along with matching voting mana and Resource Credits. Its weight in witness and proposal votes matures over the 30-day [delayed-voting](chain-parameters.md#pixa-power-staking) period ([hive_evaluator_transfer.cpp:287-341][tr-287]).
- **Update their own keys and metadata** with `account_update` or `account_update2`.

**What they cannot do.** Every other operation fails with `This account is restricted to VESTS transfers only.` That includes:

- liquid transfers
- powering up or down
- delegation
- savings
- claiming rewards
- posting
- voting on content
- witness votes and proxies
- `custom_json`

The check runs before any operation is applied. Any operation that requires either account's authority is rejected, including when that authority is nested inside another required authority ([database.cpp:2762-2810][db-2762]).

**Consequences**

- **The genesis stake does not vote.** Neither account can vote for witnesses or on DPF proposals. Stake gains a voice only after it leaves these accounts, and only after its 30-day maturity.
- **Stake leaves only by direct transfer.** Neither account can power down.
- **Anything else sent to them is stuck.** PIXA, PXS or rewards sent to either account can never be moved out. Do not send them funds.
- **The 3-of-3 multisig is a setup, not a rule.** Genesis set it on the owner, active and posting authorities, so three separate signers must approve each action. The signers can change the arrangement with `account_update`, because the protocol does not enforce 3 of 3. The memo key is a single key.

### What each allocation is for

These are commitments stated by the operator. The protocol does not enforce them, but anyone can check the outflows on chain.

| Account | Commitment | How stake leaves |
|---|---|---|
| `pixa.rex` | Distribute the whole allocation within 9 to 11 years of the token generation event (TGE). | VESTS transfers to the operator's working account `pixa` (see [Operational accounts](#operational-accounts)), which powers the stake down for distribution. |
| `pixa.team` | Pay team members and contributors. There is no fixed schedule. | VESTS transfers straight to the people being paid. |

## The treasury: pixa.omnibus

`pixa.omnibus` holds the Decentralized Pixa Fund (DPF).

**It has no keys.** Genesis created it without keys, and hardfork 24, applied at block 1, locked it ([database_hardfork.cpp:576-587][hf-576]). Locking empties its owner, active and posting authorities. No person, company or foundation can sign for it.

**How money comes in**

- **A share of issuance.** Every block it receives the DPF's share of new issuance, converted to PXS at the median feed ([Chain Parameters](chain-parameters.md#issuance)).
- **PIXA sent to it.** This is converted to PXS at once.

**How money goes out.** It only pays proposals:

- Once an hour it pays active proposals in order of their votes.
- Payouts stop at a daily budget of 1% of the treasury balance.
- Proposals ranked below the return proposal (id 2 on this chain) receive nothing. That proposal sends its pay straight back to the treasury.
- Proposal votes are cast with Pixa Power.

**It holds PXS only.** PIXA sent to it is converted into PXS at once, and no one can stake on its behalf. Proposals are paid from its PXS balance.

**Don't confuse it with the Foundation.** The *Pixa Omnibus Foundation* is a legal entity: the protocol's steward. It holds no keys to this account.

`steem.dao` is the name of Steem's original treasury, which the inherited code still recognises. It was created, empty and locked, when hardfork 21 ran at block 1. Any balance that reaches it is moved to `pixa.omnibus` in the same block ([database.cpp:1283-1310][db-1283]).

## initminer

`initminer` produced the chain's first blocks and was the only witness at genesis. It started with no balance and earned Pixa Power by producing blocks, 45,515.494253 VESTS by 2026-10-08. Today it is an ordinary account; it remains registered as a witness but was not among the 8 scheduled on 2026-10-08 (`condenser_api.get_witness_schedule`).

## Placeholders inherited from Hive

| Account | Origin | Behaviour on Pixa |
|---|---|---|
| `null` | Hive's burn address | No authority can spend from it. Any balance sent to it is destroyed in the same block ([database.cpp:1178][db-1178]). Account creation fees end up here. |
| `temp` | Hive's open-authority account | Its authorities have threshold 0, so **anyone can spend what it holds**. Never send anything to it. |
| `miners` | Steem's proof-of-work era | Unused. |
| `steem` | Steem's founding account | Created at genesis with no keys, as a placeholder for code inherited from Steem. Unused. |

## Operational accounts

Some accounts matter to the project but follow ordinary rules.

| Account | Role |
|---|---|
| `pixa` | Working account of the operator, Pixa Rex S.A. It receives stake from `pixa.rex` for distribution. |
| Witnesses | Block producers are listed live on the [witness status page](https://pixagram.com/witness-status/). |

## Check them yourself

```bash
rpc() { curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"$1\",\"params\":$2,\"id\":1}"; }

# Balances and keys of every account on this page
rpc condenser_api.get_accounts '[["pixa.rex","pixa.team","pixa.omnibus","steem.dao","initminer","null","temp","miners","steem","pixa"]]'

# Proposals the treasury pays, including the return proposal
rpc database_api.list_proposals '{"start":[""],"limit":50,"order":"by_creator","order_direction":"ascending","status":"active"}'
```

The public endpoint returns `pxs_balance`. A node queried directly returns `hbd_balance`.

## Notes for developers

- **Transfers look like ordinary transfers.** VESTS transfers from the restricted accounts appear in history as plain `transfer` operations with a VESTS amount, for example `"1000.000000 VESTS"`. They emit no virtual operation.

[init-386]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_init.cpp#L386-L421
[ops-245]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L245
[tr-287]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L287-L341
[db-2762]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2762-L2810
[hf-576]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_hardfork.cpp#L576-L587
[db-1283]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1283-L1310
[db-1178]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L1178-L1195
