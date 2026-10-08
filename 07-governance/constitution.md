# Constitution

> **Status: Proposed.** Five principles were drafted in December 2025. None has been adopted, and no rule on chain refers to them. Last checked 2026-10-05.

Code decides what the chain does. It cannot say what the community is for. A constitution would set down the shared values against which code changes, moderation and the use of the fund are judged. This page records the principles drafted for Pixagram and where the idea comes from. It also sets each principle against today's network and lists the questions to settle before anything is adopted.

## Where the idea comes from

- **Larimer, 2016.** In "Why every Blockchain needs a Constitution" (2016-07-01), Dan Larimer wrote that "blockchains do not solve the governance problem". He made four points:
  - A constitution should define values rather than laws, because people who share values can settle new questions together.
  - If the code is to stay flexible, the constitution must be practically immutable.
  - Every user should sign it cryptographically. Signing gives its dispute-resolution terms standing.
  - The purpose of governance is to make a fork less likely.
- **EOS, 2018–2019.** EOS, whose software Larimer led at Block.one, launched in 2018 with an interim constitution and an arbitration forum. The forum was soon overwhelmed with cases. In April 2019, EOS's block producers replaced the constitution with a user agreement.
- **Steem and Hive** have no constitution. Their rules are the code and what the elected witnesses choose to run. When Steem's community split in 2020, the outcome was a fork ([From STEEM to HIVE to PIXA](../01-start-here/from-steem-to-hive-to-pixa.md#the-2020-split)).
- **Pixagram, 2025.** An article by the project, "How Pixagram Completes the Vision for Blockchain World Domination" (2025-12-20), took up Larimer's idea and proposed five principles.

## The five principles (draft)

These are the draft's words:

1. **Censorship Resistance & Freedom of Expression.** "Art should never be restricted or erased by centralized entities."
2. **Financial Liberty & Decentralization.** "True ownership means no intermediaries controlling access, storage, or monetization."
3. **Technology as a Community Pillar.** "Great communities are built on great technology."
4. **Opposing Apathy with Art.** "Instead of empty words, we fight stagnation with meaningful artworks."
5. **Pixel Art as a Form of Meditation.** "There is peace in simplicity. The constraints of pixel art encourage focus, patience, and deep artistic expression."

## The draft against today's network

| Principle | What already supports it | Where it falls short, or needs a decision |
|---|---|---|
| 1. Censorship resistance | No one can erase a post from the chain. Edits and deletions add new versions; the original stays ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md#permanence)). | Interfaces can still hide content. The app hides flagged posts by default, community moderators can mute posts, and the law may oblige an app to hide something ([Censorship Resilience and Moderation](../02-social-layer/censorship-resilience-and-moderation.md)). Does the principle bind the record, the app, or both? |
| 2. Financial liberty | Keys are created in your browser. Artworks are stored in the chain itself. Most operations need no fee. | Opening an account in the app requires phone verification by the operator. Stake is highly concentrated ([Decentralization and Safeguards](decentralization-and-safeguards.md)). |
| 3. Technology | Open code, built on software in public use since 2016 | A value to hold to, not a rule that code can check |
| 4. Opposing apathy with art | Rewards go to people who publish and curate, never to holding ([Supply, Inflation and Yield](../04-tokens-and-economy/supply-inflation-and-yield.md#yield-there-is-none)) | A value, not a rule |
| 5. Pixel art as meditation | The app's canvas, palettes and size presets | A value, not a rule |

## What adoption would have to settle

1. **Values or rules?** Larimer argued for values. Which of the five are commitments people can hold the network to, and which describe its culture?
2. **Who ratifies it?** Stakeholders, witnesses, users, or all three? Existing tools could each count a different group:
   - a DPF proposal that pays nothing, used as a stake-weighted poll
   - witnesses publishing a statement that they endorse it
   - users signing it

   On 2026-10-05, a few accounts would decide each of these.
3. **Which text?** The exact version should be fixed on chain, for example by recording its hash in a `custom_json` operation, so that everyone knows what was signed.
4. **Whom does it bind?** The chain cannot enforce values. A constitution binds people and organisations, so it must say who: the witnesses who choose what software to run, the operator of the app, community moderators, the developers.
5. **How does it change?** "Practically immutable" needs a definition: what majority, over what period?
6. **How are disputes settled?** Larimer called for dispute resolution and a jurisdiction, and EOS's arbitration forum was overwhelmed. Each artwork's licence already names a governing law ([Licence](../03-art-on-chain/permanence-and-provenance.md#licence)). Should the constitution add anything for disputes between users?
7. **How does it relate to the legal entities?** The 2025 article proposed that a foundation stand behind the constitution. The Pixa Omnibus Foundation, which stewards the protocol, has not adopted one ([Who Does What](../01-start-here/who-does-what.md)).

Until these are answered, the principles describe what the project intends. They do not bind anyone.

## Inherited → changed

| | Steem / Hive | Pixa |
|---|---|---|
| Constitution | none | five principles drafted in 2025; not adopted |
| What sets the rules | the code, and the witnesses who choose what to run | same |
| The last resort | a fork, as Hive from Steem in 2020 | same |

## Sources

- Dan Larimer, "[Why every Blockchain needs a Constitution](https://steemit.com/blockchain/@dan/why-every-blockchain-needs-a-constitution)", Steemit, 2016-07-01.
- "How Pixagram Completes the Vision for Blockchain World Domination", LinkedIn, 2025-12-20: the five principles. Some figures in that article predate the chain and differ from it; [Chain Parameters](../21-reference/chain-parameters.md) has the values the chain enforces.
- CryptoSlate, "[Block Producers change EOS constitution following voting gridlock](https://cryptoslate.com/block-producers-change-eos-constitution-following-voting-gridlock/)", 2019-04-15.
