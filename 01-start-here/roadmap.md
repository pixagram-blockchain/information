# Roadmap

> **Status:** Live items run on mainnet today. The one dated item is **Planned (2027)**. Last updated 2026-10-08.

This page lists what exists, what is committed with a date, and what is only proposed. It replaces the dates in earlier articles, such as a pre-alpha "by May 2025", which have passed. It makes no statement about prices, exchanges or listings.

## Live

| Area | Since | What runs |
|---|---|---|
| Chain | 2026-09-04 | Pixa mainnet: 3-second blocks, witnesses, Resource Credits, hived 1.30.0 since hardfork 30 (2026-10-07) |
| Publishing | 2026-09-04 | Artworks stored inside posts; comments |
| Rewards | 2026-09-18 | Proof-of-Brain payouts. Hardfork 29 fixed the inherited reward denominator, and the first post was paid about five minutes after it activated. Hardfork 30 (2026-10-07) let votes from small accounts count. |
| Wallet | 2026-09-04 | Transfers, staking, delegation, PIXA ↔ PXS conversion, savings, tax reports |
| Governance | 2026-09-04 | Witness elections and the Decentralized Pixa Fund; the return proposal has been in place since 2026-09-24 |
| Communities | 2026-09-12 | 12 communities, including the official Proposals, Governance and Development portals; blog posts within them |
| Accounts | 2026-09 | Free sign-up after phone verification, funded by a DPF proposal through 2026-12-31 |
| Account recovery | 2026-10-07 | The chain records owner-key history since hardfork 30, so a stolen owner key can be reversed through a recovery partner; the app has no screen for it yet ([Keys and Recovery](../08-guides/keys-and-recovery.md#if-your-keys-are-stolen)) |

## Planned (2027)

**Buying and selling artworks on chain.** The aim is a marketplace built into the protocol rather than added on top. [NFTs and Marketplace](../17-marketplace/nfts-and-marketplace.md) separates what is decided from what is still open.

## Scheduled by the protocol

These are not product promises. They are dates already fixed by the chain's own rules.

| When | What |
|---|---|
| about 2047 (block 220,750,000) | The yearly issuance rate reaches its floor of 0.95% ([Issuance](../21-reference/chain-parameters.md#issuance)). |

## Proposed, not committed

| Item | State |
|---|---|
| Constitution | Five principles drafted in 2025; not adopted ([Constitution](../07-governance/constitution.md)) |
| Marketplace fees | 10% on first sales and 2.5% on resales, paid in PIXA and burned, proposed in 2025; not decided |
| Payout choices in the app | The chain lets authors decline rewards or take them all as Pixa Power; the app does not offer this yet |

## How this page changes

Items move from *Proposed* to *Planned* only with a date, and from *Planned* to *Live* only when they run on mainnet. A date that slips is changed here, never left to stand.

## Sources

- Chain milestones: `condenser_api.get_ops_in_block` for blocks 1 and 402,205; [Chain Parameters](../21-reference/chain-parameters.md).
- First reward payout after hardfork 29: the `author_reward` operation at 2026-09-18 12:05:30 UTC (account history).
- Communities: `bridge.list_communities`, read on 2026-10-05.
- Account funding: DPF proposal 1 (`database_api.list_proposals`).
