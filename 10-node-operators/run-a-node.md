# Run a Node

> **Status: Live.** For hived 1.29.0 (`pixadock/pixagram:1.29.0`) and the `witness` repository at commit `5193896`. The commands were run on 2026-10-05; syncing over P2P could not be run from the test machine, and the log lines it prints are quoted from the hived source.

A node is a copy of hived that downloads every block, checks it against the rules and keeps the chain's state. Run one to have your own endpoint, to answer your own queries, or as the base of a witness or an API node. This page sets up a node that follows the chain, explains its plugins and data, and covers replays, upgrades and errors.

| Kind of node | What it adds | Page |
|---|---|---|
| **Follower** | Nothing: it validates and stores the chain, and can answer queries on your machine | this page |
| **Witness** | The `witness` plugin, a signing key and a price feed | [Become a Witness](become-a-witness.md) |
| **API node** | Account history, HAF, Hivemind and a public gateway | [Run an API Node](run-an-api-node.md) |

## What you need

| | Follower or witness | API node |
|---|---|---|
| Processor | 2 vCPU | 4 vCPU |
| Memory | 4 GB | 16 GB |
| Disk | 50 GB SSD | 100 GB SSD |
| System | Linux on x86-64. The images are built for `linux/amd64` only; ARM machines cannot run them. | same |
| Software | Docker Engine with the Compose plugin, and git | same |
| Network | Port 2001/tcp open to the internet | Ports 80, 443, 2001 and 2002 |
| Clock | Synchronized by NTP | same |

The sizes are the repositories' recommendations. Their figures come from the pre-launch network: an API node used 5.4 GB of memory and 5.1 GB of chain data, and a witness node is estimated at 1.0 to 1.5 GB of memory and 0.4 GB of chain data. The chain grows with every block; the margin is for that growth.

## Prepare the server

**1. Install Docker** with Docker's own installer, then let your user run it:

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
# log out and back in, then:
docker compose version
```

Expected output: `Docker Compose version` and a version number. These pages need 2.24.4 or newer; current releases are numbered 5.x.

**2. Check the clock.** A node decides when blocks are due from the system clock.

```bash
timedatectl | grep -E 'synchronized|NTP service'
```

Expected output:

```text
System clock synchronized: yes
              NTP service: active
```

If either line says otherwise, install a time daemon. Debian cloud images often ship without one.

```bash
sudo apt-get update && sudo apt-get install -y chrony
sudo systemctl enable --now chrony
```

For a witness the clock matters more, because each block slot lasts only 3 seconds ([Become a Witness](become-a-witness.md)).

**3. Open port 2001/tcp** for peer-to-peer traffic, in your provider's firewall and in the server's own. The node also connects out to its seed, `api.pixagram.com:2001`.

## Start a node that follows the chain

The `witness` repository is the smallest stack that joins the network. Without a witness name and key, its node follows the chain and produces nothing.

```bash
git clone https://github.com/pixagram-blockchain/witness.git pixa-node
cd pixa-node
grep 'image: pixadock/pixagram' docker-compose.yml
```

Expected output: the line `image: pixadock/pixagram:1.29.0`, indented.

Start only the node, not the price feed:

```bash
docker compose up -d pixagram
docker compose logs -f pixagram
```

Compose warns that `WITNESS_ACCOUNT` and `WITNESS_WIF` are not set. They configure the price feed, which a follower does not run; ignore the warnings.

What the log shows, in order (`<…>` stands for values that change):

```text
P2P adding seed node <address>:2001
Syncing Blockchain --- Got block: #<n> time: <time> producer: <witness> …
entering live mode
Got <n> transactions on block <n> by <witness> -- Block Time Offset: <ms> ms
```

The *Syncing* lines repeat until the node has every block. The chain is young, so this takes minutes. After `entering live mode`, one *Got … transactions* line arrives every 3 seconds. Press Ctrl+C to stop following the log; the node keeps running.

The node restarts by itself after a reboot (`restart: unless-stopped`).

## Query it from the same machine

The node's API listens on port 7777 inside Docker's network only. To query it from the host, create `docker-compose.override.yml` next to `docker-compose.yml`:

```yaml
services:
  pixagram:
    ports:
      - "127.0.0.1:7777:7777"
```

```bash
docker compose up -d pixagram
curl -s -X POST http://127.0.0.1:7777 -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_dynamic_global_properties","params":[],"id":1}'
```

- **Compare** its `head_block_number` with the same call to `https://api.pixagram.com`. They should differ by a block or two at most.
- **Field names are Hive's** on a node without the gateway: `hbd_balance`, not `pxs_balance` ([why](../09-developers/differences-from-hive.md#talking-to-hived-directly)).
- **Keep `127.0.0.1:`** in the mapping. Without it, Docker publishes the port to the internet, past the server's own firewall.

## Choose the plugins

The `plugin` line of `pixagram/config.ini` decides what the node indexes and which calls it answers.

| Purpose | `plugin =` | What it adds |
|---|---|---|
| Follow the chain, broadcast, produce blocks (the `witness` repository) | `witness database_api condenser_api network_broadcast_api` | Chain state and broadcasting. `witness` produces nothing without a name and key. |
| Use the [CLI wallet](cli-wallet.md) against your node | add `wallet_bridge_api` | The API the wallet needs. Starts without a replay. |
| Serve history and profiles (the `pixagram-node` repository) | `metadata account_history_rocksdb account_history_api database_api account_by_key_api network_broadcast_api reputation_api market_history_api condenser_api block_api rc_api` | Account history, key lookups, profiles, reputation, the internal market |

- **Plugins with their own index need a replay.** `metadata`, `account_history_rocksdb`, `account_by_key`, `reputation` and `market_history` build indexes from the blocks. Adding one to a node that has already synced needs the replay below, or hived stops with ``Inconsistency occurs. A new index is created, but other indexes are found in `shared_memory_file` file. A replay is needed.``
- **Account history is most of the disk.** It measured 1.2 GB of a 1.57 GB data directory. A witness answers no history queries and should not load it.
- **Profiles need `metadata`.** Without it, account profiles read back empty.

## What the node keeps

The data directory is `pixagram/` in the repository, mounted into the container.

| Path | What it is | Back it up? |
|---|---|---|
| `pixagram/config.ini` | The node's settings, and on a witness its signing key | **Yes.** It cannot be rebuilt. |
| `pixagram/blockchain/block_log*` | Every block. The chain itself. | No; download it again. **Never delete it** on a node you keep. |
| `pixagram/blockchain/shared_memory.bin` | The current state, rebuilt from the block log by a replay | No |
| `pixagram/blockchain/*-rocksdb-storage` | Archived comments and, with the history plugin, account history | No |
| `pixagram/p2p/`, `pixagram/*.log` | Peer list and logs | No |

## Run it day to day

```bash
docker compose ps                    # what is running
docker compose logs -f pixagram      # follow the log; Ctrl+C stops following
docker compose restart pixagram      # after editing config.ini
docker compose down                  # stop; the data stays on disk
df -h . && du -sh pixagram/blockchain   # the chain only grows
```

## Replay and resync

**Replay** rebuilds the state from your own block log. Use it after adding an indexing plugin, or when hived reports `Error: Headblock and statefile are inconsistent, need to start hived with --replay-blockchain`.

```bash
docker compose down
rm -f pixagram/blockchain/shared_memory.bin
HIVED_EXTRA_ARGS=--replay-blockchain docker compose up -d pixagram
docker compose logs -f pixagram      # wait for "entering live mode"
docker compose up -d pixagram        # back to normal start-up arguments
```

On a node with account history, also remove `pixagram/blockchain/account-history-rocksdb-storage` and `pixagram/blockchain/comments-rocksdb-storage` before the replay.

**Resync** downloads the chain again from genesis. It keeps `config.ini`.

```bash
docker compose down
sudo rm -rf pixagram/blockchain pixagram/p2p pixagram/logs pixagram/*.log
docker compose up -d pixagram
```

## Upgrade to a new hived version

A new version arrives as a new image tag in the repository's `docker-compose.yml`. hived records its build in `shared_memory.bin` and refuses a state file written by another version, with `Blockchain config from shared memory file mismatch current version of app.` The first start on the new image is therefore a forced replay of your block log:

```bash
git pull
grep 'image: pixadock/pixagram' docker-compose.yml   # must show the new tag
docker compose pull pixagram
docker compose stop pixagram
HIVED_EXTRA_ARGS="--force-replay --exit-before-sync" docker compose run --rm --no-deps pixagram
docker compose up -d pixagram
```

The one-off container rebuilds the state and exits; the last line starts the node normally. For hardfork 29 the replay took about 20 seconds.

**If `git pull` stops with `Aborting`,** you have changed a file that the update also changes, usually `config.ini`, and nothing was updated. Do not continue with the old tag: reconcile your local change with the update, keeping any secret out of the repository, then run the commands again.

**Upgrade before a hardfork activates.** After activation, a node on an older version can no longer follow the chain ([Protocol Upgrades](../07-governance/protocol-upgrades.md#how-a-hardfork-activates)).

## When something is wrong

| You see | It means | Do this |
|---|---|---|
| `Permission denied` at start | The data directory is not owned by the container's user | `sudo chown -R 1000:1000 ./pixagram` |
| `Error: Headblock and statefile are inconsistent …` | The state file does not match the block log | [Replay](#replay-and-resync) |
| `Inconsistency occurs. A new index is created …` | A plugin was added and the old state file kept | Delete `shared_memory.bin`, then replay |
| `Blockchain config from shared memory file mismatch current version of app.` | The image changed version | The [forced replay](#upgrade-to-a-new-hived-version) |
| No *Syncing* lines, head block stuck at 0 | The node cannot reach a peer | Check that `p2p-seed-node = api.pixagram.com:2001` is in `config.ini` and that outbound port 2001 is open |
| Disk almost full | The chain or the logs grew | Resize the volume. Never delete the block log. |

## Sources

- **Repository** [`pixagram-blockchain/witness`](https://github.com/pixagram-blockchain/witness/tree/51938966c3714908a10f158be197064c2d16d94b) at commit `5193896`: [`README.md`](https://github.com/pixagram-blockchain/witness/blob/51938966c3714908a10f158be197064c2d16d94b/README.md) (sizing, clock, ports, replay, upgrade), [`docker-compose.yml`](https://github.com/pixagram-blockchain/witness/blob/51938966c3714908a10f158be197064c2d16d94b/docker-compose.yml) and [`pixagram/config.ini`](https://github.com/pixagram-blockchain/witness/blob/51938966c3714908a10f158be197064c2d16d94b/pixagram/config.ini).
- **API node plugins:** [`pixagram-node/pixagram/config.ini`](https://github.com/pixagram-blockchain/pixagram-node/blob/7e57cca075d51a3ac1cf3065d367581a3efe56c6/pixagram/config.ini) and its [README](https://github.com/pixagram-blockchain/pixagram-node/blob/7e57cca075d51a3ac1cf3065d367581a3efe56c6/README.md) at commit `7e57cca`.
- **Log lines,** at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443): *Syncing* and *entering live mode* in [`chain_plugin.cpp:686-687`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/chain/chain_plugin.cpp#L686-L687) and [1991-1997](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/chain/chain_plugin.cpp#L1991-L1997); *Got … transactions* in [`p2p_plugin.cpp:169`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/p2p/p2p_plugin.cpp#L169); the replay options in [`chain_plugin.cpp:1518-1525`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/plugins/chain/chain_plugin.cpp#L1518-L1525); the state-file errors in [`database_exceptions.hpp:90-91`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/include/hive/chain/database_exceptions.hpp#L90-L91) and [`chainbase.hpp:1416`](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chainbase/include/chainbase/chainbase.hpp#L1416).
- **Tests on 2026-10-05:** the image's platforms (`docker buildx imagetools inspect`); the stack above started with the override, answering on `127.0.0.1:7777`; `wallet_bridge_api` added to a started node without a replay.
