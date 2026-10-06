# Become a Witness

> **Status: Planned.** The step-by-step witness guide is kept private while the witness set is being hardened. This page says what a witness is and how to ask for the guide. Last checked 2026-10-06.

A witness runs a node that produces blocks in turn and publishes a price feed. What witnesses decide, how they are elected and how they are paid is on [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md).

The operational guide — keys, node setup, registration, price feed and upkeep — is not published here for now. The details of how witnesses sign and register are being reviewed, and these pages do not describe them until that work is complete ([Style Guide](../13-about/style-guide.md#security-and-disclosure)).

## What a witness commits to

- **A node that never sleeps.** Every missed block is public and permanent, and missed blocks are not paid.
- **An exact clock.** Each block slot lasts 3 seconds, so a node whose clock drifts costs the network blocks.
- **A price feed every hour.** PXS promises no price; the feed is each witness's statement of how many PIXA one Big Mac costs. A feed older than 7 days stops counting ([Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md)).
- **Upgrades before hardforks.** After a hardfork activates, a witness on an older version can no longer produce valid blocks ([Protocol Upgrades](../07-governance/protocol-upgrades.md)).
- **A public page.** Stakeholders vote for people they can identify, so a witness says who runs the node, where, and how to reach them.

## Before you start

- **A server** as in [Run a Node](run-a-node.md#what-you-need): 2 vCPU, 4 GB, 50 GB SSD, x86-64. Prefer a provider and a region the other witnesses do not use: a chain is only as resilient as its least diverse failure.
- **An account** with its **active key** at hand. Create it in the app if you have none ([Create an Account](../08-guides/create-an-account.md)).
- **A page** to register as your witness URL, for example a post on Pixagram.

## How to get the guide

Ask the maintainers for the current witness guide through the project's private channel ([Contributing](../13-about/contributing.md#report-a-security-problem) explains how to reach them privately). They share it with operators who are setting up a node.

Once you run a witness, stakeholders vote for you as shown in [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md#how-to-vote).

## Sources

- **What witnesses do, and how they are elected and paid:** [Witnesses and DPoS](../07-governance/witnesses-and-dpos.md).
- **Running a node:** [Run a Node](run-a-node.md).
- **The price feed:** [Oracle and Price Feed](../05-pixa-supra/oracle-and-price-feed.md).
