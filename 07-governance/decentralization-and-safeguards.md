# Decentralization and Safeguards

> **Status: Live.** Figures were read at block 979,332 on 2026-10-08, five weeks after genesis. Stake is highly concentrated today. The safeguards below limit what concentrated stake can do, but they do not spread it.

A chain is as decentralized as the stake that elects its witnesses and funds its proposals. This page gives those figures as they stand, explains where they come from, and lists the protocol rules that limit what any holder can do. It also shows how to recompute the figures yourself, and says what is expected to change them.

## The figures on 2026-10-08

| Measure | Value |
|---|---|
| Accounts | 100 |
| Stake held by `pixa.rex` and `pixa.team`, which cannot vote | 72.29% |
| Stake that can vote: outside those two accounts, and matured for 30 days | 27.71% |
| Accounts voting for witnesses | 7, five of them with stake; none through a proxy |
| Their share of the stake that can vote | 49.55% ¹ |
| Share of the stake outside the allocation accounts held by its five largest holders | 93.00% |
| Accounts whose votes on posts move rewards, with more than 2.5 Pixa Power ² | 75 |
| Accounts voting for the one funded DPF proposal | 4 |
| Accounts voting for the DPF's funding threshold | 3, one of them with stake |

1. Down from 85% on 2026-10-05, because the operator's working account `pixa` matured on 2026-10-05 and does not vote; it holds about 40% of the stake that can vote and is powering down ([below](#what-should-change-the-figures)).
2. Hardfork 30 lowered the vote dust threshold from 2,500 to 2.5 Pixa Power on 2026-10-07; before it, 21 accounts cleared the line ([Voting and Curation](../02-social-layer/voting-and-curation.md#from-vote-to-rshares)).

## Where the concentration comes from

The chain is five weeks old, and nearly all of its stake still comes from the genesis allocations ([Genesis and Distribution](../04-tokens-and-economy/genesis-and-distribution.md#where-the-stake-is-now)):

- **The largest holders received allocations.** All nine of the largest holders outside the allocation accounts received their stake from `pixa.rex` or `pixa.team`. Accounts that never received allocation stake hold 0.33% of all stake.
- **The voters came from the team allocation.** The three largest witness voters hold 99.5% of the stake that voted for witnesses. They received it from `pixa.team` on 2026-09-04. The two voters without stake, `tine` and `eddiespino`, hold only delegated stake, which carries no governance weight.
- **One holder has a voice it does not use.** On 2026-10-05 at 18:12 UTC, 10,884,615 VESTS finished their 30-day wait, 10,384,615 of them belonging to `pixa`, the operator's working account. `pixa` holds about 40% of the stake that can vote and casts no governance vote. Its share falls each week as it powers down, 1,153,846 VESTS at a time from 2026-10-10, to nothing by about 2026-12-05.

**Who runs the witnesses.** Witnesses do not have to say who operates them. On 2026-10-08, three of the eight scheduled witnesses gave a pixagram.com address as their website, and five gave the address of the public API node each runs ([Architecture](../18-infrastructure/architecture.md#the-six-public-nodes)). One of them, `rex`, is the account the app uses to open new accounts.

**What this means.** The protocol keeps the powers apart. The allocations cannot vote, the fund has no keys, and the rules change only through the witnesses. Today, though, a small group of accounts that received the team allocation stands behind each of these powers. Those accounts elect every witness, set the DPF's funding threshold and cast most of the votes that move rewards. The separation exists in the code; it does not yet exist in practice.

## Safeguards in the protocol

| Safeguard | What it prevents | Details |
|---|---|---|
| The allocation accounts cannot vote | The genesis stake deciding elections or proposals | [System Accounts](../21-reference/system-accounts.md#restricted-accounts-pixarex-and-pixateam) |
| Stake that is powered up, or received from the allocation accounts, waits 30 days before it counts in governance | Buying or receiving stake and swinging a vote at once. Hive added this rule in answer to the 2020 takeover of Steem's witnesses. | [Pixa Power](../04-tokens-and-economy/pixa-power.md#power-up) |
| Stake leaves over 13 weeks | Voting with stake and leaving at once: a voter stays exposed to the result | [Pixa Power](../04-tokens-and-economy/pixa-power.md#power-down) |
| Votes expire after 365 days without a governance action | Abandoned votes keeping witnesses or proposals in place | [Witnesses and DPoS](witnesses-and-dpos.md#how-witnesses-are-elected) |
| Parameters and the feed are medians across witnesses | One witness setting the account fee, the block size or the conversion price | [Witnesses and DPoS](witnesses-and-dpos.md#what-witnesses-do) |
| Conversions use the median of 3.5 days of feeds | A short-lived false feed moving conversions | [Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed) |
| Rule changes need a supermajority of the witnesses | A minority of witnesses changing the rules | [Protocol Upgrades](protocol-upgrades.md) |
| The fund has no keys and a daily limit of 1% | Anyone spending it without votes, or emptying it quickly | [Decentralized Pixa Fund](decentralized-pixa-fund.md) |
| An account can give up its voting rights for good | Doubt about custodians: an exchange can prove it will never vote with its customers' stake | [Pixa Power](../04-tokens-and-economy/pixa-power.md#giving-up-voting-rights) |

## What the safeguards do not do

- **They do not spread stake.** Only distribution, rewards and new participants do that.
- **They do not separate the people.** When the same accounts elect the witnesses and set the funding threshold, the separation of powers depends on those accounts' restraint.
- **They do not cover the services most people use.** The app at pixagram.com and its account service are run by the operator, Pixa Rex S.A. The chain does not depend on them, and anyone can run a node or build another app ([Who Does What](../01-start-here/who-does-what.md)).

## What should change the figures

| Change | Effect | Enforced by the protocol? |
|---|---|---|
| `pixa` finishes powering down, about 2026-12-05 | Its stake becomes liquid PIXA, to be distributed | The schedule, yes; the distribution, no |
| `pixa.rex` distributes its remaining 59,500,000 VESTS within 9 to 11 years of the TGE | Stake reaches more accounts | No |
| Issuance pays authors and curators about 18,900 PIXA a day | Stake reaches people who publish. Curation follows stake, so it does not spread stake by itself. Since hardfork 30, accounts above 2.5 Pixa Power take part. | Yes |
| Witness pay, 15% of new PIXA since hardfork 30 | Adds to the stake of the eight witness accounts | Yes |
| More witnesses join | Block production spreads; a new witness needs approval from 1% of all stake to be scheduled ([Witnesses and DPoS](witnesses-and-dpos.md#how-witnesses-are-elected)) | — |

This page is updated as the figures move.

## Check the figures yourself

This script needs only Python 3. It reads every account from a public node and prints the main figures:

```python
import json, urllib.request

NODE = "https://api.pixagram.com"
ALLOCATIONS = {"pixa.rex", "pixa.team"}

def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    request = urllib.request.Request(NODE, body, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(request))["result"]

def vests(text):
    return float(text.split()[0])

names, start = [], ""
while True:
    page = rpc("condenser_api.lookup_accounts", [start, 1000])
    names += [n for n in page if n != start]
    if len(page) < 1000:
        break
    start = page[-1]
accounts = [a for i in range(0, len(names), 100)
            for a in rpc("condenser_api.get_accounts", [names[i:i + 100]])]

total = vests(rpc("condenser_api.get_dynamic_global_properties", [])["total_vesting_shares"])
others = [a for a in accounts if a["name"] not in ALLOCATIONS]
own = sorted((vests(a["vesting_shares"]) for a in others), reverse=True)
matured = {a["name"]: vests(a["vesting_shares"]) - sum(int(d["val"]) for d in a["delayed_votes"]) / 1e6
           for a in others}
voters = [a["name"] for a in others if a["witnesses_voted_for"] > 0 or a["proxy"]]

print(f"accounts:                          {len(accounts)}")
print(f"stake in the allocations:          {100 * (total - sum(own)) / total:.2f}%")
print(f"stake that can vote (matured):     {100 * sum(matured.values()) / total:.2f}%")
print(f"witness voters:                    {len(voters)}")
print(f"  their share of the voting stake: {100 * sum(matured[n] for n in voters) / sum(matured.values()):.2f}%")
print(f"top 5 holders, outside allocations: {100 * sum(own[:5]) / sum(own):.2f}%")
```

Run on 2026-10-08 at block 979,332, it printed:

```
accounts:                          100
stake in the allocations:          72.29%
stake that can vote (matured):     27.71%
witness voters:                    7
  their share of the voting stake: 49.55%
top 5 holders, outside allocations: 93.00%
```

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Founding stake | Steem: mined and earned from 2016. Hive: copied from Steem, minus 328 accounts. | Held in two allocation accounts that cannot vote |
| 30-day delay on new governance weight | Hive, since HF24 (2020) | from genesis |
| Votes expire after a year of silence | Hive, since HF25 (2021) | from genesis |
| Hardfork quorum | 17 of 21 | a supermajority of the scheduled witnesses |
| Witnesses | 21 | 8 on 2026-10-08 |

## Sources

- [Hive whitepaper](https://hive.io/whitepaper.pdf), §III.1.1, "Addressing 51% Attacks", on delayed voting as a response to the events of 2020.
- [From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split), with sources for the 2020 events.
- **Code**, at commit [`48f75a2`](https://github.com/pixagram-blockchain/pixagram/tree/48f75a28840c24e5a5b42ccb4f94dc8668ecb443):
  - delayed voting: [delayed_voting.cpp:7-122](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/util/delayed_voting.cpp#L7-L122)
  - vote expiry: [database.cpp:3580-3623](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L3580-L3623)
  - the allocation accounts' restriction: [database.cpp:2762-2810](https://github.com/pixagram-blockchain/pixagram/blob/48f75a28840c24e5a5b42ccb4f94dc8668ecb443/libraries/chain/database.cpp#L2762-L2810)
- **Live chain**, read on 2026-10-08: `condenser_api.get_accounts` for all 100 accounts and `condenser_api.get_witnesses_by_vote` at block 979,332; `database_api.list_witness_votes` and `list_proposal_votes`; the account histories of `pixa.rex` and `pixa.team` (2026-10-05).
