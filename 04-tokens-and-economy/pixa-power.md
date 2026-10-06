# Pixa Power

> **Status: Live.** Figures from the live chain were read at block 895,415 on 2026-10-05.

Pixa Power (PXP) is PIXA that has been staked. It is the weight behind everything an account does on chain: its votes on posts, its Resource Credits, and its say in governance. This page explains what it gives you, how to stake and unstake, how to lend it, and the rules that protect governance from fresh stake.

## What Pixa Power gives you

| Use | How it works |
|---|---|
| **Voting on posts** | Your voting mana equals your effective Pixa Power. Votes direct rewards and earn curation rewards ([Voting and Curation](../02-social-layer/voting-and-curation.md)). |
| **Resource Credits** | About 1,000,000 credits per Pixa Power, recharging 20% a day ([Resource Credits](resource-credits.md)) |
| **Governance** | Votes for witnesses and on DPF proposals, weighted by your own Pixa Power. Stake you power up, or receive from the allocation accounts, counts after 30 days. |

**What it does not give you.** Holding Pixa Power earns nothing by itself. Hive adds 15% of issuance to staked tokens; Pixa adds none. One VESTS has therefore stayed worth about one PIXA since genesis. Stake grows only through rewards, powering up, or transfers.

## Effective Pixa Power

The chain counts slightly different amounts for different purposes:

| Counts toward | Own stake | Stake lent to you | Stake you have lent out |
|---|---|---|---|
| Voting mana and Resource Credits | yes | yes | no |
| Witness and proposal votes | yes, after the 30-day wait where it applies | no | **yes: still yours** |

This week's power-down instalment no longer counts toward voting mana or Resource Credits. Your governance weight falls by each instalment as it is paid out.

## Power up

Powering up turns liquid PIXA into Pixa Power immediately, at the current ratio of about 1:1. You can power up to your own account or to someone else's.

**Staked PIXA waits 30 days before it counts in governance.** Freshly added Pixa Power counts at once for voting on posts and for Resource Credits, but only after 30 days in witness and proposal votes. The wait applies to three kinds of new stake:

- stake from powering up
- stake received from the allocation accounts
- power-down instalments that a route stakes again

Rewards claimed as Pixa Power, and witness pay, count at once. The wait stops anyone from buying stake and swinging a governance vote the same day ([Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md)).

## Power down

Powering down turns Pixa Power back into PIXA in **13 weekly instalments**, the first 7 days after you start.

- **Starting again** replaces the previous schedule.
- **Cancelling** is done by setting the amount to 0.
- **Lent-out stake** must be taken back before it can be powered down.
- **Routes:** up to 10 can send the instalments to other accounts, either as PIXA or re-staked.

On 2026-10-05, nine accounts were powering down, with 14.39 million VESTS left to pay out at about 1.6 million a week.

## Delegation

Delegation lends Pixa Power to another account without giving it away.

- **The borrower gets** voting mana and Resource Credits.
- **You keep** ownership, and your governance weight still counts the stake as yours.
- **Minimum:** a new delegation must be at least about 6.67 VESTS (a third of the account creation fee in VESTS).
- **Return:** when you reduce or remove a delegation, the borrower loses it at once and you get it back after **5 days**.
- **Restrictions:** you can lend only stake you own, not stake you borrowed, and not stake being powered down. You can lend no more than your current voting mana, so stake whose mana you have just spent on votes must recharge first.

Delegation is how the app gives new accounts their first Resource Credits. On 2026-10-05, 7.03 million VESTS (7.5% of all stake) were lent from 9 accounts to 51.

## Giving up voting rights

An account can permanently give up its right to vote with `decline_voting_rights`.

- **Once applied, nothing can restore it.** The request needs the owner key and takes effect after 30 days. It can be cancelled during that time.
- **What it clears:** the account's witness votes, proxy and proposal votes.
- **What it blocks:** it also blocks votes on posts.

No account had made this request on 2026-10-05.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Power-down | 13 weekly instalments | same |
| Delayed governance weight | 30 days (Hive, since 2020) | same |
| Delegation return | 5 days | same |
| Reward for holding stake | 15% of issuance | none |
| VESTS per liquid token | about 1,608 on Hive, falling | about 1, flat |

## Sources

- **Code**
  - Power-down: [hive_evaluator_transfer.cpp:390-455](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L390-L455).
  - Delegation: [hive_evaluator_transfer.cpp:750-980](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L750-L980).
  - Governance weight: [account_object.hpp:302-317](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/include/hive/chain/detail/state/account_object.hpp#L302-L317).
  - Delayed voting: [delayed_voting.cpp:7-122](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/delayed_voting.cpp#L7-L122), applied to power-ups at [hive_evaluator_transfer.cpp:374-379](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/hive_evaluator_transfer.cpp#L374-L379).
- **Constants**: [Chain Parameters](../11-reference/chain-parameters.md#pixa-power-staking).
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §II.1 and §II.3.
- **Live chain**: accounts and delegations from `condenser_api.get_accounts`, read at block 895,415.
