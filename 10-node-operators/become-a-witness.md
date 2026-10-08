# Become a Witness

> **Status: Live.** 8 witnesses on 2026-10-08; up to 21 elected, 1 required. For the `witness` repository at commit `e3b8841`, `pixadock/pixagram:1.30.0`, `pixadock/bigmac-feed:v1.0.3` and the agnostic feed at commit `96b9d4a`. Commands were run on 2026-10-05, except those that need a registered witness.

A witness runs a node that produces blocks in turn, publishes a price feed every hour and asks stakeholders for their votes. What witnesses decide, how they are elected and how they are paid is on [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md). This page is the procedure: keys, node, registration, price feed and upkeep. pixa.org's [node operator guide](https://pixa.org/witness.html) walks through the same setup, together with an API node, from renting the server onward; this page pins the versions and gives the expected output of each step.

## What you commit to

- **A node that never sleeps.** Every block you miss is public and permanent in your `total_missed` count, and missed blocks are not paid.
- **An exact clock.** A slow clock costs the *next* witness its block ([below](#check-the-clock-to-the-millisecond)).
- **A price feed every hour.** Feeds older than 7 days stop counting.
- **Upgrades before hardforks.** After activation, a witness on an older version can no longer produce valid blocks ([Protocol Upgrades](../07-governance/protocol-upgrades.md)).
- **A public page.** Stakeholders vote for people they can identify: say who runs the node, where, and how to reach you.

## Before you start

- **A server** as in [Run a Node](run-a-node.md#what-you-need): 2 vCPU, 4 GB, 50 GB SSD, x86-64. Prefer a provider and a region the other witnesses do not use: a chain is only as resilient as its least diverse failure.
- **An account** with its **active key** at hand. Create it in the app if you have none ([Create an Account](../08-guides/create-an-account.md)).
- **A page** to register as your witness URL, for example a post on Pixagram.

## The two keys

| Key | Signs | Lives in |
|---|---|---|
| **Block-signing key**, new, made in step 1 | Blocks, and `witness_set_properties` updates to your witness's own settings (URL, price feed, parameter votes). It cannot move funds. | `pixagram/config.ini` on the witness server |
| **Active key** of your account | The registration (`witness_update`), the price feed (`feed_publish`) and every transfer | Your password manager, and the feed's `.env` file |

- **Do not mix them up.** The active key in `config.ini` produces no blocks; the signing key in `.env` publishes no feed.
- **Guard both.** Whoever holds the signing key can produce blocks and change your witness's settings in your name. Whoever holds the active key can move your funds. Both files get `chmod 600`, and neither is ever committed or pasted into a chat.
- **The owner key never goes on a server.**

## 1. Create a signing key

Generate it offline, with the wallet inside the node image. Nothing is sent anywhere.

```bash
docker run --rm -it --entrypoint /home/hived/bin/cli_wallet pixadock/pixagram:1.30.0 -o
```

At the `new >>>` prompt, type:

```text
suggest_brain_key
```

Expected output (your values differ):

```json
{
  "brain_priv_key": "<16 words>",
  "wif_priv_key": "5…",
  "pub_key": "PIX…"
}
```

Type `exit` to leave the wallet. Store all three values with your other keys: `wif_priv_key` goes into `config.ini` in step 2, `pub_key` goes on chain in step 4, and the 16 words recreate both. More on the wallet: [CLI Wallet](cli-wallet.md).

## 2. Set up the node

```bash
git clone https://github.com/pixagram-blockchain/witness.git
cd witness
grep 'image: pixadock/pixagram' docker-compose.yml
```

Expected output: the line `image: pixadock/pixagram:1.30.0`, indented. The repository pins every image version; this page describes its commit `e3b8841`.

**Fill in `pixagram/config.ini`.** Near the end, two lines ship commented out, because hived stops with `unable to parse private key` when `private-key =` is present but empty. Open the file with `nano pixagram/config.ini`, remove the `#` from both lines and fill them in:

```ini
witness = "your-account"
private-key = 5…the wif_priv_key from step 1
```

**Protect the file.** It now holds the signing key, and git tracks it as a template. Mark it so that git leaves your copy alone:

```bash
chmod 600 pixagram/config.ini
git update-index --skip-worktree pixagram/config.ini
git ls-files -v pixagram/config.ini
grep -E '^(witness|private-key)[[:space:]]*=' pixagram/config.ini
```

Expected output: `S pixagram/config.ini`, then your two lines.

- **With the mark,** `git status` no longer lists the file, `git add` refuses it, and `git reset --hard` keeps your copy.
- **Without it,** `git reset --hard` replaces your copy with the template. hived reads the file only when it starts, so the node keeps producing until its next restart, perhaps days later, and then stops.
- **When the template changes upstream,** `git pull` stops with `Aborting` and updates nothing, image versions included. Take the change this way, which keeps your key out of git:

  ```bash
  cp pixagram/config.ini ~/config.ini.mine            # your copy, outside the repository
  git update-index --no-skip-worktree pixagram/config.ini
  git checkout -- pixagram/config.ini                 # back to the template
  git pull
  nano pixagram/config.ini                            # fill in the two lines again, from ~/config.ini.mine
  chmod 600 pixagram/config.ini
  git update-index --skip-worktree pixagram/config.ini
  rm ~/config.ini.mine                                # once the node runs on the new file
  ```

**Create `.env` for the price feed,** with your account's **active** key. Use an editor rather than a command line, so the key does not land in your shell history: run `nano .env`, enter these two lines, save, then `chmod 600 .env`.

```ini
WITNESS_ACCOUNT=your-account
WITNESS_WIF=5…your active key
```

**Leave two settings out.** The node that started the chain needed `enable-stale-production = true` and `required-participation = 0` to produce alone. On a node joining a live network, they remove the checks that stop it from building on a stale chain or producing during a network split. The shipped `config.ini` contains neither; keep it that way.

### Check the clock to the millisecond

hived decides when to produce from the system clock, and each slot lasts 3 seconds. If your clock runs a second or two slow, your block reaches your peers during the next witness's slot. That witness has not seen it, produces a competing block at the same height, loses the fork, and the miss is recorded against **it**, not you. Your own count stays clean while you cost the network blocks. On this network, one witness running 2.672 seconds slow caused 121 of 123 same-height collisions.

Install a time daemon as in [Run a Node](run-a-node.md#prepare-the-server), then measure the real offset from the server itself. Comparing `date` over SSH measures your connection, not the clock.

```bash
python3 - <<'PY'
import socket, struct, time, statistics
def probe(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(4)
    try:
        t1 = time.time(); s.sendto(b'\x1b' + 47 * b'\0', (host, 123))
        d, _ = s.recvfrom(1024); t4 = time.time()
    finally:
        s.close()
    u = struct.unpack('!12I', d[:48])
    t2 = u[8] + u[9] / 2**32 - 2208988800
    t3 = u[10] + u[11] / 2**32 - 2208988800
    return ((t2 - t1) + (t3 - t4)) / 2
offsets = []
for host in ('pool.ntp.org', 'time.google.com', 'time.cloudflare.com'):
    for _ in range(3):
        try: offsets.append(probe(host))
        except Exception: pass
print(f'clock offset: {statistics.median(offsets):+.4f}s  ({len(offsets)} samples)'
      if offsets else 'could not reach any NTP server')
PY
```

Expected output: a line such as `clock offset: +0.0031s  (9 samples)`. Under about 50 ms is fine. Past about half a second, you cost your neighbours in the schedule their blocks.

## 3. Start the node and let it sync

Start the node alone; the feed comes in step 5.

```bash
docker compose up -d pixagram
docker compose logs -f pixagram
```

Wait for `entering live mode`, followed by one `Got … transactions on block …` line every 3 seconds ([what the log shows](run-a-node.md#start-a-node-that-follows-the-chain)). Register only once the node is in live mode.

## 4. Register on chain

Registration is one `witness_update` operation, signed with your active key. This script sends it with dpixa through `api.pixagram.com`. Run it on any machine with Node.js 18 or newer:

```bash
mkdir witness-tools && cd witness-tools
npm init -y
npm install @pixagram/dpixa@1.5.4
```

Save as `register-witness.js`, with your values in the first three constants:

```js
// register-witness.js: run once, and again whenever the URL, key or properties change
const { Client, PrivateKey } = require("@pixagram/dpixa/dist/dpixa.js");

const ACCOUNT = "your-account";
const SIGNING_PUB = "PIX…";                          // pub_key from step 1
const URL = "https://pixagram.com/…";                // your witness page

const client = new Client(["https://api.pixagram.com"]);
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  const key = PrivateKey.fromString(process.env.ACTIVE_WIF || ""); // from the environment, never from a file
  const { id } = await client.broadcast.sendOperations([
    ["witness_update", {
      owner: ACCOUNT,
      url: URL,
      block_signing_key: SIGNING_PUB,
      props: { account_creation_fee: "20.000 PIXA", maximum_block_size: 2097152, pxs_interest_rate: 0 },
      fee: "0.000 PIXA",
    }],
  ], key);
  console.log("accepted, transaction", id);
  await sleep(9000);
  const w = await client.call("condenser_api", "get_witness_by_account", [ACCOUNT]);
  console.log("on chain:", w.owner, "signs with", w.signing_key, "url", w.url);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

Run it with the active key read from the keyboard, so the key stays out of your shell history:

```bash
read -rsp 'Active key: ' ACTIVE_WIF && export ACTIVE_WIF && echo
node register-witness.js
unset ACTIVE_WIF
```

Expected output:

```text
accepted, transaction <40 hexadecimal characters>
on chain: your-account signs with PIX… url https://pixagram.com/…
```

| Field | What to put |
|---|---|
| `url` | Your witness page. It cannot be empty. |
| `block_signing_key` | The `pub_key` from step 1 |
| `account_creation_fee` | Your vote for the fee to open an account. The median was 20.000 PIXA on 2026-10-05; the floor is 0.001 PIXA. |
| `maximum_block_size` | Your vote for the block size, from 131072 to 2097152 bytes. Every witness voted 2097152 on 2026-10-05. |
| `pxs_interest_rate` | 0. The chain rejects any other value. |
| `fee` | `0.000 PIXA` |

Your votes for the fee and the block size count through the median of the scheduled witnesses ([account fee](../21-reference/chain-parameters.md#accounts-and-keys), [block size](../21-reference/chain-parameters.md#transaction-and-block-size)).

## 5. Publish the price feed

**PXS promises no price.** Its feed is each witness's statement of how many PIXA one Big Mac costs. The chain takes the median of the witnesses' feeds once an hour, conversions use the median of the last 84 samples, and a feed older than 7 days stops counting ([the rules](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). Until PIXA trades on a market, every feed uses the agreed placeholder price of 0.12 USD for PIXA.

### Today: `bigmac-feed` v1.0.3

The `bigmac-feed` service in the repository reads the US price of a Big Mac from The Economist's index and divides it by `--token-price`, the placeholder. It broadcasts through your own node over Docker's internal network, which is why `config.ini` loads `database_api`, `condenser_api` and `network_broadcast_api`.

**Check the version first.** On 2026-10-05 the repository pins v1.0.2, which reads the January 2026 edition of the index and publishes 51.000 PIXA per PXS. Every live witness publishes 51.833, the value v1.0.3 computes from the July 2026 edition. On the witness server, in the `witness` directory:

```bash
grep 'bigmac-feed:' docker-compose.yml
```

If it prints `v1.0.2`, pin v1.0.3 in `docker-compose.override.yml`, which `git pull` leaves alone:

```yaml
services:
  bigmac-feed:
    image: pixadock/bigmac-feed:v1.0.3
```

Then start the feed:

```bash
docker compose up -d bigmac-feed
docker compose logs -f bigmac-feed
```

Expected output, once an hour:

```text
Big Mac = $6.22 (as of 2026-07-01) → 1 PXS = 51.833 PIXA
Feed published by your-account: 1.000 PXS = 51.833 PIXA
```

### Next: the agnostic feed

The [agnostic feed](https://github.com/pixagram-blockchain/bigmac-feed-agnostic) succeeds `bigmac-feed`. It keeps the same feed orientation and signing, and changes where the inputs come from:

| | `bigmac-feed` v1.0.3 | Agnostic feed |
|---|---|---|
| Big Mac price | The US price, from a pinned edition of the index | The price you observe, in your currency (`bigmac.json`); or any country's, from the latest edition of the index |
| PIXA price | Always `--token-price` | Market pairings (default `coinstore:PXAUSDT`), the median if several; `--token-price` only as a declared placeholder |
| Different currencies | — | Converted with the ECB reference rate, through Frankfurter |
| Protection | — | Moves at most ±50% per publish towards the target (`--max-change`); publishes nothing if any input is missing or absurd |
| Trial run | — | `--dry-run` computes everything and broadcasts nothing |

No published image exists on 2026-10-05. Build it next to the `witness` directory, then return to it:

```bash
cd ..
git clone https://github.com/pixagram-blockchain/bigmac-feed-agnostic.git
git -C bigmac-feed-agnostic checkout -q 96b9d4a      # the version this page describes
docker build -t bigmac-feed-agnostic:local bigmac-feed-agnostic
cd witness
```

**Try it without a key.** With no `bigmac.json`, it uses the US price from the index:

```bash
docker run --rm bigmac-feed-agnostic:local --dry-run --once --witness your-account --token-price 0.12
```

Expected output, after a warning that a placeholder is configured:

```text
Big Mac = 6.22 USD [The Economist index, United States, edition 2026-07-01] | PXA = 0.12 USD [fixed placeholder] → 1 PXS = 51.833 PIXA
DRY RUN — your-account would publish: 1.000 PXS = 51.833 PIXA
```

The dry run reads your current feed from the chain to apply the ±50% limit. For an account that is not yet a witness, the second line reads `ERROR: your-account: read current feed: witness "your-account" not found on chain` instead; add `--max-change 0` to try it before registering.

**Declare the Big Mac you observe.** Create `bigmac.json` in the `witness` directory; the feed reads it again before every publish, so later edits need no restart.

```bash
cat > bigmac.json <<'EOF'
{ "currency": "CHF", "price": "7.30 CHF" }
EOF
docker run --rm -v "$PWD/bigmac.json:/data/bigmac.json:ro" bigmac-feed-agnostic:local \
  --dry-run --once --witness your-account --token-price 0.12
```

Expected output on 2026-10-05; the exchange rate changes daily:

```text
Big Mac = 7.3 CHF [bigmac.json] | PXA = 0.12 USD [fixed placeholder] = 0.0997248 CHF | FX USD→CHF 0.83104 (ECB 2026-10-05) → 1 PXS = 73.201 PIXA
DRY RUN — your-account would publish: 1.000 PXS = 73.201 PIXA
```

Each witness's feed then reflects its own Big Mac, and the chain's median combines them. Create `bigmac.json` before you mount it: if the file is missing, Docker creates a directory in its place and the feed publishes nothing.

**Switch the stack to it.** Replace `docker-compose.override.yml` with:

```yaml
services:
  bigmac-feed:
    image: bigmac-feed-agnostic:local
    command:
      - --witness=${WITNESS_ACCOUNT}
      - --rpc=http://pixagram:7777
      - --token-price=0.12
      - --interval=1h
    volumes:
      - ./bigmac.json:/data/bigmac.json:ro
```

```bash
docker compose up -d bigmac-feed
docker compose logs -f bigmac-feed
```

**When PIXA trades,** remove the `--token-price=0.12` line and run `docker compose up -d bigmac-feed`; `docker compose restart` would keep the old command. The feed then reads the default pairing. While the pairing is not listed, it logs `coinstore PXAUSDT: symbol not listed` and publishes nothing; the chain keeps your previous feed.

## Keep it healthy

- **When your witness is scheduled,** which needs votes from 1% of all Pixa Power ([below](#before-you-announce)), `condenser_api.get_witness_schedule` lists it in `current_shuffled_witnesses`, and the node logs `Generated block #<n> with timestamp <time> at time <time>` at each of its turns. If it logs `Won't produce block because I don't have the private key for PIX…` instead, the key in `config.ini` does not match the one you registered: fix one of them and run `docker compose restart pixagram`.
- **Look daily** at the [witness status page](https://pixagram.com/witness-status/): your missed blocks, your feed's age, your version against the majority.
- **Let a machine watch.** The status project's check exits 0 when everything is healthy, 1 on a warning, 2 on a critical finding and 3 if it cannot fetch. It judges the whole network, so a warning may concern another witness. Run it on a machine that holds no keys, pinned to a version you have read, with Node.js 20 or newer. A cron line can alert you:

  ```bash
  */10 * * * * npx github:pixagram-blockchain/witness-status#a376149 --check >/dev/null 2>&1 || <your alert command>
  ```

- **Your own numbers,** from any machine:

  ```bash
  curl -s -X POST https://api.pixagram.com -H 'Content-Type: application/json' \
    -d '{"jsonrpc":"2.0","method":"condenser_api.get_witness_by_account","params":["your-account"],"id":1}'
  ```

  `total_missed` should stay flat; `running_version` should match the other witnesses.
- **Short maintenance.** Restart right after your node has produced a block, with `docker compose restart pixagram`, so it is back within seconds.
- **Longer maintenance: a standby node.** Run a second synced node with its **own** signing key. Move to it by running `register-witness.js` with the standby's public key, do the work, and move back the same way. Never let two nodes sign with the same key at the same time: that can harm the chain, not just you.
- **Upgrades** follow [Run a Node](run-a-node.md#upgrade-to-a-new-hived-version). Running the new version is how your node signals support for its hardfork.
- **Back up keys, not the chain.** `config.ini`, `.env` and your key store cannot be downloaded again; the chain can.

## Before you announce

- [ ] `get_witness_by_account` shows your signing key and URL, and once you are scheduled, your missed count stays flat.
- [ ] Your feed is published, less than an hour old, and matches the other witnesses' reference.
- [ ] `config.ini` and `.env` are `chmod 600`, backed up, and in no git commit.
- [ ] `timedatectl` reports a synchronized clock, and the offset is under 50 ms.
- [ ] Your witness URL says who runs the node, where, and how to reach you.
- [ ] Something other than you checks the node every ten minutes.

Then ask for votes: tell stakeholders why you run a witness and what you run besides it. They vote as shown in [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md#how-to-vote). Since hardfork 30 your witness is scheduled only once accounts holding at least 1% of all Pixa Power have voted for it, so registering alone produces no blocks ([Witnesses and DPoS](../07-governance/witnesses-and-dpos.md#how-witnesses-are-elected)).

## Sources

- **Repository** [`pixagram-blockchain/witness`](https://github.com/pixagram-blockchain/witness/tree/e3b88414f563e02beff7587a3722d076214652c3) at commit `e3b8841`: [`README.md`](https://github.com/pixagram-blockchain/witness/blob/e3b88414f563e02beff7587a3722d076214652c3/README.md) (keys, clock incident, verification), [`docker-compose.yml`](https://github.com/pixagram-blockchain/witness/blob/e3b88414f563e02beff7587a3722d076214652c3/docker-compose.yml), [`pixagram/config.ini`](https://github.com/pixagram-blockchain/witness/blob/e3b88414f563e02beff7587a3722d076214652c3/pixagram/config.ini).
- **Feeds:** [`bigmac-feed`](https://github.com/pixagram-blockchain/bigmac-feed/tree/c88c43c8b3b8e08ff472fe523b33277b9940ffb2) v1.0.3 at commit `c88c43c` ([`main.go`](https://github.com/pixagram-blockchain/bigmac-feed/blob/c88c43c8b3b8e08ff472fe523b33277b9940ffb2/main.go)); [`bigmac-feed-agnostic`](https://github.com/pixagram-blockchain/bigmac-feed-agnostic/tree/96b9d4a1f1a203d1fedbf603e7769f005c77cfba) at commit `96b9d4a` ([README](https://github.com/pixagram-blockchain/bigmac-feed-agnostic/blob/96b9d4a1f1a203d1fedbf603e7769f005c77cfba/README.md)). Both feed images' log lines were captured on 2026-10-05 without a node; the agnostic feed's dry runs reached `api.pixagram.com` read-only.
- **Registration:** the `witness_update` above, signed by dpixa, matched the public node's serialization (`condenser_api.get_transaction_hex`) on 2026-10-05. Validation of the properties: [`hive_operations.cpp:312-336`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/protocol/hive_operations.cpp#L312-L336) at commit `48f75a2`.
- **Log lines:** [`witness_plugin.cpp:342`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/witness/witness_plugin.cpp#L342), [427](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/witness/witness_plugin.cpp#L427) and [625](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/witness/witness_plugin.cpp#L625).
- **Live values,** 2026-10-05: `condenser_api.get_witnesses_by_vote` and `condenser_api.get_chain_properties`.
- **Monitoring:** [`witness-status`](https://github.com/pixagram-blockchain/witness-status/tree/a376149c1c04e97d1b2391d4394699c6dc8c202c) at commit `a376149`.
- **The same procedure on the developer site:** pixa.org, [Run a Pixagram node](https://pixa.org/witness.html), node operator guide version 1.0, 2026-09-05.
