# CLI Wallet

> **Status: Live.** The `cli_wallet` inside `pixadock/pixagram:1.30.0` (revision `d986a23`). Every command on this page was run on 2026-10-05 with the 1.29.0 image and the start-up checked again with 1.30.0 on 2026-10-08; online use was tested against a local node, and no transaction was broadcast.

`cli_wallet` is hived's command-line wallet. It ships in the node image, needs no installation, and defaults to Pixa's chain ID and `PIX` keys. It has two modes: **offline**, for generating keys and inspecting transactions, and **online**, connected to a node that serves its API, for signing and broadcasting. The public API nodes do not serve that API, so online use needs your own node.

## What it can do

| Task | Commands | Offline | Online |
|---|---|---|---|
| Generate a key pair | `suggest_brain_key` | yes | yes |
| Derive an account's keys from a password | `get_private_key_from_password` | yes | yes |
| Keep keys in an encrypted file | `set_password`, `unlock`, `import_key`, `list_keys`, `lock` | yes | yes |
| Show the bytes of a transaction | `serialize_transaction` | yes | yes |
| Read the chain | `info`, `get_account`, `get_witness`, `get_block` … | no | yes |
| Sign and broadcast | `transfer`, `vote`, `update_witness`, `publish_feed`, `sign_transaction` … | **no** | yes |

Offline, a signing command stops with `Online mode is required in order to perform this method`. The wallet cannot sign a transaction offline and broadcast it elsewhere.

## Start it offline

```bash
mkdir -p wallet
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD/wallet:/wallet" -w /wallet \
  --entrypoint /home/hived/bin/cli_wallet pixadock/pixagram:1.30.0 -o
```

Expected output:

```text
STARTING HIVE WALLET
chain id: 706978616772616d000000000000000000000000000000000000000000000000
blockchain version: 1.30.0
git_revision: "d986a238a4fbece1ce1df07782ca868174ee9bf8"
…
Starting a new wallet
Please use the set_password method to initialize a new wallet before continuing
new >>>
```

- **`-o`** keeps the wallet offline: it connects to nothing.
- **`--user` and `-v`** keep the wallet file in `./wallet` on your machine. Without `--user`, the wallet runs as user 1000 inside the container; if that user cannot write to `./wallet`, the wallet still prints `Saving wallet to file wallet.json`, but no file appears.
- **`exit`** leaves the wallet. There is no `quit` command.
- **`help`** lists every command; **`gethelp <command>`** explains one.

## Generate a key pair

```text
new >>> suggest_brain_key
```

Expected output (your values differ):

```json
{
  "brain_priv_key": "<16 words>",
  "wif_priv_key": "5…",
  "pub_key": "PIX…"
}
```

The private key in WIF form starts with `5`; the public key starts with `PIX`. The 16 words recreate both. A witness uses such a pair as its block-signing key ([Become a Witness](become-a-witness.md#1-create-a-signing-key)).

## Derive keys from a password

```text
new >>> get_private_key_from_password your-account active "your password"
```

Expected output:

```json
[
  "PIX…",
  "5…"
]
```

The result is the public and private key that the password gives for that account and role (`owner`, `active`, `posting` or `memo`). dpixa's `PrivateKey.fromLogin(account, password, role)` gives the same pair. The command only derives keys; it does not check that the account uses them.

## Keep keys in the wallet file

```text
new >>> set_password your-wallet-password
locked >>> unlock your-wallet-password
unlocked >>> import_key 5…
unlocked >>> list_keys
```

- `wallet.json` stores keys encrypted with the wallet password; no key appears in it as text. The wallet saves it after each change, and `lock` locks it again.
- Commands typed at the prompt, passwords and keys included, appear on your screen and may stay in your terminal's scrollback. Clear it afterwards.

## Show the bytes of a transaction

```text
new >>> serialize_transaction {"ref_block_num":1234,"ref_block_prefix":1122334455,"expiration":"2026-10-05T18:00:00","operations":[["transfer",{"from":"alice","to":"bob","amount":"1.000 PIXA","memo":"hi"}]],"extensions":[],"signatures":[]}
```

Expected output:

```text
"d204f776e542a0e5c36a010205616c69636503626f62e80300000000000003504958410000000268690000"
```

The last byte, `00`, is the empty list of signatures. The bytes before it, preceded by the chain ID, are what a signature covers. A public node's `condenser_api.get_transaction_hex` returns the same for this transaction, which is how to [test another library](../09-developers/sdks-and-libraries.md#test-a-library-before-you-trust-it).

## Use it online

The wallet talks to a node over a websocket, through the node's `wallet_bridge_api` plugin. On 2026-10-05 none of the public nodes offer either, so connect it to your own node.

**1. Add the plugin.** On a node set up as in [Run a Node](run-a-node.md), append `wallet_bridge_api` to the `plugin` line of `pixagram/config.ini`:

```ini
plugin = witness database_api condenser_api network_broadcast_api wallet_bridge_api
```

```bash
docker compose restart pixagram
docker compose logs pixagram | grep 'Wallet bridge api'
```

Expected output, among other lines: `Wallet bridge api initialized. Missing plugins: account_history_api account_by_key_api market_history_api`. The wallet works without those three; only commands that need history, key lookups or the market fail. Adding this plugin needs no replay.

**2. Start the wallet inside the node's container,** where the node's websocket listens on port 8090:

```bash
docker compose exec pixagram /home/hived/bin/cli_wallet -s ws://127.0.0.1:8090 -w /tmp/wallet.json
```

The wallet file lives in the container's `/tmp` and disappears when the container is recreated. Import the key you need for the session, use it, and `exit`.

```text
new >>> get_witness your-account
```

The wallet speaks to hived directly, so it uses **Hive's names**: commands such as `convert_hbd`, fields such as `hbd_interest_rate`, `hbd_amount` and `reward_hbd`. Amounts are written with Pixa's symbols: `"1.000 PIXA"`, `"1.000 PXS"`. Every command that ends in `bool broadcast` signs, and broadcasts only when that last argument is `true`.

## Sources

- **Wallet source,** commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443): online-only signing in [`libraries/wallet/wallet.cpp:183-186`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/wallet/wallet.cpp#L183-L186) and [530-533](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/wallet/wallet.cpp#L530-L533); the plugin's requirements in [`wallet_bridge_api_plugin.hpp:24-31`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/apis/wallet_bridge_api/include/hive/plugins/wallet_bridge_api/wallet_bridge_api_plugin.hpp#L24-L31).
- **Image:** `pixadock/pixagram:1.30.0`, revision `d986a23`, pushed 2026-10-07; its entrypoint starts hived with the websocket on `WS_PORT`, 8090 by default. The wallet code is unchanged from 1.29.0.
- **Tests on 2026-10-05** with the 1.29.0 image, and the start-up and `about` with 1.30.0 on 2026-10-08: every command above, offline; `get_private_key_from_password` compared with dpixa's `PrivateKey.fromLogin`; `serialize_transaction` compared with `condenser_api.get_transaction_hex` on `api.pixagram.com`; the online wallet connected to a local 1.29.0 node with `wallet_bridge_api`; `wallet_bridge_api` and websocket upgrades tried on all six public nodes.
