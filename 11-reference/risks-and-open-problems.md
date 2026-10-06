# Risks and Open Problems

> **Status: Live.** A register of the known risks to the network and of the problems its design leaves open, with the state of each on 2026-10-06. It changes when a risk does.

This page lists what could go wrong, how far each risk has gone, and what limits it, with a link to the page that explains it. Security vulnerabilities are handled under the [Style Guide's disclosure rule](../13-about/style-guide.md#security-and-disclosure): reported privately, and documented once fixed.

## PXS and the economy

PXS promises no price: nothing defends it, and no one owes its holder anything. The rows below are risks in the mechanism that converts it into PIXA, and in the economy that mechanism rests on.

| Risk | What could happen | Where it stands | What limits it | Details |
|---|---|---|---|---|
| What a PXS delivers can fall | Conversions settle 3.5 days after the request, at the median less the haircut, which falls toward zero below a collateral ratio of 7/3. No market exists for PXS or PIXA, so a holder may find no buyer. | Printing on, no haircut, no orders and no trades (2026-10-06) | Nothing defends it | [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#the-haircut) |
| The feed is a placeholder | Every collateral ratio and threshold distance is computed from an assumed PIXA price. If PIXA comes to trade, its first market price may differ from the placeholder by any factor. | All 84 samples at 51.833 PIXA per PXS, from 6.22 USD ÷ 0.12 USD (2026-10-06) | Nothing: the medians delay a switch by about two days but do not soften it | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#the-placeholder) |
| The treasury holds almost all PXS | PXS paid out of the treasury enters the debt ratio. If all of it were outside, the collateral ratio would be about 7.7 instead of about 804. | 249,266.219 PXS, 99.04% of all PXS (2026-10-06) | At most 1% of the fund a day, and only to proposals that stakeholders approve | [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#where-the-network-stands) |
| The Big Mac reference | One good stands for purchasing power. Its price differs by country, changes in steps when The Economist publishes a new edition, and depends on a third party continuing to publish. Local prices that witnesses declare cannot be checked on chain. | Every feed uses the US price of the July 2026 edition | The median across witnesses; the reference can be changed in the feed software | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#the-agnostic-feed) |
| The design and the chain disagree | Readers of the design notes expect a corridor of 3 to 10, 21 witnesses and a basket; the chain enforces other thresholds, elects up to 21 witnesses with 1 required, and reads one good | Thresholds unchanged since genesis; 9 witnesses on 2026-10-06 | Every PXS page states the chain's numbers | [PXS at a Glance](../05-pixa-supra/pxs-at-a-glance.md#where-the-design-and-the-chain-differ) |
| Words that promise | Words that imply a peg or a stable value would invite reliance on a promise that does not exist | — | The wording rules | [Style Guide](../13-about/style-guide.md#writing-about-pxs) <!-- retired-ok --> |
| Sustainability of rewards and the fund | Issuance funds rewards, witnesses and the fund. If the network does not grow, it dilutes holders without drawing new participants; the fund shrinks while it pays more than it receives. | Rate 9.75% a year, about 11.3% in PIXA-equivalent terms while 9 witnesses run; the fund shrinks by about 52 PXS a day while proposal 1 runs (2026-10-05) | The rate falls by 0.01 percentage points every 250,000 blocks; more witnesses lower the witness part; proposals need votes | [Supply, Inflation and Yield](../04-tokens-and-economy/supply-inflation-and-yield.md), [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md#proposals-on-2026-10-05) |
| Distribution of the allocations | Most stake has yet to reach users. How it reaches the market shapes PIXA's market value, and with it every PXS ratio. | 72.31% of stake in `pixa.rex` and `pixa.team` (2026-10-05) | The allocation accounts cannot vote; `pixa.rex` is to be distributed within 9 to 11 years of the TGE, a commitment the protocol does not enforce | [Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md#what-the-operator-has-committed-to) |

## Governance

| Risk | What could happen | Where it stands | What limits it | Details |
|---|---|---|---|---|
| Few voters | A handful of accounts elects every witness and sets the fund's threshold | 6 accounts voted for witnesses, and the five largest holders held 93.06% of the stake outside the allocations (2026-10-05) | The 30-day delay on new stake; votes expire after a year; the allocations cannot vote | [Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md#the-figures-on-2026-10-05) |

## Technology

| Risk | What could happen | Where it stands | What limits it | Details |
|---|---|---|---|---|
| Dependence on Hive's code | Pixa must carry its own changes forward onto each new Hive release, or fall behind its fixes | Built on hived 1.28.7, now 1.29.0 with hardfork 29 | A short, documented list of Pixa changes | [Differences from Hive](../09-developers/differences-from-hive.md), [Protocol Upgrades](../07-governance/protocol-upgrades.md) |
| Tools that age | Libraries and services lag behind the chain or carry quirks | `@pixagram/dpixa` 1.5.4 needs workarounds; the public gateway rewrites some field names inside post text | Documented workarounds | [SDKs and Libraries](../09-developers/sdks-and-libraries.md#quirks-in-154), [Differences from Hive](../09-developers/differences-from-hive.md#known-issue-renames-inside-text) |
| Storage that only grows | Every artwork stays in the block log for good, so a full node's disk keeps growing | Artwork posts had a median body of about 26 kB in the first month; the largest was 497,479 bytes | Resource Credits price every byte; the block size is a witness vote | [Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md#how-large-an-artwork-can-be), [Run a Node](../10-node-operators/run-a-node.md#what-the-node-keeps) |
| Content that cannot be removed | Data published by mistake, personal data, or content unlawful somewhere stays in the history every full node keeps | — | Apps and indexers can hide content; the record cannot change | [Censorship Resilience and Moderation](../02-social-layer/censorship-resilience-and-moderation.md#what-the-chain-does-not-do), [Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md#permanence) |
| No account recovery yet | A stolen owner key cannot be recovered | Possible from about 2026-12-24 (block 3,186,477) | Keep the owner key offline | [Chain Parameters](chain-parameters.md#accounts-and-keys) |
| No testnet | Every test transaction is real and permanent | — | Test with a small account | [Developer Quickstart](../09-developers/developer-quickstart.md#before-you-start) |

## Product and growth

| Risk | What could happen | Where it stands | What limits it | Details |
|---|---|---|---|---|
| A narrow medium | Pixel art draws a smaller audience than photography or video | 141 artworks published in the first month (2026-09-04 to 2026-10-04) | Blog posts and communities widen what members can publish | [Pixel Art On Chain](../03-art-on-chain/pixel-art-on-chain.md#why-pixel-art) |
| The network effect | A young network has few readers, so few rewards, so few reasons to join | 85 accounts (`condenser_api.get_account_count`, 2026-10-06); 21 accounts with votes large enough to move rewards (2026-10-05) | Free sign-up; stake reaches authors through rewards | [Voting and Curation](../02-social-layer/voting-and-curation.md#why-small-votes-count-for-nothing), [Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md) |
| The marketplace is not built | Selling artworks, the project's stated aim, is not yet possible on chain | Planned for 2027 | — | [NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md#open-questions) |
| Dependence on the operator | The app, the account service and free sign-up rest on one operator, Pixa Rex S.A. | Sign-up is funded by a fund proposal until 2026-12-31 | The chain does not depend on the app; anyone can run a node or another app | [Who Does What](../01-start-here/who-does-what.md), [Roadmap](../01-start-here/roadmap.md) |

## Legal and regulatory

| Risk | What could happen | Where it stands | What limits it | Details |
|---|---|---|---|---|
| Changing rules on crypto-assets | Regulators may classify PIXA, Pixa Power or PXS differently from one another, and differently by jurisdiction; rules such as the EU's MiCA regulation continue to develop | These pages state no legal classification | — | The Regulatory Status page (planned) will hold the approved text; [Style Guide](../13-about/style-guide.md#tokens-rewards-and-money) |

## Open problems

| Problem | Why it is open | Where it is discussed |
|---|---|---|
| Leaving the placeholder | Whether and when witnesses switch to market prices, and how the network absorbs the jump in every ratio, is not decided | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#the-placeholder) |
| Independent feeds | The agnostic feed lets each witness report its own local price from its own markets; no witness runs it yet | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#the-agnostic-feed) |
| A basket beyond the Big Mac | The design notes name a coffee as well; nothing reads it, and nothing says who would decide | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#the-agnostic-feed) |
| Design and chain thresholds | Either a hardfork brings the corridor into the code, or the design adopts the chain's thresholds | [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#corridor-and-thresholds-design-and-chain) |
| The treasury and the debt ratio | How PXS paid out by the fund should be planned against the print stop and the haircut | [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#where-the-network-stands) |
| Measuring the Atlas | The chain counts PIXA and values PXS against it at the median; it cannot see how much a market would absorb | [The Four Components](../05-pixa-supra/the-four-components.md#atlas-the-collateral-base) |
| What a sale settles in | Whether the marketplace settles in PIXA, PXS or both | [NFTs and Marketplace](../03-art-on-chain/nfts-and-marketplace.md#open-questions) |
| Who pays for history | Full nodes keep every artwork forever; nothing pays them for it directly | [Run an API Node](../10-node-operators/run-an-api-node.md#size-the-server) |
| Spreading stake and witnesses | The protocol separates powers; distributing stake, adding witnesses and finding voters is work outside it | [Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md#what-should-change-the-figures) |

## Sources

Each row links to the page that sources its figures. Figures dated 2026-10-06 were read at block 917,250 with `condenser_api.get_dynamic_global_properties`, `condenser_api.get_feed_history`, `condenser_api.get_accounts`, `condenser_api.get_order_book` and `condenser_api.get_account_count`.
