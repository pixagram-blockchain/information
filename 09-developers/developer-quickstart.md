# Developer Quickstart

> **Status: Live.** Steps 1 to 4 were run on 2026-10-05 with Node.js 22.22 and `@pixagram/dpixa` 1.5.4 against `api.pixagram.com`. Step 5 broadcasts a real vote, so it needs your own account and key; its parts were checked separately (see [Sources](#sources)).

This page takes you from nothing to reading the chain, saving an artwork and signing a vote, in five steps. It assumes you know JavaScript and JSON-RPC, not Hive. If you know Hive, read [Differences from Hive](differences-from-hive.md) next.

## Before you start

- **Endpoints.** Six public API nodes serve the same chain: `https://api.pixagram.com`, `https://pixarex.net`, `https://merlion.surf`, `https://blockforge.lol`, `https://boitata.quest` and `https://pixa-dubai.xyz`. All accept browser requests from any origin.
- **There is no testnet.** Every transaction you broadcast is real and stays in the chain forever ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)). Test with a small account.
- **Use the weakest key that works.** The posting key votes, posts and follows; the active key moves funds; the owner key is never needed by code ([Keys](../11-reference/glossary.md#keys)). Pass keys through environment variables. Never write one into a file or a repository. The examples use placeholders such as `5K...`.
- **Requests are limited to about 1 MiB** by the public nodes ([Chain Parameters](../11-reference/chain-parameters.md#transaction-and-block-size)).

## 1. One request with curl

```bash
curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_dynamic_global_properties","params":[],"id":1}'
```

Expected output, shortened; the values change with every block:

```json
{"jsonrpc":"2.0","result":{"head_block_number":901965,"head_block_id":"…","time":"2026-10-05T20:29:48","current_witness":"matus", … ,"current_supply":"100660263.344 PIXA","init_pxs_supply":"0.000 PXS","current_pxs_supply":"251649.961 PXS","total_vesting_fund_pixa":"…", …},"id":1}
```

The API is Hive's JSON-RPC. Field names that Hive spells with `hbd` or `hive` come back with `pxs` or `pixa`, because the public nodes rename them ([why](differences-from-hive.md#field-renames)).

## 2. Set up a Node.js project

```bash
mkdir pixa-quickstart && cd pixa-quickstart
npm init -y
npm install @pixagram/dpixa@1.5.4
```

**Load the bundle, not the package name.** In version 1.5.4 the package's entry point names a file that is not published. In Node, `require("@pixagram/dpixa")` and `import { Client } from "@pixagram/dpixa"` both fail with `Cannot find module …/lib/index-node`. Load the bundled build instead:

```js
// CommonJS
const { Client, PrivateKey } = require("@pixagram/dpixa/dist/dpixa.js");

// ES modules
import dpixa from "@pixagram/dpixa/dist/dpixa.js";
const { Client, PrivateKey } = dpixa;
```

Bundlers such as webpack, and browsers loading `https://unpkg.com/@pixagram/dpixa@1.5.4/dist/dpixa.js`, use the bundle already.

## 3. Read the chain

Save as `read.js`:

```js
// read.js: three reads through the public API
const { Client } = require("@pixagram/dpixa/dist/dpixa.js");

const client = new Client([
  "https://api.pixagram.com",
  "https://pixarex.net",
  "https://merlion.surf",
]);

async function main() {
  const props = await client.database.getDynamicGlobalProperties();
  console.log("head block", props.head_block_number, "produced by", props.current_witness);

  const [fund] = await client.database.getAccounts(["pixa.omnibus"]);
  console.log("pixa.omnibus holds", fund.balance, "and", fund.pxs_balance);

  const posts = await client.pixamind.getRankedPosts({ sort: "created", tag: "", limit: 5 });
  for (const p of posts) {
    const kind = p.json_metadata.format === "image" ? "artwork" : "text post";
    console.log(`@${p.author}/${p.permlink}: ${kind}, body ${p.body.length} characters`);
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

```bash
node read.js
```

Expected output on 2026-10-05:

```text
head block 901862 produced by top.witness
pixa.omnibus holds 0.000 PIXA and 249295.022 PXS
@mathiew/not-a-bank-robber-1791222997311: artwork, body 25027 characters
@tetiana/schwyz-1791219064927: artwork, body 32547 characters
@retro/peach-knight-1791211388189: artwork, body 23371 characters
@mrdragon/mr-dragon-is-here-1791210562903: artwork, body 11883 characters
@matus/myocastor-coypus-1791149708674: artwork, body 29119 characters
```

- `client.database` calls go to hived; `client.pixamind` calls (`bridge.*`) go to Hivemind ([Chain Architecture](chain-architecture.md#how-a-read-travels)).
- `pixa.omnibus` is the keyless treasury of the [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md).
- With several nodes in the list, the client moves to the next one when a node cannot be reached.

## 4. Save an artwork

An artwork's body is the image itself: a lossless WebP file, base64-encoded as a data URI ([Artwork Encoding Spec](artwork-encoding-spec.md)). Save as `artwork.js`:

```js
// artwork.js: save the newest artwork as a WebP file
const fs = require("fs");
const { Client } = require("@pixagram/dpixa/dist/dpixa.js");

const client = new Client(["https://api.pixagram.com"]);
const PREFIX = "data:image/webp;base64,";

async function main() {
  const posts = await client.pixamind.getRankedPosts({ sort: "created", tag: "", limit: 20 });
  const art = posts.find((p) => p.json_metadata.format === "image" && p.body.startsWith(PREFIX));
  const bytes = Buffer.from(art.body.slice(PREFIX.length), "base64");

  // A lossless WebP starts with RIFF, WEBP and VP8L, then packs width − 1 and height − 1 in 14 bits each.
  if (bytes.toString("ascii", 0, 4) !== "RIFF" || bytes.toString("ascii", 8, 16) !== "WEBPVP8L") {
    throw new Error("not a lossless WebP");
  }
  const bits = bytes.readUInt32LE(21);
  const width = (bits & 0x3fff) + 1;
  const height = ((bits >>> 14) & 0x3fff) + 1;

  fs.writeFileSync("artwork.webp", bytes);
  console.log(`@${art.author}/${art.permlink}: ${width} x ${height} px, ${bytes.length} bytes, saved as artwork.webp`);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

```bash
node artwork.js
```

Expected output on 2026-10-05:

```text
@mathiew/not-a-bank-robber-1791222997311: 194 x 258 px, 18752 bytes, saved as artwork.webp
```

Open `artwork.webp` in any image viewer. It is the original, at its own size; the app only enlarges it on screen.

## 5. Sign and broadcast a vote

Save as `vote.js`:

```js
// vote.js: sign a vote with your posting key, broadcast it, wait for its block
const { Client, PrivateKey } = require("@pixagram/dpixa/dist/dpixa.js");

const client = new Client(["https://api.pixagram.com"]);
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  const [voter, author, permlink] = process.argv.slice(2);
  const key = PrivateKey.fromString(process.env.POSTING_WIF || ""); // from the environment, never from a file

  const { id } = await client.broadcast.vote({ voter, author, permlink, weight: 10000 }, key);
  console.log("accepted, transaction", id);

  for (let attempt = 0; attempt < 10; attempt++) {
    await sleep(3000);
    try {
      const tx = await client.call("condenser_api", "get_transaction", [id]);
      console.log("included in block", tx.block_num);
      return;
    } catch (e) {
      // "Unknown Transaction" until a block holds it
    }
  }
  throw new Error("not in a block after 30 seconds");
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

Run it with your account and a post you want to upvote. Read the posting key from the keyboard, so it stays out of your shell history:

```bash
read -rsp 'Posting key: ' POSTING_WIF && export POSTING_WIF && echo
node vote.js your-account author permlink
unset POSTING_WIF
```

Expected output: two lines, the second within a few seconds.

```text
accepted, transaction <40 hexadecimal characters>
included in block <block number>
```

- **What happens.** The library reads the head block, builds the transaction, signs it locally and sends it with `condenser_api.broadcast_transaction`. Your key never leaves your machine.
- **What "accepted" means.** The broadcast call returns as soon as the node accepts the transaction, with only its `id`. It does not wait for a block, so the script asks `condenser_api.get_transaction` until a block holds it.
- **What the vote does.** `weight` runs from −10000 (full downvote) to 10000 (full upvote). A full-strength vote spends 2% of your voting mana, and it moves rewards only if you hold more than about 2,500 Pixa Power ([why](../02-social-layer/voting-and-curation.md#why-small-votes-count-for-nothing)).

## 6. When a call fails

| You see | Cause | What to do |
|---|---|---|
| `Cannot find module …/lib/index-node` | dpixa 1.5.4's package entry point | Load `@pixagram/dpixa/dist/dpixa.js` ([step 2](#2-set-up-a-nodejs-project)) |
| `private key network id mismatch` | `POSTING_WIF` is empty, or not a private key in WIF form | Export the key; a WIF starts with `5` |
| `missing required posting authority … Missing Posting Authority your-account` | The key is not this account's posting key, or the text in your transaction contains a name the public nodes rename ([known issue](differences-from-hive.md#known-issue-renames-inside-text)) | Check the key; check the text |
| `Unable to acquire database lock` | The node was busy | Retry the call |
| `Could not find API bridge` | A batch request that mixes chain calls with social calls | Send `bridge.*` calls in their own requests ([batches](differences-from-hive.md#batches-ids-and-limits)) |
| `id required` | A batch request whose first call is a social call | Same |
| HTTP 413 | The request is larger than about 1 MiB | Make the artwork smaller |
| `Invalid asset symbol: PXS` | A Hive library parsing a Pixa amount | Use dpixa ([SDKs and Libraries](sdks-and-libraries.md)) |

## Next steps

- [Artwork Encoding Spec](artwork-encoding-spec.md): publish an artwork that the Pixagram app displays.
- [Differences from Hive](differences-from-hive.md): everything that differs from Hive's documentation.
- [SDKs and Libraries](sdks-and-libraries.md): dpixa's API, its quirks, and the other `@pixagram` packages.
- [Run a Node](../10-node-operators/run-a-node.md): your own endpoint.
- The [Hive developer portal](https://developers.hive.io/) documents every operation and API call. They apply here, with PIXA for HIVE and PXS for HBD.

## Sources

- **Library:** [`@pixagram/dpixa` 1.5.4](https://www.npmjs.com/package/@pixagram/dpixa), source at commit [`fddb47d`](https://github.com/pixagram-blockchain/dpixa/tree/fddb47d677bf6b2364c1a7bcaba704208432071c); the broadcast call is in [`src/helpers/broadcast.ts:312-363`](https://github.com/pixagram-blockchain/dpixa/blob/fddb47d677bf6b2364c1a7bcaba704208432071c/src/helpers/broadcast.ts#L312-L363).
- **Checks for step 5,** on 2026-10-05: a vote signed by dpixa produced the same digest as the node's own serialization (`condenser_api.get_transaction_hex`); `condenser_api.get_transaction` returned the `block_num` of a known transaction; a wrongly signed vote sent to a local 1.29.0 node returned the `Missing Posting Authority` error above. No transaction was broadcast to the network.
- **Errors:** observed against `api.pixagram.com` on 2026-10-05, except the last, from `@hiveio/dhive` 1.3.2.
