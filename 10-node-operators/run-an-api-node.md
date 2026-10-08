# Run an API Node

> **Status: Live.** For the `pixagram-node` repository at commit `4a271e8`: hived and HAF 1.30.0, Hivemind `mainnet`. The six public nodes behaved as this stack does when checked on 2026-10-05. The full stack could not be run on the test machine; its configuration was checked with `docker compose config`.

An API node serves the chain to apps: balances, history, feeds, communities. The Pixagram app works only through API nodes, so each new one adds capacity and a place to fail over to, and a node near its users makes the app faster for them. This page sets one up, explains what each part does, and covers its ports, upgrades and the gateway's behaviour. An API node produces no blocks; for that, see [Become a Witness](become-a-witness.md).

## What the stack runs

```text
Internet → Caddy (TLS) → Jussi (routing, renames) → hived  (chain calls)
                                                  → Hivemind (social calls) ← HAF (hived + PostgreSQL)
```

| Service | Image | Job |
|---|---|---|
| `pixagram` | `pixadock/pixagram:1.30.0` | hived with the chain API plugins and account history |
| `pixagram_haf` | `pixadock/pixagram-haf:1.30.0` | A second hived that writes every block into PostgreSQL |
| `hivemind_setup` | `pixadock/hivemind:mainnet` | Creates Hivemind's schema and roles, once |
| `hivemind_sync` | `pixadock/hivemind:mainnet` | Indexes blocks from HAF |
| `hivemind` | `pixadock/hivemind:mainnet` | Serves `bridge.*`, `follow_api.*`, `tags_api.*` |
| `jussi` | `openresty/openresty:alpine` | Routes each call and renames fields ([Differences from Hive](../09-developers/differences-from-hive.md#the-public-api)) |
| `ssl-proxy` | `caddy:alpine` | TLS, certificates, compression |
| `init_permissions` | `alpine:3.20` | Fixes file ownership, once |

[Chain Architecture](../09-developers/chain-architecture.md) explains how a call travels through them.

## Size the server

**Recommended: 4 vCPU, 16 GB of memory, 100 GB SSD,** on Linux x86-64 ([Run a Node](run-a-node.md#what-you-need)). On the pre-launch network the stack used 5.4 GB of memory and 0.21 vCPU when idle, 2.46 vCPU at peak during the first sync, and about 15 GB of disk with its images.

**Retune PostgreSQL below about 24 GB of memory.** HAF ships PostgreSQL configured for Hive's full chain, with 16 GiB of shared buffers, and PostgreSQL does not start if it cannot reserve them. The repository has an override directory, mounted and read last; [Set it up](#set-it-up) creates the file there before the first start.

## Before you start

1. **Prepare the server** as in [Run a Node](run-a-node.md#prepare-the-server): Docker, a synchronized clock.
2. **Open ports** 80, 443, 2001 and 2002 (TCP) in your provider's firewall.
3. **Point a name at the server.** At your domain registrar, create an A record such as `api.example.com` with the server's IPv4 address, and wait until it resolves:

   ```bash
   dig +short api.example.com
   ```

   Expected output: the server's address. Caddy requests a certificate as soon as it starts, and failed requests count against the domain's limits at Let's Encrypt.

## Set it up

```bash
git clone https://github.com/pixagram-blockchain/pixagram-node.git
cd pixagram-node

echo 'SITE_ADDRESS=api.example.com' > .env
chmod 600 .env
```

If the server has less than about 24 GB of memory, retune PostgreSQL now ([why](#size-the-server)); raise the values in proportion on a larger machine:

```bash
cat > pixagram-haf/haf_postgresql_conf.d/local.conf <<'EOF'
shared_buffers = 2GB
effective_cache_size = 4GB
maintenance_work_mem = 512MB
EOF
```

Then start everything:

```bash
docker compose up -d
docker compose logs -f pixagram_haf
```

- **Without `SITE_ADDRESS`** Caddy serves plain HTTP on port 80 and requests no certificate. The default is deliberate: a template that names a real domain would make every unedited copy request certificates it cannot obtain.
- **The first sync** pulls the chain over P2P twice, once for hived and once for HAF, and indexes it into PostgreSQL and Hivemind.
- **`hivemind_setup` runs once** and must exit with code 0 before `hivemind_sync` and `hivemind` start. Do not restart the stack while it runs.
- **Jussi may restart for up to a minute** after a cold start. It looks up Hivemind's address when it loads its configuration and fails while Hivemind is still starting; its restart policy brings it back.

## Close the local ports

`docker-compose.yml` publishes four ports meant for the machine itself on **every** interface: hived's HTTP (7777), Hivemind (7778), HAF's HTTP (7779) and HAF's websocket (8092). Docker writes its own firewall rules, so the server's firewall (`ufw`, for example) does not close them. Either block them in your provider's firewall, or bind them to the machine itself with `docker-compose.override.yml`:

```yaml
services:
  pixagram:
    ports: !override
      - "127.0.0.1:7777:7777"
      - "2001:2001"
  pixagram_haf:
    ports: !override
      - "127.0.0.1:7779:7778"
      - "127.0.0.1:8092:8092"
      - "2002:2002"
  hivemind:
    ports: !override
      - "127.0.0.1:7778:8080"
```

```bash
docker compose up -d
```

`!override` replaces the port list instead of adding to it, and needs Docker Compose 2.24.4 or newer. An override file is not tracked by git, so `git pull` leaves it alone.

| Port | Open to | Purpose |
|---|---|---|
| 80, 443 | everyone | The public API, and certificate renewal |
| 2001 | everyone | hived's peers |
| 2002 | everyone | HAF's peers |
| 7777, 7778, 7779, 8092 | this machine only | Direct access to hived, Hivemind and HAF, bypassing the gateway |

## Check that it serves

From any machine:

```bash
# the chain layer
curl -s -X POST https://api.example.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"condenser_api.get_dynamic_global_properties","params":[],"id":1}'

# the social layer
curl -s -X POST https://api.example.com -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"bridge.get_ranked_posts","params":{"sort":"created","tag":"","limit":1},"id":1}'
```

- The first call's `head_block_number` should match `https://api.pixagram.com` within a block or two, and its fields should read `current_pxs_supply`, not `current_hbd_supply`. That shows the gateway's renames work.
- The second call should return one post.
- Hivemind's own progress is in PostgreSQL. On a healthy node it equals the head block:

  ```bash
  docker compose exec pixagram_haf psql -U haf_admin -d haf_block_log -tAc \
    'SELECT last_completed_block_num FROM hivemind_app.hive_state'
  ```

## What the gateway changes

Jussi renames Hive's field names to Pixa's in every response, and some of them back in requests ([the full list](../09-developers/differences-from-hive.md#field-renames)). Two consequences matter to operators:

- **Clients expect the same API on every public node.** Change `jussi/nginx.conf` through the repository, so that every node changes together, not on one node alone.
- **The renames apply to the whole body, text included.** Until that is fixed, a transaction whose text contains a renamed name fails to broadcast through any node running this gateway ([known issue](../09-developers/differences-from-hive.md#known-issue-renames-inside-text)).

## Run it day to day

```bash
docker compose ps                         # all long-running services should be "running"
docker compose logs -f hivemind_sync      # indexing progress
docker compose restart jussi              # if bridge.* calls return 502
```

- **After a reboot** every long-running service starts again by itself (`restart: unless-stopped`). `init_permissions` and `hivemind_setup` stay stopped; they run once.
- **Keep `.env` and the data directories out of git.** The repository's `.gitignore` covers them; the data directories hold your peer list and logs.
- **If `Permission denied` appears at start,** run the stack's own ownership fix again: `docker compose run --rm init_permissions`. Do not `chown` all of `./pixagram-haf` yourself: PostgreSQL's data in `pixagram-haf/haf_db_store` must keep its own owner, and the fix leaves it alone.

## Upgrade

A new hived version needs a replay of the consensus node, and HAF and Hivemind rebuilt from scratch, because HAF cannot replay into a database that already holds blocks. The whole chain resyncs in minutes. The repository's README gives these steps for the move to 1.30.0 at hardfork 30 (2026-10-07); a node left on 1.29.0 applies the old rules from block 949,330 and drifts from the network.

```bash
git pull
docker compose pull pixagram pixagram_haf

# 1. hived: rebuild the state from the block log, then start normally
docker compose stop pixagram
HIVED_EXTRA_ARGS="--force-replay --exit-before-sync" docker compose run --rm --no-deps pixagram
docker compose up -d pixagram

# 2. HAF and Hivemind: drop their derived data and resync them together
docker compose stop pixagram_haf hivemind_sync hivemind hivemind_setup
docker compose rm -f pixagram_haf hivemind_sync hivemind hivemind_setup
sudo rm -rf pixagram-haf/haf_db_store pixagram-haf/blockchain pixagram-haf/logs pixagram-haf/p2p
docker compose up -d

# 3. Jussi keeps Hivemind's old address and answers 502 on bridge.* until restarted
docker compose restart jussi
```

- HAF is healthy within a few minutes; `hivemind_sync` logs live blocks after 10 to 15 minutes.
- Start Hivemind together with HAF, as above. Started against a HAF that has already synced, its hand-over to live indexing has failed on `hive_notification_cache_pkey`.
- The `rm -rf` line keeps `pixagram-haf/haf_postgresql_conf.d/` and your `local.conf`.

## Get listed

Once both checks pass, ask the maintainers to add your node to the app's node list ([`DEFAULT_NODES`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/constants.js#L94)), and name it on your witness page if you run one. A node in a region the others do not cover, such as Africa or South Asia on 2026-10-05, helps users there most.

## Sources

- **Repository** [`pixagram-blockchain/pixagram-node`](https://github.com/pixagram-blockchain/pixagram-node/tree/4a271e879818b194ffbef57b8efc5744151017c4) at commit `4a271e8`: [`README.md`](https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/README.md) (sizing, PostgreSQL, setup, verification, restarts, upgrade), [`docker-compose.yml`](https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/docker-compose.yml) (services and published ports), [`ssl-proxy/Caddyfile`](https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/ssl-proxy/Caddyfile) and [`jussi/nginx.conf`](https://github.com/pixagram-blockchain/pixagram-node/blob/4a271e879818b194ffbef57b8efc5744151017c4/jussi/nginx.conf).
- **Override syntax:** Docker's [Merge Compose files](https://docs.docker.com/reference/compose-file/merge/) (`!override` requires Compose 2.24.4); the override above checked with `docker compose config` on 2026-10-05.
- **Public nodes:** the gateway's renames, request limit, compression and method list, compared on all six on 2026-10-05; locations from the app's node list.
