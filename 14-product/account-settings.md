# Account Settings

> **Status: Live.** Described from the app's code of 2026-10-04 (commit `ca1d157`). One setting, *Preferred Payout*, is stored but has no effect yet.

The app has two kinds of setting that look alike on screen but live in different places. Everything under *Settings* is kept in the browser and never leaves it: language, currency, how artworks are drawn, what is filtered, which node is used. Everything under *Edit profile* is written to the chain, in the account's `posting_json_metadata`, where any program can read it. This page lists both, says where each is stored and what it does, and notes where the app's behaviour differs from what its labels suggest.

## Where settings live

| Kind | Stored in | Travels with | Visible to |
|---|---|---|---|
| **Settings** (the gear) | The browser's local database, LacertaDB, document `main_settings`, one per browser profile ([`settings.js:292-321`][defaults]) | Nothing: another browser or device starts from the defaults | You |
| **Profile** (*Edit profile* on your page) | The chain: the account's `posting_json_metadata`, written with `account_update2` | Every app that reads the chain | Everyone |
| **Keys and session** | The browser, encrypted with your password, until you log out ([Keys and Recovery](../08-guides/keys-and-recovery.md)) | Nothing | You |
| **Notification read marks, favourites, drafts** | The browser, LacertaDB | Nothing | You |

The chain has no concept of a setting. Hive front ends sometimes store preferences in `posting_json_metadata` too; the Pixagram app stores none there.

## Settings

Open them with the gear in the toolbar, or at `https://pixagram.com/+settings`. Each row is one control; the stored key and default are from the code.

### Display

| Control (label) | Choices | Default | Stored as | Effect |
|---|---|---|---|---|
| **Languages** | 51 locale codes, served by 27 language files; a locale without a file falls back to English | The browser's language | `locales` | The app's text. Posts are not translated. |
| **Currency** | 34 currencies | From the locale | `currency` | The currency the wallet converts to, through Frankfurter's rates; PIXA itself has a placeholder price ([Wallet Basics](../08-guides/wallet-basics.md#open-your-wallet)) |
| **Rendering Engine** | Square (`square`), Hexagon (`hexagon`), Retro (`crt`), Painting (`xbrz`), Painting (Fast) (`tri`) | Painting | `renderer` | How pixel art is scaled on screen; the stored image is unchanged |
| **Disable GPU Optimization** | on, off | **on** (`mode: "CPU"`); off stores `GPU` | `mode` | Draws with the processor instead of WebGL. The default is the processor; turning the switch off enables the GPU path. |
| **Download File Format** | PNG, WebP, JPEG | WebP | `format` | The format of a downloaded artwork |
| **PDF Default Page Size** | A4, US Letter | `A4` | `pdf_page_size` | For the wallet's PDF export and printed artworks |

### Content

| Control | Default | Stored as | Effect |
|---|---|---|---|
| **Don't filter NSFW content** | off: "NSFW content is hidden" | `nsfw_filter` (true while filtering) | On, artworks marked NSFW appear in feeds and profiles, blurred. |
| **Don't blur NSFW content** | off: "NSFW content shows blurred" | `nsfw_enabled` | On, shown NSFW artworks are not blurred. Turning it on asks you to confirm "I am 18 or older" ([`SettingsDialog.js:282-290, 672-692`][nsfw]). While blurring is on, an on-device model also blurs unflagged artworks it rates likely NSFW ([Censorship Resilience and Moderation](../02-social-layer/censorship-resilience-and-moderation.md#what-the-pixagram-app-and-the-indexer-do)) |
| **Toxic Comment Helper** | on: "Kindly flags harsh wording while you type" | `toxicity_enabled` | An on-device model underlines harsh wording in a comment before you post. It blocks nothing. |

The panel says of both models: they "run on tiny AI models that work fully offline … No data is ever sent to a server". The models are loaded with the app and run in the browser; the search box is the one feature that sends your text to a service ([Search](search.md)).

### Posting and voting

| Control | Choices | Default | Stored as | Effect |
|---|---|---|---|---|
| **Preferred Payout** | Renounced, Balanced, Sovereign | Balanced (`share`) | `payout` (`decline`, `share`, `power`) | **None today.** The value is saved and read back by the dialog, and nothing else reads it; a post's payout options are set in the post editor's own panel ([Posting and Rewards](../02-social-layer/posting-and-rewards.md)) |
| **Licensing** | Configure or reset a default licence | None: "new posts start from the standard Pixa NFT License terms" | `default_license` | The starting terms the editor shows for a new post; the licence itself goes into the post's `json_metadata` only when you publish ([Artwork Encoding Spec](../09-developers/artwork-encoding-spec.md#the-licence-record)) |
| **Voting Power** | 1% to 100% | 100 | `voting` | The weight of a vote cast by clicking the heart |
| **Always ask before voting** | on, off | off | `askvote` | On, every vote opens a dialog to choose the weight first |

### Endpoint

The *Endpoint* section lists the six public nodes with their measured latency and lets you set a custom one ("Set custom endpoint", "Type a URL, then press Enter or the check to switch to it").

| Behaviour | Detail |
|---|---|
| Default | `api.pixagram.com`. On first start, while no node has been chosen, the app times all six and keeps the fastest that answers ([`settings.js:330-372`][race]). |
| The six | `api.pixagram.com`, `pixarex.net`, `merlion.surf`, `blockforge.lol`, `boitata.quest`, `pixa-dubai.xyz` ([`constants.js:94-137`][nodes]; [JSON-RPC Surface](../12-api-reference/json-rpc.md#endpoints)) |
| Custom | Any HTTPS address; it must run the same gateway or the app's field names fail ([Differences from Hive](../09-developers/differences-from-hive.md#talking-to-hived-directly)) |
| Stored as | `api_node_url` and `api_node_source` |

There is no theme setting.

## Your profile

*Edit profile*, on your own page, writes the `profile` object of your `posting_json_metadata` ([`EditProfileDialog.js:583-594, 960-986`][profile]; [Data Model](../11-protocol-reference/data-model.md#application-only-what-the-pixagram-app-defines)):

| Field on screen | Stored key | Rule in the app | What Hivemind serves of it |
|---|---|---|---|
| Display name | `profile.name` | free text | The first 20 characters |
| Biography | `profile.about` | free text | 160 characters |
| Location | `profile.location` | free text | 30 |
| Website | `profile.website` | a valid URL | Up to 100 characters; longer, nothing |
| Profile picture | `profile.profile_image` | A pixel-art file of at most 48,000 bytes, stored **inside the metadata** as a data URI, not uploaded anywhere ([`EditProfileDialog.js:773`][avatar]) | **Nothing.** Hivemind keeps a picture only when it is an `http(s)://` address of at most 1,024 characters, so `bridge.get_profile` returns an empty `profile_image` for every Pixagram account; the app reads the picture from `condenser_api.get_accounts` instead ([`extract_profile_metadata.sql:110-115`][hm-profile]) |
| Addresses, links, contacts | `profile.addresses`, `profile.links`, `profile.contacts` | lists of name and value pairs | Pixagram-only keys; other apps ignore them |

What the operation does and costs:

- **One `account_update2` operation**, which merges the new `profile` into the existing `posting_json_metadata` so other keys survive, and re-sends the account's `json_metadata` unchanged ([`pixaproxyapi.js:5549-5590`][update-profile]).
- **It asks for your active key**, although the dialog first checks that your posting key is unlocked ([`EditProfileDialog.js:925-931`][unlock]). The reason is the re-sent `json_metadata`: an `account_update2` that carries `json_metadata` needs the active authority, while one that carries only `posting_json_metadata` needs posting ([Operations Reference](../11-protocol-reference/operations-reference.md#accounts-and-keys)). Leaving `json_metadata` out would let the profile be saved with the posting key.
- **It is public and permanent.** Every version of the profile stays in the block log. Do not put a phone number or an address you would not print.
- **No cover image.** The dialog has no field for one, and the app shows none.
- **Resource Credits:** the operation's size, which the picture dominates: a 48,000-byte picture is about 64,000 bytes once encoded as a data URI, the largest routine operation an account sends after an artwork ([Resource Credits](../04-tokens-and-economy/resource-credits.md)).

Other apps that read Hive profiles through Hivemind (`name`, `about`, `location`, `website`, `profile_image`) will show a Pixagram profile cut to Hivemind's lengths and without its picture; an app that reads `posting_json_metadata` from hived gets everything, with a data-URI picture it may or may not render.

## What the chain, the indexer and the app each decide

| Behaviour | Chain | Indexer | App |
|---|---|---|---|
| Profile fields' existence and content | yes, as metadata | | |
| Profile length limits, and the dropped picture | | yes, when serving | |
| Which key saves a profile | yes, by what the operation carries | | yes, by what it sends |
| Every setting under the gear | | | yes, per browser |
| NSFW filtering and the on-device models | | | yes |

## Inherited → changed

| | Hive front ends | Pixagram |
|---|---|---|
| Profile storage | `posting_json_metadata.profile` | the same keys, plus `addresses`, `links`, `contacts` |
| Profile picture | a URL | a data URI of pixel art, at most 48,000 bytes |
| Cover image | `profile.cover_image` | none |
| Preferences on chain | some front ends keep them in `posting_json_metadata` | none; all in the browser |
| NSFW setting | per user, often in the profile | per browser |

## Sources

- **App** at commit [`ca1d157`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52): defaults and storage, [`utils/settings.js:292-321`][defaults]; the node race, [`settings.js:330-372`][race]; the node list, [`constants.js:94-137`][nodes]; currencies and locales, [`constants.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js) and [`locales/`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales); the dialog, [`SettingsDialog.js`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/SettingsDialog.js); how the voting settings reach the API, [`Index.js:1588-1589`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/pages/Index.js#L1588-L1589); the profile dialog, [`EditProfileDialog.js`][profile]; the broadcast, [`pixaproxyapi.js:5494-5590`][update-profile]; English text, [`en.js:2622-2669`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L2622-L2669).
- **Hivemind** at commit [`5765e21`](https://github.com/pixagram-blockchain/hivemind/tree/5765e2113da3c2c3da3c056d7d795c51e925711a): profile field limits in [`hive/utils/account.py:80-89`](https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/utils/account.py#L80-L89) and [`extract_profile_metadata.sql:50-115`][hm-profile]; checked live with `bridge.get_profile` against `condenser_api.get_accounts` on 2026-10-08.
- **Chain:** the authority `account_update2` requires, [`hive_operations.hpp:74-110` at `48f75a2`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/include/hive/protocol/hive_operations.hpp#L74-L110).

[defaults]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/settings.js#L292-L321
[race]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/settings.js#L330-L372
[nodes]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L94-L137
[profile]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditProfileDialog.js#L583-L594
[avatar]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditProfileDialog.js#L773
[unlock]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditProfileDialog.js#L925-L931
[update-profile]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L5494-L5590
[nsfw]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/SettingsDialog.js#L672-L692
[hm-profile]: https://github.com/pixagram-blockchain/hivemind/blob/5765e2113da3c2c3da3c056d7d795c51e925711a/hive/db/sql_scripts/postgrest/utilities/extract_profile_metadata.sql#L50-L115
