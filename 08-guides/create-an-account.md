# Create an Account

> **Status: Live.** Sign-up in the app is free after phone verification; a fund proposal pays the account fee until 2026-12-31. Described from the app's code of 2026-10-04. Last checked 2026-10-06.

This guide opens a Pixagram account at pixagram.com and signs you in. You need a phone that can receive an SMS and a safe place for one PDF file. What happens on the chain is explained in [What Is Pixagram](../01-start-here/what-is-pixagram.md#how-an-account-starts); what each key does, in [Keys and Recovery](keys-and-recovery.md).

## Before you start

- **A phone number that can receive an SMS.** Each number opens one account, and verification is not available in every country. If yours is not offered, see [If you cannot verify by SMS](#if-you-cannot-verify-by-sms).
- **A safe place for your backup.** The app gives you a PDF with your recovery phrase and your keys. Whoever holds it controls your account. If you lose both the PDF and your keys, no one can give the account back.

## 1. Open the sign-up

Go to [pixagram.com/+signup](https://pixagram.com/+signup), or choose **SignUp** in the side menu. The sign-up opens over the newest posts. It is called **Join Pixa** and has three steps: **GENERATE**, **VERIFY** and **CONFIRM**.

## 2. Choose your name

1. **Type a username.** It is permanent: an account cannot be renamed. The name must:
   - be 3 to 16 characters long;
   - use only lowercase letters, digits, hyphens and dots;
   - be made of parts separated by dots, each at least 3 characters long, starting with a letter and ending with a letter or a digit;
   - contain no two hyphens in a row.
2. **Wait for the tick at the end of the field.** Its tooltip reads "SUCCESS: The username is available." If the name belongs to an account already, the dialog switches to recovery mode, which is for owners signing in with their recovery phrase ([Keys and Recovery](keys-and-recovery.md#sign-in-with-your-recovery-phrase)). Choose another name.
3. **Read the Terms of Use and the Privacy Policy,** then tick "I have read the Terms of Use and the Privacy Policy and fully agree with them."
4. **Optional: open Advanced Configuration.** It shows the recovery phrase the app has just made for you in your browser: 18 words by default, from 12 to 24. It also offers **Password (Optional)**. A password is combined with the phrase to make your keys, so you will need both to rebuild them, and the PDF prints the password next to the phrase.
5. **Click NEXT.**

## 3. Verify your phone

1. **Choose your country** and type your number.
2. **Click SEND CONFIRMATION CODE.** A browser check runs first.
3. **Type the code from the SMS:** six letters and digits. It is checked as soon as it is complete, and the dialog shows "Verified. You can continue."
4. **Click NEXT.**

A number can receive only a few codes, with a wait between them; the app tells you the date of the next one. The service also opens a limited number of accounts each day, shown under "Accounts still available". If none are left, the app shows when new places open.

## 4. Save your backup

1. **Wait for "Account created."** The operator's account service opens the account, pays the account creation fee and lends it a little Pixa Power, so you can post from the first day. Only your public keys leave your browser.
2. **Click DOWNLOAD BACKUP PDF** and save `KeysOf-yourname-Pixagram.pdf`. Some browsers then ask you to tick "I have saved my backup PDF". The dialog does not close until the PDF is saved.

   The PDF holds your recovery phrase, your password if you set one, your master key and your four private keys, with QR codes. **Keep it offline.** Print it, or keep it on a drive you store safely. Do not send it by email or chat, and do not keep it in a shared folder.
3. **Click OK.** The app signs you in.

## After you sign up

- **You are signed in on this browser for one day.** Then [log in](#log-in) again.
- **Your browser may offer to save a password.** What it would save is your master key, outside the app's protection. Decline on any device that other people use.
- **Settings** set the language, the display currency and the API node. Open them from the ⋮ menu in the toolbar, or at [pixagram.com/created/+settings](https://pixagram.com/created/+settings).
- **Publish:** [Publish Your First Artwork](publish-your-first-artwork.md).
- **Your votes on posts move no rewards yet.** A vote counts only once the account holds more than 2,500 Pixa Power ([why](../02-social-layer/voting-and-curation.md#why-small-votes-count-for-nothing)).

## Log in

1. Open [pixagram.com/+login](https://pixagram.com/+login), or choose **LogIn** in the side menu.
2. Type your username. In "Master password or private key", paste the master key from your PDF, or one of your private keys. The app detects which key it is.
3. Click **LOG IN**. The app keeps your keys in this browser for 48 hours. To protect them with a password, or to change how long they are kept, open **Advanced mode.** first ([how the app keeps your keys](keys-and-recovery.md#how-the-app-keeps-your-keys)).

The log-in does not accept the recovery phrase. To sign in with it, use [recovery mode](keys-and-recovery.md#sign-in-with-your-recovery-phrase).

## If you cannot verify by SMS

Someone who already has an account can open one for you. In the menu, under Apps, they choose **Create Account** ("Use your credits"). They pay the account creation fee, or use an account ticket claimed with Resource Credits, and the app gives *them* a PDF with your new keys. When they pass it to you, [change your keys](keys-and-recovery.md#change-your-keys), so that only you hold them.

## If something goes wrong

| The app says | What to do |
|---|---|
| "This phone number has already been used to create an account." | Each number opens one account. Log in to that account, or use another number. |
| "An SMS was already sent to this number. The next one is possible on …" | Use the code you received, or wait until that date. |
| "SMS verification is not yet available for this country." | See [If you cannot verify by SMS](#if-you-cannot-verify-by-sms). |
| "The browser check did not pass. …" | Allow challenges.cloudflare.com in your content blocker, reload the page and try again. |
| "That code doesn't match — … left before you need a new one." | Check the SMS and type the code again. |
| "@… was just taken on-chain. Go back and pick another name — your phone verification is still valid." | Go back to the first step and choose another name. |
| "The download was cancelled — your backup isn't saved yet." | Click **DOWNLOAD AGAIN** and let the download finish. |

## Sources

- **Sign-up:** [`CreateAccountDialog.js`][cad]; the name rules the app checks, [`BackUpWallet2.js:184-196`][bw-184]; the phrase and the keys, [`BackUpWallet2.js:291-348`][bw-291]; the PDF, [`BackUpWallet2.js:111-154`][bw-111].
- **Addresses:** `+signup`, `+login` and `+settings`, [`constants.js:825-920`][const-825].
- **Log-in:** [`LoginDialog.js`][login]; the 48-hour default, [`LoginDialog.js:1353`][login-2213].
- **Creating an account for someone else:** [`AddAccountDialog.js`][add].
- **English text:** [`en.js:438-563`][en-438] (sign-up) and [`en.js:1378-1449`][en-1378] (log-in).
- **Chain:** the account-name rule, [`authority.cpp:58-121`][name]; the account creation fee and tickets, [Chain Parameters](../11-reference/chain-parameters.md#accounts-and-keys); who pays for new accounts, [Who Does What](../01-start-here/who-does-what.md#who-pays-for-what-today).

[cad]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/CreateAccountDialog.js
[bw-184]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/BackUpWallet2.js#L184-L196
[bw-291]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/BackUpWallet2.js#L291-L348
[bw-111]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/BackUpWallet2.js#L111-L154
[const-825]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L825-L920
[login]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/LoginDialog.js
[login-2213]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/LoginDialog.js#L1353
[add]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/AddAccountDialog.js
[en-438]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L438-L563
[en-1378]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1378-L1449
[name]: https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/authority.cpp#L58-L121
