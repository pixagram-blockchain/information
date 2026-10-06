# Wallet Basics

> **Status: Live.** PIXA does not trade on any market yet, so the wallet values it at a fixed placeholder price, and PXS promises no price. Described from the app's code of 2026-10-04. Last checked 2026-10-06.

The wallet holds your three balances: PIXA, Pixa Power and PXS ([Tokens at a Glance](../04-tokens-and-economy/tokens-at-a-glance.md)). This guide covers sending tokens, staking, savings, conversions and rewards. Every action here except claiming rewards needs your active key ([Keys and Recovery](keys-and-recovery.md)). None can be undone once it is in a block, though you can stop a power-down, a savings withdrawal, a delegation or a recurring transfer.

## Open your wallet

On your profile, click the wallet icon: in the sidebar on a computer, or in the profile card on a phone, once you open it. You can also go straight to `https://pixagram.com/@yourname/wallet/overview`, replacing `yourname` with your account.

| Tab | Address ends in | What it shows |
|---|---|---|
| Overview | `/wallet/overview` | "Estimated Wealth", how it splits between the tokens, pending rewards, any power-down, and the **Quick Transfer**, **Keys** and **Taxes** buttons |
| Power | `/wallet/power` | Your Pixa Power, your delegations in and out, and your power-down |
| Pixa | `/wallet/pixa` | Your PIXA, savings, pending conversions and recurring transfers |
| Supra | `/wallet/supra` | Your PXS, with the same sections |
| History | `/wallet/history` | Your last 1,000 transactions, and **Claim Reward** |

The app writes PIXA as PXA and Pixa Power as PXP.

**About the amounts in your currency.** PIXA does not trade on any market yet. The wallet values PIXA and Pixa Power at a fixed placeholder of 0.12 USD, and PXS through the witnesses' feed, which uses the same placeholder ([Chain Parameters](../11-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). The rate to your currency comes from Frankfurter, and you choose the currency in Settings. These amounts are not prices anyone has paid.

## Send tokens

1. On the Pixa or Supra tab, click **Transfer**. On the overview, **Quick Transfer** sends PIXA.
2. Type the account under "Username". The app also lists "People you've sent to before".
3. Type the amount, with up to 3 decimals, and choose PXA or PXS.
4. Optionally, write a memo under "Memo (optional)", up to 140 characters. **Memos are public.** Never put a key, a password or private details in one.
5. Optionally, tick "Make this a recurring transfer" and set how often, at least every 24 hours, and how many payments, at least 2. The first payment leaves at once.
6. Click **Confirm** and check the summary.
7. Slide "Slide to Confirm" to the end.

**You cannot undo this.** Check the account name twice: a transfer to the wrong account cannot be recalled.

To stop a recurring transfer, open the Pixa or Supra tab and, under **Recurring Transfers**, click × on its row. No further payments are sent.

## Stake: power up and power down

- **Power up.** On the Pixa tab, click **Power-Up**, type the amount and confirm. The PIXA becomes Pixa Power at once. It gives your votes their weight and your account its [Resource Credits](../04-tokens-and-economy/resource-credits.md); for votes on witnesses and proposals, it counts after 30 days ([Pixa Power](../04-tokens-and-economy/pixa-power.md#effective-pixa-power)).
- **Power down.** On the Power tab, click **Power-Down** and type the amount. It comes back as PIXA in 13 weekly instalments, the first one 7 days after you start. Only one power-down runs at a time. **Cancel**, on the same tab, stops the instalments not yet paid ([Power down](../04-tokens-and-economy/pixa-power.md#power-down)).

## Delegate Pixa Power

1. On the Power tab, under **Outgoing**, click **Delegate**.
2. Type the account under **Beneficiary**, and the amount: at least about 6.67 Pixa Power, and at most your own Pixa Power not already lent. The chain also leaves out stake you are powering down, and lets you lend no more than your voting power covers, so wait after heavy voting.
3. Confirm, and slide to the end.

The account gets the use of the stake, for voting and for Resource Credits. The stake stays yours. To take it back, click × on its row: the account loses it at once, and it returns to you after 5 days ([Delegation](../04-tokens-and-economy/pixa-power.md#delegation)).

## Savings

1. On the Pixa or Supra tab, under **Savings**, click **Deposit**, type the amount and confirm.
2. To take money out, click **Withdraw**. The funds arrive after **3 days**. Until then, you can cancel the withdrawal and the funds stay in savings.

Savings earn no interest on Pixa. They protect you instead: someone who steals your active key needs 3 days to take your savings out, which leaves you time to [change your keys](keys-and-recovery.md#change-your-keys) and cancel the withdrawal.

## Convert between PIXA and PXS

PXS promises no price. A conversion settles at the witnesses' median feed, reduced by a haircut when collateral is thin, and today that feed uses a placeholder price for PIXA ([PXS at a Glance](../05-pixa-supra/pxs-at-a-glance.md)). **You cannot cancel a conversion** once it is sent.

- **PIXA to PXS.** On the Pixa tab, click **Swap**. The PIXA you convert is locked as collateral, and PXS arrives at once: half the collateral converted at the feed, less a 5% fee. 3.5 days later, the chain takes what the PXS cost at the market median then, plus the fee, and returns the rest of the collateral. If the median has more than doubled by then, meaning PIXA has lost more than half its value against a Big Mac, the chain keeps all the collateral. The chain refuses this conversion while PXS printing is stopped ([details](../05-pixa-supra/haircut-corridor-and-settlement.md#converting-pixa-into-pxs)).
- **PXS to PIXA.** On the Supra tab, click **Swap**. The PXS leaves your balance at once, and the PIXA arrives 3.5 days later, at the median feed of that moment. There is no fee ([details](../05-pixa-supra/haircut-corridor-and-settlement.md#converting-pxs-into-pixa)).

Do not rely on the "Receive" figure the app shows before you confirm. It does not come from the witnesses' feed, and for PIXA to PXS it counts all the PIXA and no fee, so you receive less than half of it. PXS from PIXA is fixed at once; PIXA from PXS is fixed when the conversion settles.

## Claim rewards

On the History tab, click **Claim Reward**. It moves your pending author and curation rewards into your balances, and uses your posting key. The overview shows what is waiting under "Rewards Pending".

## History and taxes

- **History** lists incoming and outgoing transfers, your own operations and rewards, with a filter for each. **Hide dust** hides rows under 1.
- **Taxes**, on the overview, exports your history as CSV, JSON or PDF for the dates and the country you choose. It values every transaction at today's placeholder price, whatever its date, so its amounts are not market values.

## If something goes wrong

| The app says | What to do |
|---|---|
| "You already have an active power down" | Wait for it to finish, or cancel it first. |
| "ERROR: The amount is above your balance." | Lower the amount. |
| "Not available on another user's wallet" | Open your own wallet. On someone else's, you can only send to them or delegate to them. |
| "Permission required for … action" | Your session does not hold the key this action needs. Give your active key, or your master key. |

## Sources

- **The wallet and its tabs:** [`PixaWalletDialog.js`][wallet]; the addresses, [`Profile.js:293-313`][profile] and [`constants.js:30`][const-30].
- **Actions:** sending, [`PixaWalletSendDialog.js`][send]; delegating, [`PixaWalletDelegateDialog.js`][delegate]; savings, [`PixaWalletSavingsDialog.js`][savings]; conversions, [`PixaWalletSwapDialog.js`][swap]; the operations and their keys, [`pixaproxyapi.js:5842-6103`][api-5842] and [`pixaproxyapi.js:6651-6786`][api-6651].
- **Values in your currency:** the placeholder price, [`pixaproxyapi.js:3814-3845`][api-3814]; exchange rates, [`pixaproxyapi.js:4193-4214`][api-4193].
- **Taxes:** [`PixaWalletTaxesDialog.js`][taxes].
- **English text:** [`en.js:1655-2045`][en-1655].
- **Chain:** power-down, delegation return and the 30-day wait, [Chain Parameters](../11-reference/chain-parameters.md#pixa-power-staking); conversions, [Haircut, Corridor and Settlement](../05-pixa-supra/haircut-corridor-and-settlement.md#sources).

[wallet]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletDialog.js
[profile]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/pages/Profile.js#L293-L313
[const-30]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L30
[send]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletSendDialog.js
[delegate]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletDelegateDialog.js
[savings]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletSavingsDialog.js
[swap]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletSwapDialog.js
[api-5842]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L5842-L6103
[api-6651]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L6651-L6786
[api-3814]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L3814-L3845
[api-4193]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/api/pixaproxyapi.js#L4193-L4214
[taxes]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/components/PixaWalletTaxesDialog.js
[en-1655]: https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/locales/en.js#L1655-L2045
