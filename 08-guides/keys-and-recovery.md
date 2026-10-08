# Keys and Recovery

> **Status: Live.** Account recovery on the chain works since hardfork 30 (2026-10-07) for owner-key changes made after it, and the app has no screen to run one. Described from the app's code of 2026-10-04. Last checked 2026-10-08.

Your account is controlled by keys that only you hold. No one at Pixagram can reset them. This guide shows where your keys come from, which one does what, how the app keeps them, and what to do when one is lost or seen by someone else. The terms are defined under [Keys](../21-reference/glossary.md#keys) in the Glossary.

## Where your keys come from

- **Your recovery phrase** has 12 to 24 words, 18 by default. With the password you may have added at sign-up, it makes your **master key**.
- **Your master key** makes your four keys: owner, active, posting and memo. Each has a public half, which starts with `PIX` and is recorded on the chain, and a private half, which only you hold.
- **Your backup PDF** holds all of them. The app never stores the phrase, so the PDF is the only place it is written down.

| Key | What the app uses it for | Where to keep it |
|---|---|---|
| **Posting** | Publishing and editing, voting, following, joining communities, claiming rewards | In the app. It cannot move tokens. |
| **Active** | Transfers, staking and delegations, savings, conversions, votes for witnesses and proposals, profile changes | Only in apps you trust: whoever holds it can take your tokens |
| **Owner** | Changing your keys | Offline. The app asks for it only when you change your keys. |
| **Memo** | Nothing yet | With the others |

Transfer memos sent from the app are not encrypted. Everyone can read them.

## See and copy your keys

1. Open your wallet at `https://pixagram.com/@yourname/wallet/overview`, replacing `yourname` with your account.
2. Under "Do you need more control?", click **Keys**.
3. On the **Wallet Keys** tab, click the eye ("Reveal key") to show a private key, or **Copy to clipboard**. If you set a vault password, the app asks for it first.

- **The app overwrites the clipboard 30 seconds after you copy a private key.** Paste it at once, and only where you mean to.
- **A key shown as "Unknown — not in current session"** is not loaded in this browser. Click its icon to add it for this session.
- **The phrase cannot be shown again.** It is in your PDF.
- **Nobody needs your private keys to help you.** As the app says: "Our team will never ask you for your private keys."

## How the app keeps your keys

| How you log in | How long the keys stay | How they are protected |
|---|---|---|
| **LOG IN** | 48 hours, in this browser | Encrypted with a key that cannot leave this browser; no password |
| **Advanced mode.** → **Set a vault password** | From 12 hours to 5 days, as you choose under **Session Timeout** | Also locked with your vault password, which the app asks for again after the **Password Timeout**: 15 minutes to 2 hours |
| **Advanced mode.**, with **Keep credentials alive across sessions** unticked | Until you close or reload the tab | Kept in the tab's memory only |

- **The vault password** must be at least 8 characters long, and the app refuses weak or common ones. When it asks for it again, it calls it your PIN.
- **Wrong entries:** after 10, unlocking is blocked for 5 minutes, and each new block lasts twice as long. After 50 in total, the app deletes every session stored in the browser, and you log in again with your master key.
- **On a device other people use,** set a vault password or untick **Keep credentials alive across sessions**, and log out when you leave.
- **To keep your master key off a device,** log in with your posting key instead. The app then asks for the active key only when an action needs it, and keeps it for that session only.

## Log out

Click the exit icon in the side menu, then **Logout**. The app removes this account's keys from the browser. If your browser saved a password for Pixagram, that copy stays: remove it in your browser's settings.

## Sign in with your recovery phrase

Use this when you have your phrase but neither your PDF nor your master key.

1. **Set the app to the language of your phrase,** if it is not English. The app accepts words from that language's list and from English.
2. **Open the sign-up** at [pixagram.com/+signup](https://pixagram.com/+signup) and type your username. Because the account exists, the dialog shows "Recovery mode: enter your seed phrase below to take this account back".
3. **Enter your words in order,** and your password if you set one.
4. **Tick the Terms of Use box** and click **RECOVER**.
5. **Click VERIFY SEED.** The app rebuilds your keys and compares them with your account on the chain. Then click **NEXT**.
6. **Wait for "Account recovered. You're signed in."** and save the copy of your backup PDF that the app offers.

This works only while your phrase still matches your account's keys. It is not the chain's account recovery, which is described [below](#if-your-keys-are-stolen).

## Change your keys

Change them if your PDF or a private key may have been seen by someone else, or if someone else opened your account for you.

1. Open **Keys**, then the **Keys Update** tab.
2. Click the seed icon, choose the length under **Entropy Selection** (12 words to start with), and click the check mark.
3. Optionally, fill in **Password (Optional but Recommended)**. It is shown as you type.
4. Tick **Download the document and acknowledge.** The app downloads your new PDF, and the label changes to "I downloaded the document". Changing the phrase or the password afterwards unticks it.
5. **Open the PDF before you go on.** Check that it shows your username and the new phrase, then store it offline. The app cannot tell whether the download finished: if no file was saved, untick the box and tick it again.
6. Click **Apply keys**, and give your current owner key or master key when asked.
7. The app shows "Applying new keys to the blockchain..." and then logs you out. Log in with the master key from the new PDF.

**You cannot undo this.** The old phrase, the old master key and the old keys stop working, and only the new PDF opens the account.

- **Other accounts lose access.** The change leaves only your new keys in control. Any app or account you had authorised to act for you must be authorised again.
- **The chain allows two owner-key changes per hour** ([Chain Parameters](../21-reference/chain-parameters.md#accounts-and-keys)).
- **If the app does not log you out,** the change did not go through. Try again.

## If your keys are stolen

| What was taken | What the thief can do | What to do |
|---|---|---|
| **Posting key** | Post, vote and follow as you, and edit or delete your posts | [Change your keys](#change-your-keys) |
| **Active key** | Move your tokens, and replace your active and posting keys | Change your keys at once. Tokens in savings take 3 days to leave, which leaves you time to cancel a withdrawal with your new keys ([Savings](../21-reference/glossary.md#savings)). |
| **Owner key**, not yet used | Everything, including changing your keys | Change your keys first, before the thief does |
| **Owner key**, already changed by the thief | Everything; you are locked out | The chain can reverse an owner-key change made after 2026-10-07 12:00 UTC, through your recovery partner, but the app has no screen for it: you need a Hive-compatible tool and the partner's help. Keeping the owner key offline is what prevents this. |

The chain keeps the history of owner keys since hardfork 30, 2026-10-07 12:00 UTC. A recovery needs an owner key the account used within the last 30 days and the recovery partner's request, and it can undo only owner-key changes made after that moment: an account whose owner key was taken before it has nothing on record to recover from ([why](../21-reference/chain-parameters.md#accounts-and-keys)).

## Sources

- **Keys from the phrase:** [`BackUpWallet2.js:291-348`][bw-291]; the PDF, [`BackUpWallet2.js:111-154`][bw-111].
- **The Keys dialog**, with its three tabs: [`PixaWalletKeysDialog.js`][keys]; the clipboard, [`PixaWalletKeysDialog.js:663-689`][keys-663]; changing keys, [`PixaWalletKeysDialog.js:767-830`][keys-767]; the recovery partner, [`PixaWalletKeysDialog.js:904-1011`][keys-904].
- **Which action needs which key:** [`pixaproxyapi.js:1039-1069`][api-1039].
- **How keys are kept:** [`session-manager.js`][session]; the vault password's rules, [`pixaproxyapi.js:501-517`][api-501] and [`LoginDialog.js:77-95`][login-77]; wrong entries, [`pixaproxyapi.js:10519-10591`][api-10519]; the timeouts, [`LoginDialog.js:531-548`][login-531].
- **Recovery mode in the sign-up:** [`CreateAccountDialog.js:3040-3085`][cad-3040] and [`CreateAccountDialog.js:2399-2433`][cad-2399].
- **English text:** [`en.js:1826-1912`][en-1826].
- **Chain:** the recovery window, the limit on owner-key changes and the date owner-key history starts, [Chain Parameters](../21-reference/chain-parameters.md#accounts-and-keys).

[bw-291]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/BackUpWallet2.js#L291-L348
[bw-111]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/BackUpWallet2.js#L111-L154
[keys]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletKeysDialog.js
[keys-663]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletKeysDialog.js#L663-L689
[keys-767]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletKeysDialog.js#L767-L830
[keys-904]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletKeysDialog.js#L904-L1011
[api-1039]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L1039-L1069
[session]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/session-manager.js
[api-501]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L501-L517
[api-10519]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L10519-L10591
[login-77]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/LoginDialog.js#L77-L95
[login-531]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/LoginDialog.js#L531-L548
[cad-3040]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateAccountDialog.js#L3040-L3085
[cad-2399]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateAccountDialog.js#L2399-L2433
[en-1826]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1826-L1912
