# Who Does What

> **Status: Live.** This page describes the structure as the project states it. Where a role leaves a trace on chain, the page gives the account so you can check it. Last checked 2026-10-05.

Pixagram is built and run by several parties with separate jobs. Three legal entities share the off-chain work. Elected witnesses run the chain, and stakeholders govern the community fund. This page says who does what. It also lists what none of them can do alone.

## The three entities

| Entity | Seat | Role | On chain |
|---|---|---|---|
| **Pixagram SA** (commercial register CHE-299.606.603) | Zug, Switzerland | Develops the protocol and the app and owns their intellectual property, which it licenses for use. It does not operate the front-end. | Publishes the code under [github.com/pixagram-blockchain](https://github.com/pixagram-blockchain) |
| **Pixa Omnibus Foundation** | Cayman Islands | Stewards the protocol under licence and speaks for the ecosystem | Holds no keys; see the warning below |
| **Pixa Rex S.A.** | Panama | Operates the app at pixagram.com and its services, initiated the token generation event (TGE), and holds the operator allocation | [`pixa.rex`](../11-reference/system-accounts.md#restricted-accounts-pixarex-and-pixateam) (3-of-3 multisig); working account `pixa` |

**The Foundation is not the treasury account.** The *Pixa Omnibus Foundation* is a legal entity. [`pixa.omnibus`](../11-reference/system-accounts.md#the-treasury-pixaomnibus) is the keyless account that holds the Decentralized Pixa Fund. The Foundation cannot sign for that account or spend from it; only proposal votes move its funds.

Pixa Rex S.A. replaced Pixa Operations S.A. as operator in August 2026. The chain's source code still carries the old name in a comment. <!-- retired-ok -->

## The network's own roles

| Role | Who | What they decide |
|---|---|---|
| **Witnesses** | Elected block producers: up to 21 elected, 1 required, 9 on 2026-10-05 ([status page](https://pixagram.com/witness-status/)) | Which blocks are produced; the account creation fee and block size, through the median of their votes; the price feed; whether a new protocol version activates |
| **Stakeholders** | Every account with Pixa Power | Who the witnesses are; which DPF proposals are paid; where each day's rewards go, through their content votes |
| **Community moderators** | Owners, admins and moderators of each community | What is pinned or muted within their community. Their actions are recorded on chain as `custom_json` operations; the indexer and the app apply them. |
| **Node operators** | Anyone | Whether to serve the chain's data. Six public API nodes run on 2026-10-05. |

## What no single party can do

| Action | Who can do it, and how |
|---|---|
| Change the consensus rules | Only the witnesses, when a supermajority of them run a new version ([Protocol Upgrades](../07-governance/protocol-upgrades.md)) |
| Spend the community fund | Only stakeholders, by voting a proposal above the return proposal ([Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md)) |
| Vote with the genesis allocations | Nobody. `pixa.rex` and `pixa.team` cannot vote. |
| Move the genesis allocations | Only all three signers of each account together, and only as direct transfers of Pixa Power |
| Delete a post from the chain | Nobody. An app can stop showing a post, but the original stays in its block. |
| Set the price PXS converts at | No one alone. PXS promises no price: conversions use the median of the witnesses' feeds, reduced by the haircut when the network is stretched. Today every feed uses the same placeholder price for PIXA ([Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md)). |
| Print PIXA outside issuance | Nobody. New PIXA comes only from the issuance rule and from conversions. |

## Who pays for what today

**New accounts.** The app's sign-up service opens accounts through the account `rex`, which pays the account creation fee and lends each new account a little Pixa Power. DPF proposal 1, voted by stakeholders, pays `rex` 110 PXS a day until 2026-12-31 to cover account fees and SMS verification.

**Development, stewardship and operation** are financed by the entities above. The genesis allocations are described on [Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md).

## Sources

- The operator account and the treasury name in the chain's code: [config.hpp:483-485](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/config.hpp#L483-L485).
- Pixagram SA, Zug: the organisation profile at [github.com/pixagram-blockchain](https://github.com/pixagram-blockchain); the register number from the Swiss commercial register, as shown by [Moneyhouse](https://www.moneyhouse.ch/en/company/pixagram-ag-1298024171) (registered as Pixagram AG, Pixagram SA and Pixagram Ltd). <!-- retired-ok -->
- Witnesses and the hardfork quorum: `condenser_api.get_witness_schedule`, read on 2026-10-05.
- Proposal 1 and the return proposal: `database_api.list_proposals`, read on 2026-10-05.
- An account opened by `rex` with a 20.000 PIXA fee and a 100 VESTS delegation: `condenser_api.get_ops_in_block` at block 894,437.
