# Take Part in Governance

> **Status: Live.** Votes for witnesses and for fund proposals are weighted by Pixa Power. Described from the app's code of 2026-10-04. Last checked 2026-10-06.

Stakeholders elect the witnesses who produce blocks, and decide which proposals the Decentralized Pixa Fund pays. This guide shows how to vote for both in the app, how to name a proxy and how to submit a proposal. How the votes are counted is on [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md) and [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md).

## Before you start

- **Your weight is your Pixa Power.** Stake you power up counts for these votes after 30 days. Your votes and your proxy are cleared after 365 days without a vote or a change of proxy ([how witnesses are elected](../07-governance/witnesses-and-dpos.md#how-witnesses-are-elected)).
- **Every vote needs your active key.** If your session does not hold it, the app asks for it.

## Open Governance

Click **Governance** in the toolbar. On a small screen, it is in the ⋮ menu. Governance opens on the proposals.

Its four tabs are icons: **Viability Management**, **Attributes**, **Methods** and **Disruptions**. Viability Management has three sections, also icons: the proposals, the witness vote and the tokenomics. Each has its own address, and the part from `+` on works after the address of any page but the home page:

| Section | Address |
|---|---|
| Proposals | [pixagram.com/created/+governance-viability-proposals](https://pixagram.com/created/+governance-viability-proposals) |
| Witness vote | [pixagram.com/created/+governance-viability-vote](https://pixagram.com/created/+governance-viability-vote) |
| Tokenomics | [pixagram.com/created/+governance-viability-tokenomics](https://pixagram.com/created/+governance-viability-tokenomics) |
| Attributes | [pixagram.com/created/+governance-attributes](https://pixagram.com/created/+governance-attributes) |
| Methods | [pixagram.com/created/+governance-methods](https://pixagram.com/created/+governance-methods) |
| Disruptions | [pixagram.com/created/+governance-disruptions](https://pixagram.com/created/+governance-disruptions) |

## Vote for witnesses

1. Open the [witness vote](https://pixagram.com/created/+governance-viability-vote).
2. Under **Top Witnesses**, each row shows a witness, the version it runs, its votes, its last block, its missed blocks and the price feed it publishes.
3. Tick the box in the **Voted** column to vote for a witness. Untick it to withdraw your vote.
4. To vote for a witness that is not in the table, type its name under "@username" and click **Vote For Account**.

You can vote for up to 30 witnesses, and each vote carries your full weight. If a box flips back, the vote did not go through: check that you have not named a proxy, then try again. The app cannot withdraw a vote for a witness that is not in the table; any Hive-compatible library can ([how to vote](../07-governance/witnesses-and-dpos.md#how-to-vote)).

## Name a proxy

A proxy votes for you on witnesses and on proposals, with your weight. Naming one replaces your own witness votes. While a proxy is set, the chain refuses your own witness votes and ignores your proposal votes, and the app cannot remove it: name one only if you can clear it later with a library.

1. In the witness vote, type the account under "@username".
2. Click **Delegate My Vote**.

The app does not show your current proxy and cannot remove it. To remove it, broadcast `account_witness_proxy` with an empty proxy from any Hive-compatible library ([how to vote](../07-governance/witnesses-and-dpos.md#how-to-vote)).

## Vote on proposals

1. Open the [proposals](https://pixagram.com/created/+governance-viability-proposals). The **DAO Treasury** box shows the fund's daily budget and how much of it goes to proposals now.
2. Below it are the active proposals, then the return proposal under "Active Proposal's Dynamic Threshold", then the pending ones.
3. Open a proposal to read it: what it requests in total, its **Daily Pay** and the days left. **View Proposal** opens its post.
4. Tick **Vote** to support it, and untick it to withdraw your support. Each click votes on one proposal.

The fund pays proposals in order of their votes, as far as its daily budget goes, and pays nothing to a proposal with fewer votes than the return proposal ([how it pays](../07-governance/decentralized-pixa-fund.md#how-it-pays)). A vote for the return proposal raises that bar for all of them. The app's "Paid Out" and "Remaining" figures are estimates from the dates and the daily pay, not payments read from the chain.

## Submit a proposal

A proposal asks the fund for a daily amount of PXS between two dates. In the app, it is a post in the Proposals portal and a request on the chain, made one after the other.

1. In the proposals, click **Create Proposal**. The editor opens in the Proposals portal, `portal-156480`.
2. Write the title, a short description and the text. The short description becomes the proposal's subject: the chain allows 80 bytes, and accented or non-Latin letters take two or more each, so keep such a description under 40 characters.
3. In the settings, tick **This is a proposal**.
4. Set the dates under **Start – End**, starting today or later, and the **Daily pay**, in PXS.
5. Check the summary: the duration, the daily and total payouts, and the **Total fee**, which is 10 PXS plus 1 PXS for each day beyond 60. The fee is taken from your PXS balance, which must already cover it, and goes into the fund.
6. Click **Preview**, then **Publish**.
7. Wait for "Proposal submitted successfully!" The app publishes the post with your posting key, then creates the proposal with your active key.

- **The proposal pays your own account.** The app has no field for another receiver.
- **"Post published, but proposal failed: …"**, or "Post published, but the proposal submission failed.", means the post is up but there is no proposal yet. You can create it directly from its post ([Proposing](../07-governance/decentralized-pixa-fund.md#proposing)).
- **Later changes.** Editing the post updates the proposal. The daily pay can be lowered but never raised, the start date is fixed, and the end date can only move earlier. Deleting the post removes the proposal.

## Discuss and report

The **Disruptions** tab lists the official portals: Proposals, Discussion, Governance, Marketing, Legal, Risks, Security, Bug Reports and Development. Each opens its community page, where proposals and problems are discussed in public.

**Never report a security problem in a portal.** Report it privately ([Contributing](../22-about/contributing.md#report-a-security-problem)).

## The other sections

- **Tokenomics** shows the token generation event and the allocation ledger, checked against live balances ([Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md)).
- **Attributes** shows the chain's status, network figures and the latest blocks.
- **Methods** lists guides, as PDFs and videos.

## Sources

- **Governance:** the tabs, [`GovernanceDialog.js:45-88`][gd]; the sections, [`GDViabilityManagement.js:18-31`][gdvm]; the addresses, [`constants.js:848-879`][const-848]; the portals, [`constants.js:595-620`][const-595].
- **Witness votes and proxy:** [`GDVMWitnesses.js:922-954`][wit-922] and [`GDVMWitnesses.js:1660-1711`][wit-1660]; the operations, [`pixaproxyapi.js:6512-6548`][api-6512].
- **Proposals:** voting, [`GDVMProposals.js:1029-1042`][prop-1029]; the fee, [`SettingsPanel.js:29-36`][fee]; the proposal fields, [`SettingsPanel.js:425-483`][fields]; publishing and creating the proposal, [`LexicalTextEditorDialog.js:1617-1752`][lex]; the operation, [`pixaproxyapi.js:7035-7056`][api-7035].
- **Disruptions:** [`GDDisruptions.js:154-272`][dis].
- **English text:** [`en.js:1151-1168`][en-1151], [`en.js:150-164`][en-1104], [`en.js:1002-1016`][en-1002] and [`en.js:1331-1347`][en-1331].
- **Chain:** the rules for votes, proxies and expiry, [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md#sources); proposals and the fee, [Chain Parameters](../21-reference/chain-parameters.md#decentralized-pixa-fund-dpf).

[gd]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/GovernanceDialog.js#L45-L88
[gdvm]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/GDViabilityManagement.js#L18-L31
[const-848]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L848-L879
[const-595]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L595-L620
[wit-922]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/GDVMWitnesses.js#L922-L954
[wit-1660]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/GDVMWitnesses.js#L1660-L1711
[api-6512]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L6512-L6548
[prop-1029]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/GDVMProposals.js#L1029-L1042
[fee]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/editor/SettingsPanel.js#L29-L36
[fields]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/editor/SettingsPanel.js#L425-L483
[lex]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/editor/LexicalTextEditorDialog.js#L1617-L1752
[api-7035]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L7035-L7056
[dis]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/GDDisruptions.js#L154-L272
[en-1151]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1151-L1168
[en-1104]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L150-L164
[en-1002]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1002-L1016
[en-1331]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1331-L1347
