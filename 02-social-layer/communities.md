# Communities

> **Status: Live.** 12 communities existed on 2026-10-05. Checked against the indexer at commit `5765e21` and the app at commit `ca1d157`.

A community is a shared space with its own name, rules and moderators. Members publish blog posts there and discuss them. Communities are not part of consensus. They are run by Hivemind, the social indexer behind the public API, which reads community actions from the chain and applies the community's rules when it serves posts.

## What a community is

**A community is an ordinary account** whose name follows a fixed pattern: `portal-`, then a digit for its initial type, then four to six more digits, for example `portal-156480`. Numbered names prevent squatting, and several communities may share a title. Like any account, a community can hold tokens and sign operations; its keys belong to whoever created it.

Posts join a community by naming it as their category. Every action in a community is a `custom_json` operation with the id `community`, signed with a posting key. Hivemind reads these operations and keeps each community's state.

## Types

| Type | Digit after `portal-` | Who may post | Who may comment |
|---|---|---|---|
| Topic | 1 | Anyone not muted | Anyone not muted |
| Journal | 2 | Members and above | Anyone not muted |
| Council | 3 | Members and above | Members and above |

A post that breaks its community's rules is indexed as muted, and so are replies beneath it. On 2026-10-05 every community was a topic.

## Roles

| Role | What it can do |
|---|---|
| Owner | The community account itself. It appoints the first admins, and its role cannot be changed. |
| Admin | Everything a moderator can, plus editing the community's title, description, rules and settings |
| Moderator | Mute and unmute posts; pin and unpin posts; set roles below their own; give members a title |
| Member | Post in journals and councils |
| Guest | The default role of everyone else |
| Muted | Their posts are shown greyed out, and they cannot flag |

No one can grant a role equal to or above their own. At most 100 accounts in a community can hold moderator rank or above.

## Moderation

Moderators act on the community's own feed, not on the chain:

- **Muting a post** marks it as muted. The Pixagram app shows muted blog posts dimmed until you hover over them. The post remains on chain and in its author's profile.
- **Pinning a post** keeps it at the top of the community's feed.
- **Flagging** lets any non-muted user alert the moderators to a post. Hivemind supports flags, but the app cannot send them yet.

Every mute, unmute and flag must carry a note of 1 to 120 characters. Muting a user, and member titles, exist in Hivemind but are not yet offered by the app. See [Censorship Resilience and Moderation](censorship-resilience-and-moderation.md) for how this fits with what the chain itself guarantees.

## Settings and their limits

| Setting | Limit |
|---|---|
| Title | 3 to 20 characters; may not start with `@` or `#` |
| About | up to 120 characters |
| Description, flag text | up to 1,000 characters each |
| Language | a two-letter ISO 639-1 code |
| Member title | up to 32 characters |
| Avatar and cover | `http(s)` addresses under 1,024 characters |

An update with an unknown setting or an untrimmed string is rejected in full.

## Creating a community

The app's profile page has a button to create a community. It:

1. Asks for the type, title, description and language, and generates a name of the form `portal-<type><5 digits>`.
2. Generates a new 24-word recovery phrase for the community account and offers it as a PDF. **Whoever holds this PDF controls the community account.**
3. Opens the account from your wallet. You pay the chain's account creation fee: 20.000 PIXA on 2026-10-05 (`condenser_api.get_chain_properties`), which is burned.
4. Optionally lends the new account Pixa Power: 50 by default, so it has Resource Credits.
5. Makes you an admin, subscribes you, and publishes the community's settings.

In the app, changing the settings later needs the community account's own keys, which is why the PDF matters. Step by step: [Create a Community](../08-guides/create-a-community.md). Hivemind itself accepts new settings, including a new type, from any admin.

## Rewards

Communities earn nothing by default. Posts in a community pay their authors and curators like any other post. The app's "default beneficiary" setting is not applied yet, so no share of a community's posts goes to the community account.

## The communities today

On 2026-10-05 there were 12 communities:

- **Nine official portals:** Proposals (`portal-156480`), Governance, Development, Security, Risks, Legal, Marketing, Discussions and Bugs.
- **Three created by other accounts:** MES Science, Human's Rights and Pixagram R&D.

Most had a single subscriber: their creator. Read the current list with:

```bash
curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"bridge.list_communities","params":{"limit":100},"id":1}'
```

The app has proposals to the [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md) written as blog posts in the Proposals portal.

## Inherited → changed

| | Hive | Pixa |
|---|---|---|
| Name pattern | `hive-` + digits | `portal-` + digits |
| Types, roles, operations, limits | as above | unchanged |
| Indexer | Hivemind | Hivemind, with configurable token names |

## Sources

- **Hivemind**, commit [`5765e21`](https://github.com/pixagram-blockchain/hivemind/tree/5765e2113da3c2c3da3c056d7d795c51e925711a):
  - roles and types: [`community.py:22-36`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/indexer/community.py#L22-L36); the name pattern: [`community.py:119-129`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/indexer/community.py#L119-L129)
  - who may post: [`hive_post_operations.sql:51-100`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/db/sql_scripts/hive_post_operations.sql#L51-L100)
  - settings, which only admins may change: [`community.sql:476-512`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/db/sql_scripts/community.sql#L476-L512)
- **App**: [`CreateCommunityDialog.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateCommunityDialog.js), [`Community.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/pages/Community.js).
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §V.3 "Communities".
- **Live chain**: `bridge.list_communities`, read on 2026-10-05.
