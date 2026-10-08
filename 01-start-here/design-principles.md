# Design Principles

> **Status: Live.** These principles describe the network as it runs today. Where the network falls short of one, the page says so. Last checked 2026-10-05.

Pixagram inherits its founding ideas from Steem and adds a few of its own. Each principle below gives the idea, how the chain puts it into practice, and where that practice is still incomplete. The aim is a list readers can hold the project to.

## Three principles inherited from Steem

The Steem whitepaper opens with three principles:

1. Everyone who contributes to a venture should receive a share of it.
2. All forms of capital are equally valuable. Time and attention spent producing and curating are worth as much as money: this is *sweat equity*.
3. A community creates value to serve its own members.

Pixagram keeps all three and sharpens the first two.

## The principles

### 1. Contribution earns a share; holding earns nothing

**Idea.** New tokens go to the people who do the work: artists who publish, curators who find good work early, witnesses who run the network, and proposals the community funds.

**In the protocol.** New PIXA is issued every block and split between the reward fund, the witnesses and the [Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md). Pixa removed both of Hive's rewards for passive holding: interest on the debt-style token, and the share of issuance paid to stake. The only reward stake earns is curation, which requires voting ([Issuance](../21-reference/chain-parameters.md#issuance)).

**Still incomplete.** A vote moves rewards only once an account holds more than 2,500 Pixa Power. Small accounts can publish and earn, but not yet curate ([Voting and Curation](../02-social-layer/voting-and-curation.md)).

### 2. The work is the record

**Idea.** An artwork should not depend on a server staying online.

**In the protocol.** The app writes each artwork into its post as a lossless WebP image, so the image travels with the chain's history. The author's signature and the block's time record who published what, and when ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)).

**Still incomplete.** Images inside blog posts are links to files stored elsewhere. Provenance shows who posted a work first, not who made it.

### 3. Participation should not cost a fee

**Idea.** In the Steem whitepaper's words, "micropayments don't work." Asking someone to pay for every like or post drives them away.

**In the protocol.** Most operations draw on [Resource Credits](../04-tokens-and-economy/resource-credits.md), which recharge from stake.

**Still incomplete.** Three operations keep a fee, each to deter abuse: opening an account, creating a proposal, and converting PIXA into PXS ([list](../21-reference/chain-parameters.md#figures-you-may-meet-elsewhere)).

### 4. Promise less, and say what is true

**Idea.** A system that promises a fixed value has to defend it, and defences fail. Pixa's second token, PXS, promises no price. Under stress it settles for less rather than defending a number ([PXS at a Glance](../05-pixa-supra/pxs-at-a-glance.md)).

**Applied to documentation.** The same rule applies to the project's own documents: they state what the chain enforces, and they flag where older plans or designs differ ([Style Guide](../22-about/style-guide.md)).

### 5. Separate the powers

**Idea.** No single party should be able to issue, spend and rule.

**In the protocol:**

- **The genesis allocations cannot vote.** They can only hand out stake ([restricted accounts](../21-reference/system-accounts.md#restricted-accounts-pixarex-and-pixateam)).
- **The community fund has no keys.** It pays only proposals that stakeholders approve.
- **Protocol changes need the witnesses.** A change activates only when enough elected witnesses run it.
- **Off chain, the work is split.** Development, stewardship and operation sit with three separate legal entities ([Who Does What](who-does-what.md)).

**Still incomplete.** Separation on paper is not yet distribution in practice. On 2026-10-05, a handful of accounts held almost all of the stake that can vote ([Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md)).

### 6. Serve the members

**Idea.** Steem's third principle: the community serves its own members.

**In practice:**

- **Communities** let members organise themselves ([Communities](../02-social-layer/communities.md)).
- **The fund** lets them finance what they need ([Decentralized Pixa Fund](../07-governance/decentralized-pixa-fund.md)).
- **No fee for joining.** The app opens accounts at no cost to the user.

### 7. Build on proven code, change only what you must

**Idea.** Hive's code has run in public since 2016.

**In practice.** Pixa changes a short, documented list of rules and keeps everything else, so tools written for Hive work once they are set to Pixa's chain ID, key prefix and token symbols ([Chain Parameters](../21-reference/chain-parameters.md#network-identity)). Hardfork 29 fixed the inherited reward denominator that a new chain could not use.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Who receives new tokens | Authors, curators, witnesses, the fund, and stakeholders for holding | Authors, curators, witnesses and the fund; nothing for holding |
| Interest on the second token | Yes | No |
| Where artworks live | Links to image hosts | Inside the post |
| Separation of roles | One company at Steem's start; community-run on Hive | Allocations that cannot vote, a keyless fund, three entities |

## Sources

- [Steem whitepaper](https://steem.com/steem-whitepaper.pdf): introduction (the three principles), "Micropayments Don't Work", "Distributing Currency".
- [Hive whitepaper](https://hive.io/whitepaper.pdf), §II.4–II.5.
- Chain rules: [Chain Parameters](../21-reference/chain-parameters.md); live stake figures: [Decentralization and Safeguards](../07-governance/decentralization-and-safeguards.md).
