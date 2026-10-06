# Genesis and Distribution

> **Status: Live.** Balances and transfers were read at block 895,415 on 2026-10-05. The distribution commitments on this page are the operator's; the protocol does not enforce them.

The Pixa chain inherited no balances from Steem or Hive. Its genesis created all of its stake in two accounts that can do little except hand it out, plus a seeded community fund. This page describes what genesis created, the rules on those accounts, what has been handed out so far, and how to follow the rest.

## What genesis created

Block 0, on 2026-09-04 at 12:00 UTC, wrote three balances:

| Account | Created | Share of PIXA at genesis | Purpose |
|---|---|---|---|
| `pixa.rex` | 75,000,000 VESTS | 75% | Operator allocation, held for Pixa Rex S.A. |
| `pixa.team` | 25,000,000 VESTS | 25% | Team and contributors |
| `pixa.omnibus` | 245,098.039 PXS | none | Treasury of the [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md) |

- **All PIXA started as stake.** The 100,000,000 VESTS were backed by 100,000,000 PIXA in the vesting fund. There was no liquid PIXA, no airdrop and no mining.
- **The fund's seed** is 25,000,000 PIXA ÷ 102, the genesis feed of 102 PIXA per PXS.
- **No operation records them.** The balances were written straight into the initial state. Tools that rebuild balances by adding up operations must add these three by hand.

Every figure, with its source, is in [Chain Parameters](../11-reference/chain-parameters.md#genesis).

## The rules on the allocation accounts

The protocol restricts `pixa.rex` and `pixa.team` to two kinds of operation: transferring VESTS, and updating their own account, meaning its keys and metadata ([System Accounts](../11-reference/system-accounts.md#restricted-accounts-pixarex-and-pixateam)). This has four consequences:

- **The allocations cannot vote.** Neither account can vote for witnesses or on proposals, or set a proxy.
- **Stake leaves only as stake.** A recipient gets Pixa Power. Turning it into liquid PIXA takes a 13-week power-down ([Pixa Power](pixa-power.md#power-down)).
- **New stake waits 30 days for a voice.** Stake received from either account counts at once for voting on posts and for Resource Credits, but only after 30 days in governance.
- **Each transfer needs three signatures.** Genesis set up both accounts as 3-of-3 multisig. The signers could change that arrangement; the restriction itself they cannot change.

## What has been handed out

| Date (UTC) | From | To | VESTS |
|---|---|---|---|
| 2026-09-04 18:32–18:40 | `pixa.team` | six accounts | 16,510,000, from 150,000 to 8,000,000 each |
| 2026-09-05 18:12 | `pixa.rex` | `pixa`, the operator's working account | 15,000,000 |
| 2026-09-05 18:12 | `pixa.rex` | two other accounts | 500,000, 250,000 each |

No other transfer had left either account by 2026-10-05.

| Account | Left on 2026-10-05 | Share of its allocation |
|---|---|---|
| `pixa.rex` | 59,500,000 VESTS | 79.3% |
| `pixa.team` | 8,490,000 VESTS | 34.0% |

**From stake to liquid PIXA.** `pixa` began powering down all 15,000,000 VESTS on the day it received them. It receives 1,153,846.154 VESTS as PIXA every week for 13 weeks, ending about 2026-12-05. By 2026-10-05, four instalments had been paid.

## Where the stake is now

| Holder | VESTS | Share of all stake |
|---|---|---|
| `pixa.rex` and `pixa.team`, which cannot vote | 67,990,000.000 | 72.31% |
| `pixa`, powering down | 10,384,615.385 | 11.04% |
| The eight other accounts that received allocations | 15,342,918.468 | 16.32% |
| Every other account | 310,257.032 | 0.33% |
| **Total** | **94,027,790.885** | **100%** |

After one month, nearly all stake is still allocation stake or stake that came from it. The 0.33% is what other accounts have earned or been given: witness pay, author and curation rewards, and PIXA they received and powered up. What this means for votes is set out in [Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md).

## What the operator has committed to

| Account | Commitment | Enforced by the protocol? |
|---|---|---|
| `pixa.rex` | Distribute the whole allocation within 9 to 11 years of the token generation event (TGE), through `pixa` | No. No schedule or deadline is enforced. |
| `pixa.team` | Pay team members and contributors, with no fixed schedule | No |

What the protocol does enforce is the form: stake leaves only as VESTS, and it gains a governance voice only after 30 days.

## Follow it yourself

```bash
rpc() { curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"$1\",\"params\":$2,\"id\":1}"; }

# Every transfer out of the allocation accounts
rpc condenser_api.get_account_history '["pixa.rex",-1,100]'
rpc condenser_api.get_account_history '["pixa.team",-1,100]'

# Balances, and the power-down of the operator's working account
rpc condenser_api.get_accounts '[["pixa.rex","pixa.team","pixa"]]'
```

In `get_accounts`, `vesting_withdraw_rate` is the weekly instalment, `to_withdraw` and `withdrawn` give the total and the part paid (in millionths of a VESTS), and `next_vesting_withdrawal` is the next date.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Starting supply | Steem: none. Hive: a copy of Steem's balances, minus 328 accounts | 100,000,000 PIXA, all staked in two allocation accounts |
| How tokens first spread | Steem: proof-of-work mining, then rewards; until hardfork 16, late in 2016, 9 of every 10 new STEEM went to Steem Power holders | Transfers of stake from the allocations; rewards |
| Rules on founding stake | none | VESTS transfers only; no voting |
| Treasury at launch | Hive: Steem's treasury balance, plus the balances of the 328 excluded accounts | 245,098.039 PXS |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): "Allocation & Supply".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §II.4, and the [Hive launch post](https://hive.blog/communityfork/@hiveio/announcing-the-launch-of-hive-blockchain).
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - genesis balances: [database_init.cpp:386-421](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database_init.cpp#L386-L421)
  - the restriction: [database.cpp:2762-2810](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2762-L2810)
  - VESTS transfers and their 30-day wait: [hive_evaluator_transfer.cpp:287-341](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L287-L341)
- **Live chain**: the account histories of `pixa.rex` and `pixa.team`, and `condenser_api.get_accounts` for all 83 accounts at block 895,415.
- **Commitments**: stated by the operator; see [System Accounts](../11-reference/system-accounts.md#what-each-allocation-is-for).
