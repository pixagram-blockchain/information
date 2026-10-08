# Pixagram

**Proven tech. New canvas.** Pixagram is a social network for pixel art. It runs on the Pixa chain, a blockchain built from the code of Steem and Hive, and every artwork published there is written into the chain itself.

> **Status: Live.** Mainnet has run since 2026-09-04 and is on hived 1.30.0 since hardfork 30 on 2026-10-07. Buying and selling artworks on chain is planned for 2027. Titles in plain text in the contents below are planned pages, not yet written.

This repository holds Pixagram's documentation: what the network is, how to use it, how to build on it, and the figures behind it. Every page is a Markdown file that you can read here on GitHub.

Nothing here is financial, investment or legal advice. PIXA, Pixa Power and PXS carry risk, and PXS promises no price.

## At a glance

| Figure | What it means |
|---|---|
| **3 seconds** | per block |
| **Few fees** | Most operations draw on Resource Credits, which recharge from your stake. Opening an account, creating a proposal and converting PIXA to PXS cost a fee. |
| **In the block** | Each artwork is stored inside its post, not linked from elsewhere. |
| **Proof-of-Brain** | Stake-weighted votes decide which authors and curators are paid. |
| **No passive yield** | Holding PIXA, Pixa Power or PXS earns nothing by itself. Publishing, curating and producing blocks do. |
| **100 million PIXA** | at genesis, all of it staked |

Every figure, with its source in the code, is on [Chain Parameters](21-reference/chain-parameters.md).

## Where to start

- **New to Pixagram:** [What Is Pixagram](01-start-here/what-is-pixagram.md), then the [FAQ](01-start-here/faq.md).
- **Tokens and rewards:** [Tokens at a Glance](04-tokens-and-economy/tokens-at-a-glance.md) and [Proof-of-Brain](02-social-layer/proof-of-brain.md). For PXS, [PXS at a Glance](05-pixa-supra/pxs-at-a-glance.md).
- **Governance:** [Witnesses and DPoS](07-governance/witnesses-and-dpos.md), and how far the network is decentralized today: [Decentralization and Safeguards](07-governance/decentralization-and-safeguards.md).
- **Building an app:** [Developer Quickstart](09-developers/developer-quickstart.md) and [Differences from Hive](09-developers/differences-from-hive.md). The chain speaks Hive's JSON-RPC:

  ```bash
  curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
    -d '{"jsonrpc":"2.0","method":"condenser_api.get_dynamic_global_properties","params":[],"id":1}'
  ```

- **Running a node:** [Run a Node](10-node-operators/run-a-node.md) and [Become a Witness](10-node-operators/become-a-witness.md).
- **Checking a number or a name:** [Chain Parameters](21-reference/chain-parameters.md) and the [Glossary](21-reference/glossary.md).

## Contents

The pages are grouped in six parts, and each folder has its own index.

### Understand

- **[Start here](01-start-here/README.md):** [What Is Pixagram](01-start-here/what-is-pixagram.md) · [From STEEM to HIVE to PIXA](01-start-here/from-steem-to-hive-to-pixa.md) · [Design Principles](01-start-here/design-principles.md) · [Roadmap](01-start-here/roadmap.md) · [Who Does What](01-start-here/who-does-what.md) · [FAQ](01-start-here/faq.md)
- **[Social layer](02-social-layer/README.md):** [Proof-of-Brain](02-social-layer/proof-of-brain.md) · [Posting and Rewards](02-social-layer/posting-and-rewards.md) · [Voting and Curation](02-social-layer/voting-and-curation.md) · [Communities](02-social-layer/communities.md) · [Censorship Resilience and Moderation](02-social-layer/censorship-resilience-and-moderation.md)
- **[Art on chain](03-art-on-chain/README.md):** [Pixel Art On Chain](03-art-on-chain/pixel-art-on-chain.md) · [Permanence and Provenance](03-art-on-chain/permanence-and-provenance.md)
- **[Tokens and economy](04-tokens-and-economy/README.md):** [Tokens at a Glance](04-tokens-and-economy/tokens-at-a-glance.md) · [Pixa Power](04-tokens-and-economy/pixa-power.md) · [Resource Credits](04-tokens-and-economy/resource-credits.md) · [Supply, Inflation and Yield](04-tokens-and-economy/supply-inflation-and-yield.md) · [Genesis and Distribution](04-tokens-and-economy/genesis-and-distribution.md)
- **[Pixa Supra (PXS)](05-pixa-supra/README.md):** [PXS at a Glance](05-pixa-supra/pxs-at-a-glance.md) · [Supracoin vs Stablecoin](05-pixa-supra/supracoin-vs-stablecoin.md) · [The Four Components](05-pixa-supra/the-four-components.md) · [Oracle and Price Feed](05-pixa-supra/oracle-and-price-feed.md) · [Haircut, Corridor and Settlement](05-pixa-supra/haircut-corridor-and-settlement.md) · [From SBD to PXS](05-pixa-supra/from-sbd-to-pxs.md) <!-- retired-ok -->
- **[Economic cybernetics](06-economic-cybernetics/README.md):** [Viable System Model](06-economic-cybernetics/viable-system-model.md) · [Variety and Regulation](06-economic-cybernetics/variety-and-regulation.md) · [Resilience and Cascades](06-economic-cybernetics/resilience-and-cascades.md)
- **[Governance](07-governance/README.md):** [Witnesses and DPoS](07-governance/witnesses-and-dpos.md) · [Decentralized Pixa Fund](07-governance/decentralized-pixa-fund.md) · [Protocol Upgrades](07-governance/protocol-upgrades.md) · [Decentralization and Safeguards](07-governance/decentralization-and-safeguards.md) · [Constitution](07-governance/constitution.md)

### Use and build

- **[Guides](08-guides/README.md):** [Create an Account](08-guides/create-an-account.md) · [Keys and Recovery](08-guides/keys-and-recovery.md) · [Publish Your First Artwork](08-guides/publish-your-first-artwork.md) · [Wallet Basics](08-guides/wallet-basics.md) · [Take Part in Governance](08-guides/take-part-in-governance.md) · [Create a Community](08-guides/create-a-community.md)
- **[Developers](09-developers/README.md):** [Chain Architecture](09-developers/chain-architecture.md) · [Developer Quickstart](09-developers/developer-quickstart.md) · [Differences from Hive](09-developers/differences-from-hive.md) · [Artwork Encoding Spec](09-developers/artwork-encoding-spec.md) · [SDKs and Libraries](09-developers/sdks-and-libraries.md)
- **[Node operators](10-node-operators/README.md):** [Run a Node](10-node-operators/run-a-node.md) · [Run an API Node](10-node-operators/run-an-api-node.md) · [Become a Witness](10-node-operators/become-a-witness.md) · [CLI Wallet](10-node-operators/cli-wallet.md)

### Protocol, API and security

- **[Protocol reference](11-protocol-reference/README.md):** [Operations Reference](11-protocol-reference/operations-reference.md) · [Transaction Lifecycle](11-protocol-reference/transaction-lifecycle.md) · [Data Model](11-protocol-reference/data-model.md) · Consensus and Block Production
- **[API reference](12-api-reference/README.md):** [JSON-RPC Surface](12-api-reference/json-rpc.md) · per-namespace pages
- **[Security](13-security/README.md):** Threat Model · Key Security · Incident Response

### The application

- **[Pixagram product](14-product/README.md):** [Feed and Discovery](14-product/feed-and-discovery.md) · [Search](14-product/search.md) · [Notifications](14-product/notifications.md) · [Account Settings](14-product/account-settings.md) · Profiles and Following · Posts, Comments and Media
- **[Search and indexing](15-search-and-indexing/README.md):** [PAPH](15-search-and-indexing/paph.md) · Indexing Architecture
- **[AI and knowledge](16-ai-and-knowledge/README.md):** Proposed; nothing built yet

### Marketplace, infrastructure and economics

- **[Marketplace](17-marketplace/README.md):** [NFTs and Marketplace](17-marketplace/nfts-and-marketplace.md) · Marketplace Protocol
- **[Infrastructure](18-infrastructure/README.md):** [Architecture](18-infrastructure/architecture.md) · Monitoring · Disaster Recovery
- **[Economics lab](19-economics-lab/README.md):** [Reward Examples](19-economics-lab/reward-examples.md) · PXS Scenarios

### History, reference and about

- **[History and design](20-history-and-design/README.md):** [Network Timeline](20-history-and-design/network-timeline.md) · [The Plan Revisited](20-history-and-design/the-plan-revisited.md) · [Essays](20-history-and-design/essays.md)
- **[Reference](21-reference/README.md):** [Chain Parameters](21-reference/chain-parameters.md) · [System Accounts](21-reference/system-accounts.md) · [Glossary](21-reference/glossary.md) · [Risks and Open Problems](21-reference/risks-and-open-problems.md) · [Sources and Credits](21-reference/sources-and-credits.md)
- **[About these pages](22-about/README.md):** [Style Guide](22-about/style-guide.md) · Disclaimer · Regulatory Status · [Contributing](22-about/contributing.md)

## About the project

Pixagram's aim is simple: artists should own their work and be paid for it directly. They are paid through other members' votes ([Proof-of-Brain](02-social-layer/proof-of-brain.md)) and through tips. The chain started from a new genesis, with no airdrop and no mining ([Genesis and Distribution](04-tokens-and-economy/genesis-and-distribution.md)).

Three legal entities, in three jurisdictions, share the work ([Who Does What](01-start-here/who-does-what.md)):

- **Pixagram SA** (Switzerland) develops the protocol.
- **The Pixa Omnibus Foundation** (Cayman Islands) stewards it.
- **Pixa Rex S.A.** (Panama) operates the app.

## How the pages are written

| Part | Folders | Voice |
|---|---|---|
| **Understand** | `01-start-here` to `07-governance` | concepts, written precisely |
| **Use and build** | `08-guides` · `09-developers` · `10-node-operators` | guides step by step; exact commands, pinned versions |
| **Protocol, API and security** | `11-protocol-reference` · `12-api-reference` · `13-security` | specification: every rule with its source |
| **The application** | `14-product` · `15-search-and-indexing` · `16-ai-and-knowledge` | the product as it works, and which layer each behaviour belongs to |
| **Marketplace, infrastructure and economics** | `17-marketplace` · `18-infrastructure` · `19-economics-lab` | what exists, what is planned, and worked numbers |
| **History, reference and about** | `20-history-and-design` · `21-reference` · `22-about` | tables, sources, dated records, signed essays |

One question organises the pages: for every behaviour, is it a rule of the chain, a property of the indexer, or a choice of the Pixagram app? Each page says which. Three rules hold them together:

- **One reference for every number.** Every protocol value is on [Chain Parameters](21-reference/chain-parameters.md); other pages that quote one link there.
- **A status line on every page.** Each page opens with one of **Live**, **Planned (date)**, **Proposed** or **Historical**.
- **Inherited → changed.** Every concept page ends with a table of what Steem or Hive did and what Pixa does instead.

The [Style Guide](22-about/style-guide.md) has the rest.

## Editing

[Contributing](22-about/contributing.md) has the full process, including how to report a security problem privately. In short:

1. Follow the [Style Guide](22-about/style-guide.md).
2. Name files in lowercase with hyphens, and list every new page in its folder's `README.md` and in the contents above.
3. Link between pages with relative paths ending in `.md`, for example `../21-reference/glossary.md#haircut`.
4. Before opening a pull request, run the checks:

   ```bash
   python3 .github/scripts/check_docs.py
   ```

   They verify that every link and anchor resolves, that every page has a status line and is listed in its folder's index, and they warn about retired terms. They need only Python 3, and they run on every pull request.

## Review

[`.github/CODEOWNERS`](.github/CODEOWNERS) routes each change to its reviewers. The pages on PXS, distribution, the legal entities and legal text need the owner's approval; chain facts are also checked by the chain maintainer. To make that approval binding, protect `main` with **Require a pull request before merging** and **Require review from Code Owners**.

## Licence

Text published under the [MIT License](LICENSE). The Pixagram® name and logo are not covered by it.
