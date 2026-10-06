# SDKs and Libraries

> **Status: Live.** Versions read from the npm registry on 2026-10-05. Behaviour tested on that date with `@pixagram/dpixa` 1.5.4 and `@hiveio/dhive` 1.3.2 against `api.pixagram.com`.

This page lists the libraries and tools for building on the Pixa chain, says which of them can sign which operations, and records the quirks of the current versions with a workaround for each. It ends with a test you can run on any library before you trust it with a key.

## Which client to use

| You want to | Use |
|---|---|
| Read and write from JavaScript or TypeScript, in Node or the browser | [`@pixagram/dpixa`](#dpixa) |
| Read from any language | JSON-RPC over HTTPS with any HTTP client ([Developer Quickstart](developer-quickstart.md#1-one-request-with-curl)) |
| Sign from another language | A Hive library that lets you set the chain ID and key prefix, after it passes [the digest test](#test-a-library-before-you-trust-it) |
| Generate keys offline | `cli_wallet`, in the node image ([CLI Wallet](../10-node-operators/cli-wallet.md)) |
| Watch the witnesses | The `witness-status` command-line check ([Tools](#tools)) |

## dpixa

`@pixagram/dpixa` is a fork of dhive, Hive's TypeScript client, with Pixa's chain ID, `PIX` key prefix and PIXA and PXS symbols as defaults. The Pixagram app uses it. Licence: BSD-3-Clause-No-Military-License.

### Install and load

```bash
npm install @pixagram/dpixa@1.5.4
```

```js
// CommonJS. require("@pixagram/dpixa") fails in 1.5.4; load the bundle.
const { Client, PrivateKey, Asset } = require("@pixagram/dpixa/dist/dpixa.js");

// ES modules
import dpixa from "@pixagram/dpixa/dist/dpixa.js";
```

```html
<!-- Browser, no build step: defines the global `dpixa` -->
<script src="https://unpkg.com/@pixagram/dpixa@1.5.4/dist/dpixa.js"></script>
```

### Configure

```js
const client = new Client(
  ["https://api.pixagram.com", "https://pixarex.net", "https://merlion.surf"],
  { timeout: 10000, failoverThreshold: 3, consoleOnFailover: true },
);
```

| Option | Default | Meaning |
|---|---|---|
| `chainId` | `706978616772616d` + zeros | Leave it. |
| `addressPrefix` | `PIX` | Leave it. |
| `timeout` | 60000 ms | How long the client keeps retrying a call on one node before it moves to the next node in the list. `0` retries forever. |
| `failoverThreshold` | 3 | How many times the client moves to another node before it gives up. `0` never gives up. |
| `consoleOnFailover` | `false` | Log each move to another node. |

### What it covers

| Property | For | Examples |
|---|---|---|
| `client.database` | Chain state and history | `getDynamicGlobalProperties()`, `getAccounts([names])`, `getBlock(n)`, `getAccountHistory(account, from, limit)`, `getCurrentMedianHistoryPrice()` |
| `client.blockchain` | Following new blocks | `getCurrentBlockNum()`, `getBlocks()`, `getOperations()` as async iterators |
| `client.broadcast` | Signing and sending | `vote()`, `comment()`, `commentWithOptions()`, `transfer()`, `json()`, `delegateVestingShares()`, `updateAccount()`, and `sendOperations(ops, key)` for any other operation, such as `claim_reward_balance` |
| `client.rc` | Resource Credits | `getRCMana(account)`, `findRCAccounts([names])` |
| `client.pixamind` | The social API (`bridge.*`) | `getRankedPosts()`, `getAccountPosts()`, `getCommunity()`, `getAccountNotifications()` |
| `client.keys` | Accounts for a public key | `getKeyReferences([keys])` |
| `client.call(api, method, params)` | Any JSON-RPC call | `client.call("condenser_api", "get_transaction", [id])` |
| `PrivateKey`, `PublicKey` | Keys | `PrivateKey.fromString(wif)`, `PrivateKey.fromLogin(account, password, role)`, `key.createPublic()` |

### Quirks in 1.5.4

Each was reproduced on 2026-10-05.

| Quirk | Effect | Workaround |
|---|---|---|
| The package entry point names `lib/index-node`, which is not published | `require("@pixagram/dpixa")` and `import … from "@pixagram/dpixa"` fail in Node | Load `@pixagram/dpixa/dist/dpixa.js` |
| The README's examples list a retired Pixagram address and Hive nodes | Requests go to the wrong network | Use the [public Pixa nodes](developer-quickstart.md#before-you-start) |
| `Client.testnet()` signs with Hive's testnet chain ID (`18dcf0…`) and `TST` keys, against `api.pixagram.com` | Everything it signs is rejected; there is no Pixa testnet | Do not use it |
| `Asset.from(5)`, with a number, makes `5.000 STEEM` | A wrong symbol in an operation | Pass strings: `Asset.from("5.000 PIXA")` |
| `broadcast.*` returns `{ id }` as soon as the node accepts the transaction | There is no block number in the result | Poll `condenser_api.get_transaction` with the id ([example](developer-quickstart.md#5-sign-and-broadcast-a-vote)) |
| Operations are serialized with Pixa's field names in `claim_reward_balance`, `comment_options`, `escrow_transfer`, `escrow_release` and `witness_update` | Sent to a hived without the gateway, a renamed field that does not hold its default value is lost, and the transaction is rejected | Broadcast them through a public node ([why](differences-from-hive.md#talking-to-hived-directly)) |
| `buildWitnessUpdateOp()` writes the properties `pxs_exchange_rate` and `pxs_interest_rate`; the chain reads `hbd_exchange_rate` and `hbd_interest_rate` | Those two properties are ignored, or the transaction is rejected | Publish feeds with `feed_publish`; leave the interest rate out |

## Hive libraries

Pixa's API is Hive's, so a Hive library can read from it. Signing is where the chains differ: the chain ID, the key prefix and, in the legacy wire format, the symbol bytes of amounts.

`@hiveio/dhive` 1.3.2, configured for Pixa:

```js
const { Client } = require("@hiveio/dhive");
const client = new Client(["https://api.pixagram.com"], {
  chainId: "706978616772616d" + "0".repeat(48),
  addressPrefix: "PIX",
});
```

| Test on 2026-10-05 | Result |
|---|---|
| `getDynamicGlobalProperties()`, `getAccounts()`, `bridge` calls | Work |
| `getCurrentMedianHistoryPrice()` and other helpers that parse amounts | Fail: `Invalid asset symbol: PXS` |
| Signing `vote`, `comment` and `custom_json` | Same digest as the chain |
| Signing a `transfer` of `1.000 HIVE` | **Different digest**: dhive writes Hive's symbol bytes, and it refuses `1.000 PIXA` |

Other Hive libraries (beem, hive-tx, hive-js and the rest) were not tested. Run the test below before you sign with one.

## Test a library before you trust it

A library signs correctly only if it builds the same bytes the chain builds. The public nodes return the chain's serialization of any transaction through `condenser_api.get_transaction_hex`, which signs nothing and broadcasts nothing. The digest a signature must cover is SHA-256 of the chain ID followed by those bytes.

Save as `expected-digest.js` (Node 18 or newer):

```js
// expected-digest.js: print the digest the Pixa chain expects a signature over
// usage: node expected-digest.js tx.json
const fs = require("fs");
const crypto = require("crypto");

const CHAIN_ID = Buffer.from("706978616772616d" + "0".repeat(48), "hex");

async function main() {
  const tx = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const reply = await fetch("https://api.pixagram.com", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0", id: 1,
      method: "condenser_api.get_transaction_hex",
      params: [{ ...tx, signatures: [] }],
    }),
  }).then((r) => r.json());
  if (reply.error) throw new Error(reply.error.message);
  const bytes = Buffer.from(reply.result.slice(0, -2), "hex"); // drop the empty signature list
  console.log(crypto.createHash("sha256").update(Buffer.concat([CHAIN_ID, bytes])).digest("hex"));
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

Save a transaction with fixed header values as `tx.json`:

```json
{
  "ref_block_num": 1234,
  "ref_block_prefix": 1122334455,
  "expiration": "2026-10-05T18:00:00",
  "operations": [["transfer", {"from": "alice", "to": "bob", "amount": "1.000 PIXA", "memo": "hi"}]],
  "extensions": []
}
```

```bash
node expected-digest.js tx.json
```

Expected output:

```text
4f7c6ec6c03d03f1f4fc4a3746cb9a01da44a02af29ce28e4382c6ffb00c3e0a
```

Then compute the digest of the same transaction with the library under test. With dpixa it is `cryptoUtils.transactionDigest(tx, chainId).toString("hex")`, which gives the same value. If your library prints anything else, signatures it makes for that operation will be rejected. Repeat the test for every operation type you use.

## Other `@pixagram` packages

The Pixagram app is built from these packages, published under the `@pixagram` scope. Each can be used on its own.

| Package | Version | What it does | Licence |
|---|---|---|---|
| `dpixa` | 1.5.4 | The chain client ([above](#dpixa)) | BSD-3-Clause-No-Military-License |
| `lacerta-db` | 0.16.0 | On-device database on IndexedDB, with indexes and encryption | MIT |
| `turboserial` | 0.5.2 | Binary serialization of JavaScript values, including typed arrays, `BigInt`, `Map`, `Set` and circular references | MIT |
| `turbobase64` | 1.0.1 | Base64 encoding and decoding | MIT |
| `pixahash` | 0.1.0 | A fast non-cryptographic hash in WebAssembly | MIT |
| `renderart` | 1.0.3 | Pixel-art rendering at any display size, in WebGL2 with a WebAssembly fallback | MIT |
| `renderart-wasm` | 1.0.3 | The WebAssembly core of `renderart` | MIT |
| `upscaler` | 0.4.0 | Pixel-art upscaling, including xBRZ, in WebGL2 and WebAssembly | MIT |
| `virtualized` | 10.1.1 | A fork of react-virtualized for long lists | MIT |
| `sanitizer` | 0.6.0 | Markdown and HTML rendering with sanitization, in WebAssembly | Proprietary |
| `nsfw` | 0.1.4 | NSFW image classification in the browser | Apache-2.0 |
| `nsfw-lite` | 0.5.6 | A smaller NSFW classifier, tuned for pixel art | Apache-2.0 |
| `toxicity` | 1.0.1 | Toxicity classification of text, offline | See the package's model licence |
| `paph-js` | 5.3.0 | PAPH, a perceptual hash for pixel art, to tell a copy from a coincidence | MIT |
| `paph3` | 3.0.1 | The previous version of PAPH | MIT |
| `pixa-vault` | 1.0.4 | Key storage with Argon2id, ChaCha20-Poly1305 and BLAKE3, in WebAssembly | MIT |

## Tools

| Tool | What it does | Where |
|---|---|---|
| `cli_wallet` | Generates keys offline; signs and broadcasts through a node that serves `wallet_bridge_api` | Inside `pixadock/pixagram:1.29.0`; [CLI Wallet](../10-node-operators/cli-wallet.md) |
| `witness-status` | The [witness status page](https://pixagram.com/witness-status/), and a command-line check: `npx github:pixagram-blockchain/witness-status#a376149 --check` exits 0 (healthy), 1 (warning), 2 (critical) or 3 (could not fetch) | [github.com/pixagram-blockchain/witness-status](https://github.com/pixagram-blockchain/witness-status) |
| Price feeds | `bigmac-feed` and its successor, the agnostic feed | [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md#the-agnostic-feed) |
| Docker images | `pixadock/pixagram`, `pixadock/pixagram-haf`, `pixadock/hivemind`, `pixadock/bigmac-feed`, for `linux/amd64` | [Run a Node](../10-node-operators/run-a-node.md) |

## Sources

- **dpixa** 1.5.4 on [npm](https://www.npmjs.com/package/@pixagram/dpixa); source at commit [`fddb47d`](https://github.com/pixagram-blockchain/dpixa/tree/fddb47d677bf6b2364c1a7bcaba704208432071c): options in [`src/client.ts:131-180`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/client.ts#L131-L180); testnet in [`src/client.ts:288-300`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/client.ts#L288-L300) and [`src/parameters.ts`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/parameters.ts); amounts in [`src/chain/asset.ts:86-98`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/chain/asset.ts#L86-L98); broadcast in [`src/helpers/broadcast.ts:312-363`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/helpers/broadcast.ts#L312-L363); witness properties in [`src/utils.ts:207-271`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/utils.ts#L207-L271).
- **Package versions and licences:** `https://registry.npmjs.org/@pixagram/<name>/latest`, read on 2026-10-05. Descriptions from the developer site, [pixa.org](https://pixa.org/library.html).
- **dhive** [1.3.2](https://www.npmjs.com/package/@hiveio/dhive), tested on 2026-10-05.
- **witness-status** at commit [`a376149`](https://github.com/pixagram-blockchain/witness-status/tree/a376149c1c04e97d1b2391d4394699c6dc8c202c): exit codes in its [README](https://github.com/pixagram-blockchain/witness-status/blob/a376149c1c04e97d1b2391d4394699c6dc8c202c/README.md).
