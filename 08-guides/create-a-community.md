# Create a Community

> **Status: Live.** Creating a community costs the account creation fee, 20.000 PIXA on 2026-10-05, which is burned. Described from the app's code of 2026-10-04. Last checked 2026-10-06.

A community, which the app calls a portal, is an account of its own, with a feed, rules and a team. This guide creates one, sets it up and runs it. How communities work on the chain is on [Communities](../02-social-layer/communities.md).

## Before you start

- **A computer.** The button that creates a portal, and the one that adds team members, appear only in the app's desktop layout.
- **PIXA for the fee.** It is the chain's account creation fee, paid from your PIXA and burned: 20.000 PIXA on 2026-10-05 (`condenser_api.get_chain_properties`). The app shows the current fee before you create.
- **Pixa Power to lend, if you have some.** The app lends the new portal 50 Pixa Power by default, so that it has Resource Credits. You can lend less, or none.
- **A safe place for a second PDF,** with the portal's own keys.

## 1. Start

Open your profile. In your list of portals, click **Create new portal**.

## 2. Describe the portal

1. **Portal Title:** 3 to 20 characters, not starting with `@` or `#`.
2. **About:** 10 to 120 characters.
3. **Portal Type:**

   | Type | In the app's words |
   |---|---|
   | Topic | "Anyone can post or comment" |
   | Journal | "Only members can post and guests can only comment" |
   | Council | "Only members can post or comment" |

4. **Language.**
5. Check the **Creation Fee**, then click **NEXT**.

## 3. Save the portal's keys

1. **Check the name.** The app proposes `portal-`, a digit for the type (1 for a topic, 2 for a journal, 3 for a council), then five random digits. You can edit it or draw another. The name is permanent.
2. **Choose the delegation:** the Pixa Power you lend the portal, 50 by default.
3. **Click DOWNLOAD CREDENTIALS** and save `KeysOf-portal-…-Pixagram.pdf`. It holds the portal's 24-word recovery phrase, its master key and its four private keys.

   **Whoever holds this PDF controls the portal.** Keep it as carefully as your own.

   **Every download makes new keys.** Only the last PDF you download will match the portal. Changing the name or the type also discards the keys, so download again after any change.
4. **Open the PDF before you continue.** Check that it names the portal and shows its phrase. "I have securely saved the portal credentials" ticks itself when the download starts, not when the file is saved: if nothing was saved, click **RE-DOWNLOAD CREDENTIALS** and keep only the new PDF.
5. **Click CREATE PORTAL.** **You cannot undo this:** the fee is burned.

The app now works through four steps: "Creating portal", "Delegating PXP to portal", "Setting portal's configuration" and "Waiting for the portal index". It opens the account with your active key, lends it the Pixa Power, makes you its admin, subscribes you, and publishes the title, description and language. Then it opens the portal's page, `pixagram.com/portal-…`, with the message 'Portal "…" created successfully!'

If an error appears after the first step, the portal account exists already. Keep the PDF: logged in as the portal with its posting key, you can finish with the pencil and **Add someone**.

**Default Beneficiary**, under the advanced options, has no effect yet ([Rewards](../02-social-layer/communities.md#rewards)).

## Edit the settings

1. On the portal's page, click the pencil on its picture. Only admins see it.
2. Change what you need:
   - **Title** and **About**, with the limits above;
   - **Rules**, one per line, up to 100 rules and 1,000 characters in all;
   - **Language** and **NSFW**;
   - **Flag / Report Text**, up to 1,000 characters;
   - **the picture,** which must be pixel art under 48 kB.
3. Click **Save Changes.** The app asks for the portal's keys from the PDF: the posting key for the settings, the active key for the picture. It uses them for this change only and does not store them.

## Build a team

| Role | What it can do |
|---|---|
| Owner | The portal account itself. It appoints the admins. |
| Admin | Edit the settings and appoint moderators |
| Moderator | Pin and mute posts |

The full list of roles is on [Communities](../02-social-layer/communities.md#roles). No one can give a role equal to or above their own.

- **To add a moderator,** click **Add someone** in the portal's sidebar, search for the account, choose **Mod**, and confirm. It is signed with your own posting key.
- **To add an admin,** log in as the portal with the posting key from its PDF, use **Add someone** with **Admin**, then [log out](keys-and-recovery.md#log-out). As the portal's creator, you are an admin, and an admin cannot appoint another.

The app cannot yet give member titles, mute accounts, make someone a member or remove a role. Any Hive-compatible library can send these community operations ([Communities](../02-social-layer/communities.md)).

## Post in your community

1. On the portal's page, click the pen button. The text editor opens with this portal chosen, at `pixagram.com/portal-…/editor`.
2. Write the post.
3. Click **Preview**, then **Publish**.

Posts in a community are text posts; artworks are published with their tags ([Publish Your First Artwork](publish-your-first-artwork.md)).

## Moderate

In a post's ⋮ menu on the portal's page, moderators and admins see:

- **Pin Post** and **Unpin Post**, which keep a post at the top of the portal's feed or release it;
- **Mute Post** and **Unmute Post**, which ask for a reason. Always give one, up to 120 characters, although the field says optional: the community index ignores a mute without a note. Write "spam" for spam. The app shows a muted post dimmed in the portal's feed until someone points at it, and the post stays on the chain and in its author's profile.

## Leave

**Leave community**, among the portal's buttons, unsubscribes you. It does not remove your role.

## Sources

- **Creating a portal:** [`CreateCommunityDialog.js`][ccd]; the fields and their limits, [`CreateCommunityDialog.js:614-647`][ccd-614]; the name, [`CreateCommunityDialog.js:477-574`][ccd-477]; the keys and the PDF, [`CreateCommunityDialog.js:527-554`][ccd-527]; what is broadcast, [`CreateCommunityDialog.js:671-938`][ccd-671].
- **Editing:** [`EditCommunityDialog.js`][ecd]; rules, [`community-rules.js:31-133`][rules].
- **Team and moderation:** [`AddSomeoneCommunityDialog.js`][add]; pinning and muting, [`PaperCardMenuOption.js:336-372`][menu] and [`Community.js:1925-1952`][mute]; the operations, [`pixaproxyapi.js:9080-9263`][api-9080].
- **Posting:** [`Community.js:1786-1791`][post].
- **English text:** [`en.js:585-619`][en-585], [`en.js:690-732`][en-690] and [`en.js:302-310`][en-302].
- **Rules of the community index:** [Communities](../02-social-layer/communities.md#sources).

[ccd]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateCommunityDialog.js
[ccd-614]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateCommunityDialog.js#L614-L647
[ccd-477]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateCommunityDialog.js#L477-L574
[ccd-527]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateCommunityDialog.js#L527-L554
[ccd-671]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateCommunityDialog.js#L671-L938
[ecd]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/EditCommunityDialog.js
[rules]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/community-rules.js#L31-L133
[add]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/AddSomeoneCommunityDialog.js
[menu]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PaperCardMenuOption.js#L336-L372
[mute]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/pages/Community.js#L1925-L1952
[api-9080]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L9080-L9263
[post]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/pages/Community.js#L1786-L1791
[en-585]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L585-L619
[en-690]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L690-L732
[en-302]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L302-L310
