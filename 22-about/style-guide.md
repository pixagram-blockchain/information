# Style Guide

> **Status: Live.** These rules apply to every page in this repository, and the PXS rules apply to all public copy about Pixagram.

This guide is for anyone who writes these pages. It sets out three rules, then the template every page follows, then the names, words and formats to use.

## The three rules

1. **Say what the chain does.** When the design, older documents and the live network disagree, give the network's value and say that the others differ. Readers can check every claim against the code or the chain, and they will.
2. **Every number has one reference.** [Chain Parameters](../21-reference/chain-parameters.md) holds every protocol value. Another page may quote a number when it helps the reader, but it links there, and Chain Parameters wins if they disagree. Live values appear with the API call that returns them and the date they were read.
3. **Promise less, loudly; reference more, quietly.** This matters most for [Pixa Supra (PXS)](#writing-about-pxs), but it applies to tokens, rewards and roadmaps too. State what is not guaranteed before you describe what the design aims for.

## Page template

Every page opens the same way:

```markdown
# Page Title

> **Status: Live.** One sentence on what is true today. Last checked YYYY-MM-DD.

Two to four sentences: what this page answers, and for whom.

## Sections …

## Inherited → changed          ← concept pages only

| | Steem / Hive | Pixa |
|---|---|---|
| Transaction fees | none for most operations; Resource Credits | same |
| Reward for holding stake | a share of issuance | none |

## Sources

- Code: [config.hpp:59](https://github.com/pixagram-blockchain/pixagram/blob/<commit>/…#L59)
- Hive whitepaper (2020), §II.2 "Resource Credits"
```

**Status values**

| Status | Use it when |
|---|---|
| **Live** | The feature runs on mainnet today. |
| **Planned (2027)** | The feature is committed on the roadmap, with a date. Buying and selling artworks on chain is planned for 2027. |
| **Proposed** | A design is under discussion and nothing is committed. |
| **Historical** | The page describes the past, or is a signed opinion piece. |

When the design and the network differ, the status line says both. For example: "**Live.** 8 witnesses today; up to 21 elected, 1 required."

**Inherited → changed.** Every concept page ends with this table. It shows what Steem or Hive did and what Pixa does instead, which is how the Steem and Hive whitepapers enter these pages: summarised, cited and updated, never copied.

## Registers

The repository's sections fall into four registers, and each has its own voice.

| Part | Voice | Do | Don't |
|---|---|---|---|
| **Understand** (concepts, sections 01 to 07, and the product pages of section 14) | Explanatory, precise; elevated vocabulary is welcome when it is exact | Define each term at first use and link it to the [Glossary](../21-reference/glossary.md) | Use marketing adjectives ("revolutionary", "world domination") or make claims nobody can check |
| **Use** (guides, section 08) | Second person, imperative, one action per step | Warn at the step where it matters: "You cannot undo this." | Explain theory; link to the concept page instead |
| **Build** (developers, node operators, protocol, API, infrastructure: sections 09 to 13 and 18) | Exact and literal | Give copy-paste commands with pinned versions and the expected output | Write "should work" or leave versions unpinned |
| **Reference** (sections 19 and 21) | Tables, no narrative | Source every value | Repeat values from other pages |

Pages in **History and design** (section 20) are dated: the timeline from the chain's record, and signed essays that may keep their authors' voice. A fact from an essay enters a reference page only after someone checks it. Sections whose pages are all planned (15 to 17 except their one written page each) carry a README that says so and nothing more.

Elevated but exact:

> Proof-of-Brain turns attention into allocation: stake-weighted votes decide where each day's new PIXA goes.

Not this:

> Pixagram's revolutionary Proof-of-Brain guarantees fair rewards for everyone.

## Names

| Thing | Write | Notes |
|---|---|---|
| The blockchain | the Pixa chain, or Pixa | not "the Pixagram chain" |
| The social network and the project | Pixagram | |
| Liquid token | PIXA | Use PXA only when naming a market pair, such as PXA/USDT. |
| Staked token | Pixa Power (PXP) | Write VESTS only in API, code or exact-balance contexts. |
| Second unit | Pixa Supra (PXS), then PXS | In one phrase: a Big Mac referenced supracoin. Never "stablecoin" or "pegged"; see [Writing about PXS](#writing-about-pxs). |
| Fund | Decentralized Pixa Fund (DPF) | |
| Accounts | `pixa.omnibus`, `pixa.rex`, `pixa.team` | Format every account name as code. |
| Block producers | witnesses | |
| Consensus and rewards | DPoS, Proof-of-Brain | Proof-of-Brain is hyphenated and capitalised. |
| Fee model | Resource Credits (RC) | |
| Upgrades | hardfork 30 in prose, HF30 in tables | |
| Organisations | Pixagram SA (Switzerland), Pixa Omnibus Foundation (Cayman Islands), Pixa Rex S.A. (Panama) | Don't confuse the Foundation with the `pixa.omnibus` account. |
| The older chains | Steem and Hive for the chains; STEEM and HIVE for their tokens | |
| Operations and API methods | `comment`, `transfer`, `condenser_api.get_accounts` | code format |
| Web addresses | pixagram.com for the app, pixa.org for developers, `api.pixagram.com` for the API | |

## Retired names and claims

These appear in older posts, articles and documentation. Do not reuse them. When a line has to name one in order to correct it, as in a FAQ answer, end the line with `<!-- retired-ok -->`. The marker renders as nothing and tells the link checker the use is deliberate.

| Retired | Use instead | Why |
|---|---|---|
| pixagram.io | pixagram.com, pixa.org | The domains changed. |
| pixagram.dev as an API endpoint | `api.pixagram.com` or another public node | It no longer serves an API. |
| Pixa Operations S.A. | Pixa Rex S.A. | Pixa Rex S.A. replaced it as operator. |
| `pixa.ico`, "ICO pool", "ICO" | `pixa.rex`; "token generation event (TGE)" | The account name never shipped, and "ICO" presents tokens as an investment offering. |
| Pixagram AG | Pixagram SA | The company presents itself publicly as Pixagram SA. |
| PixaFlat, PixaSupra | Pixa Supra (PXS) | The unit has one name. |
| "stable", "stablecoin", "Big Mac Index stablecoin", "pegged", "pegged to $1 of PIXA", "pegged to the Big Mac Index" | "Big Mac referenced supracoin", after saying that PXS promises no price; see [Writing about PXS](#writing-about-pxs) | PXS defends no price. |
| "backed by a minimum 300% reserve" | "conversions are reduced by a haircut when the collateral ratio is low; no reserve is held" | No reserve exists. The real thresholds are in [Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed). |
| Decentralized Proposal Fund | Decentralized Pixa Fund (DPF) | That is the name used on chain. |
| "17.5% of inflation to the DPF" | link to [Issuance](../21-reference/chain-parameters.md#issuance) | The nominal share is 15%. |
| "300,000 TPS", "10,000 TPS" | "capacity is bounded by block size; no benchmark has been published" | Nothing has measured these figures. |
| "72 kB posts", "128 KiB transaction limit" | link to [Transaction and block size](../21-reference/chain-parameters.md#transaction-and-block-size) | Neither limit exists. |
| "base64 PNG and WebP posts", "fully on-chain, no hashes" (about everything) | "Artworks are stored in the post itself as lossless WebP. Images inside blog posts are links to files hosted elsewhere; the editor uploads them to Arweave." | Blog images are links. |
| "zero fees", "no fees" | "Most operations carry no fee. Opening an account, creating a proposal and converting PIXA to PXS each cost one." | Three operations do charge a fee. |
| "deflationary" | issuance and burn figures | PIXA is issued in every block. |
| "21 witnesses required", or "21 witnesses" as a current fact | "up to 21 elected, 1 required; *N* active today" | One witness is enough to run the chain, and the live count is lower than 21. |
| "250k PXS" or "250,000 PXS" for the fund's seed | 245,098.039 PXS, or about 245,098 PXS | The seed is 25,000,000 PIXA ÷ 102, the genesis feed. |
| "keeps 97% of revenue" (about other platforms) | leave it out unless sourced | There is no source. |
| Steem Power, Hive Power, SBD, HBD, DHF (when meaning Pixa) | Pixa Power, PXS, DPF | Use Pixa's own names. |

## Writing about PXS

PXS promises no price. Nothing defends it, and no one owes its holder anything. It is a unit oriented toward one Big Mac's worth of purchasing power, and it converts into PIXA. The words used about it must describe exactly that and nothing more. Words that imply a promise are false, because no such promise exists, and they mislead the people who rely on them.

**Lead with what PXS does not guarantee.** Wherever a page *describes* PXS (what it is, how it behaves, what it refers to), the description opens with what PXS does not promise. Only after that may you describe the reference it is oriented toward. A plain mention of PXS as a unit, such as a balance, a fee or a symbol in a table, needs no disclaimer.

**In one phrase.** Where a single phrase must say what PXS is, call it a *Big Mac referenced supracoin*, and put it after the statement that PXS promises no price. Never call PXS pegged, not even to the Big Mac.

| Avoid | Use instead |
|---|---|
| "maintains", "holds", "protects" or "preserves" its value | "settles at the haircut-adjusted amount the collateral can bear" |
| "superior to fiat", "a better store of value" | Describe the reference, not an outcome: "The oracle orients toward a purchasing-power reference; delivered value is not guaranteed and falls under stress." |
| "stable" or "stability" as a property of PXS | "bounded but not defended", stated together with the non-guarantee |
| "backed by", "reserve", "collateralised at X%" as a promise | "borne on the Atlas"; give the collateral ratio as a threshold, never as a claim |
| "redeem", "redemption", "1 PXS = X" | "converts to PIXA at the prevailing haircut, which may be below the oracle reading" |
| "guaranteed", "pegged", "= 1 USD / EUR", "your value is safe" | Remove them. |

The words that fit are oracle, atlas, supra, macro, haircut, projection and orientation. The [Glossary](../21-reference/glossary.md#design-vocabulary) defines each.

**Six statements every PXS text must stay consistent with.** If a sentence contradicts one of them, change the sentence.

1. PXS makes no promise of a stable value.
2. PXS gives nobody a claim to a fixed amount, and nobody is obliged to honour one.
3. No managed reserve stands behind PXS.
4. What PXS is follows from its mechanism, not from the words used about it.
5. Risk is moved, not removed. Say where it sits.
6. The reference is a direction, never a destination.

**Say where the design and the chain differ.** The PXS design notes describe a corridor of roughly 3× to 10× and 21 witnesses. The chain enforces different thresholds, and fewer witnesses run today (see [Chain Parameters](../21-reference/chain-parameters.md#pixa-supra-pxs-and-the-price-feed)). Until PIXA trades on a market, the feed uses a placeholder price for PIXA, and any PXS page must say so. [PXS at a Glance](../05-pixa-supra/pxs-at-a-glance.md#where-the-design-and-the-chain-differ) lists the differences.

## Tokens, rewards and money

- **No price talk.** No price predictions, and no "investment", "returns", "profit", "passive income", "APR" or "APY". Mention "yield" only to say there is none.
- **Rewards are payment for work.** Present them as pay for publishing, curating and producing blocks, never as income from holding. Holding PIXA, Pixa Power or PXS earns nothing by itself.
- **Exchanges and listings.** Name an exchange only as a fact a reader needs, such as which market the price feed reads. Never promote a listing.
- **Legal matters.** Do not state the legal classification of any token, and do not quote correspondence with regulators. The Regulatory Status page (planned) will hold the only approved text.

## Numbers and units

- **Thousands and decimals.** Use commas for thousands and a point for decimals: 2,500 and 0.020 PXS.
- **Dates and times.** Write dates in ISO form, with times in UTC: 2026-09-04 12:00 UTC.
- **Byte units.** KiB and MiB are powers of 1,024; kB and MB are powers of 1,000. Use the one the source uses.
- **Token amounts.** Give the token's own precision: 3 decimals for PIXA and PXS, 6 for VESTS.
- **Live values.** Show the API call that returns them and the date you read them: "8 witnesses on 2026-10-08 (`get_witness_schedule`)".
- **Approximations.** Approximate only with "about", and give the exact figure on [Chain Parameters](../21-reference/chain-parameters.md).

## Sources and citations

- **Code.** Cite a permalink at a fixed commit, with line numbers.
- **Whitepapers.** Cite the Steem whitepaper and the Hive whitepaper (2020) by section. The steem.com site now serves a July 2025 edition of the Steem whitepaper. For what Steem said at its launch, cite the [March 2016 edition](https://web.archive.org/web/20160815131730/https://steem.io/SteemWhitePaper.pdf).
- **Articles and essays.** Cite with author, date and link. Facts they contain must be checked before they appear outside History and design.
- **Sources section.** Every concept page ends with one.

## Diagrams and images

- **Mermaid first.** Draw diagrams in Mermaid, which GitHub renders. Keep labels short.
- **SVG figures.** Ship light and dark versions in `assets/`, chosen with `<picture>` and `prefers-color-scheme`.
- **Meaning.** Give every image alt text. Never let colour alone carry meaning.
- **Ownership.** Use only images the project owns or that carry a clear licence. No film stills, posters, memes, game art or other projects' logos.

## Security and disclosure

- **Secrets.** Never publish private keys, WIFs, seed phrases, passwords, internal hostnames or IP addresses.
- **Vulnerabilities.** A vulnerability that has not been fixed is never published. Report it privately to the maintainers. It is documented once the fix is live.
- **Your own keys.** Examples use placeholders such as `5K...`, never a real key.

## Files, folders and links

- **File names** are lowercase words joined by hyphens, such as `pxs-at-a-glance.md`. A page's title is its first heading.
- **Folders** follow the reading order, from `01-start-here` to `22-about`. Each folder's `README.md` lists its pages, and the repository's `README.md` lists them all.
- **Links between pages** are relative and end in `.md`, for example `../21-reference/glossary.md#haircut`, so they work on GitHub and in any copy of the repository.
- **Anchors** come from headings. Renaming a heading breaks the links to it, so search for them first.
- **Planned pages** appear in plain text in the indexes until they are written. Never link to a page that does not exist.

## Before you submit

- [ ] The page opens with a status line and a date.
- [ ] Every protocol number matches [Chain Parameters](../21-reference/chain-parameters.md) and links there, or is a live value given with its API call and date.
- [ ] No retired name or claim appears.
- [ ] Anything about PXS leads with what it does not guarantee.
- [ ] Concept pages end with the inherited → changed table and their sources.
- [ ] The page is listed in its folder's `README.md` and in the repository's `README.md`.
- [ ] `python3 .github/scripts/check_docs.py` passes.
