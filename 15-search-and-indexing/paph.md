# PAPH

> **Status: Live.** The library `@pixagram/paph-js` 5.3.1 is published on npm (repository at commit `8959a08`, 2026-10-06); nothing on pixagram.com uses it today, and no production use is planned with a date.

PAPH is Pixagram's perceptual hash for pixel art: a fixed-size fingerprint of an image and a comparator that decides whether two fingerprints come from the same work, including after rotation, mirroring, colour inversion, tone shifts, nearest-neighbour upscaling or pasting into another picture. This page describes what the published library computes, how it compares, how it is versioned and calibrated, and where it stands: it is a reference implementation with a provisional calibration, and nothing on pixagram.com runs it. Readers who want copy detection on the platform should read the last section first.

## What it is for

A cryptographic hash such as `pixahash` changes completely when one pixel changes; it answers "are these bytes identical?". A perceptual hash answers "is this the same picture?", so that a copy of an artwork can be recognised even after the copier flipped it, inverted its colours or scaled it up. PAPH is built for pixel art specifically: small images, flat colours, hard edges and repetition, which defeat the perceptual hashes made for photographs.

The intended use, stated in the repository and on pixa.org, is plagiarism detection before an artwork is published or sold. That use is **not implemented**: the app does not import the library ([Search](../14-product/search.md#what-cannot-be-found)), and the pixa.org library page's sentence "used for plagiarism detection before an image becomes an NFT" describes an intention, not a running system.

## What it computes

`hash(rgbaPixels, width, height)` takes an RGBA byte buffer and returns two tiers ([`README.md`][readme], [`SPEC-005.1.md` §2][spec]):

| Tier | Size | Contents | Use |
|---|---|---|---|
| **Tier 1** (`t1`) | 2,560 bytes, fixed | Sectioned structural channels of the whole image, with a CRC-32 | Index search and the fast `screen(a, b)` pre-check |
| **Tier 2** (`t2`) | 32 + 32 × n bytes, n ≤ 512 | Keypoint records: position, pyramid level, orientation, strength, region and a 128-bit descriptor in two 64-bit planes, with CRC-32s linking it to Tier 1 | Geometric evidence in `compare` |

Extraction follows a frozen profile, **PAPH5-E03**: luma `(54r + 183g + 19b + 128) >> 8`, matte folding for images on a flat border, detection and removal of exact k×k upscales, a 5551 palette, a FAST corner detector with threshold 18, non-maximum suppression 4 and a pyramid with a 10/13 ladder. Everything is integer arithmetic: the same bytes in give the same bytes out on every platform, which is what lets fingerprints computed by different programs be compared and stored.

## How it compares

`compare(a, b)` returns a report with a **verdict** and the evidence behind it ([`SPEC-005.1.md` §3-§7][spec]):

| Verdict | Meaning |
|---|---|
| `Identical` | The same image |
| `Copy` | The same work, transformed |
| `Related` | Shared structure beyond chance |
| `Suspected` | Evidence that needs a human look |
| `Unrelated` | Different works (the specification calls this verdict `Distinct`; the code says `Unrelated`) |
| `Indeterminate` | The comparison could not be made: corrupt tiers, too few keypoints, or an image outside the method's reach |

The evidence comes from three axes, each scored on a 0 to 10,000 scale: **structure** (seven channels over Tier 1), **geometry** (a staged search over the eight D4 transforms, rotations and mirrors, with an inversion family, matching Tier 2 keypoints) and **diversity**, which demotes matches driven by repetition, a tiled pattern matching another tiled pattern. The report also carries an `evidenceClass` and an `assetRisk` level; the TypeScript declarations name the middle level `ELEVATED` and the code emits `POSSIBLE`, one of the discrepancies listed below.

The comparator is specified to survive, alone or combined: all eight D4 transforms, colour inversion, tone shifts, nearest-neighbour upscales, and crops pasted into new compositions. Its conformance suite covers 19 verdict scenarios and 13 frozen golden vectors, which the repository names as the contract any other implementation, such as a planned Rust and WebAssembly engine, must meet.

## Versions, calibration and performance

| | Value |
|---|---|
| Package | `@pixagram/paph-js` 5.3.1, MIT, © Pixagram SA; Node 18 or later; CommonJS and ES module entry points; subpaths `/wire` and `/comparator` |
| Wire format | 5 |
| Comparator | 51 |
| Extraction profile | PAPH5-E03 |
| Specification | `docs/SPEC-005.1.md` in the repository; there is no SPEC-006 |
| Calibration | `CAL-051-PROVISIONAL`: thresholds and lookup tables set from the conformance fixtures, "honest about not having seen a production corpus". `tools/calibrate.cjs` fits a real profile from a labelled corpus and refuses to bless one below the specification's gates: at least 24 image families, 60 images, 60 positive pairs and 10 measurable positives per channel. |
| Browser build | `dist/paph53.browser.js`, no dependencies, attaches `PAPH53` to the global object; the README still says `PAPH51` |
| Performance | CHANGELOG 5.3.0: a 150×110 image hashes in about 21.8 ms and a pair compares in about 36.8 ms (median, JavaScript, the project's build container); the specification's informative figures, 95 ms and 117 ms, predate that release |

Because the calibration is provisional, the verdict thresholds have not been fitted to real Pixagram artworks. A deployment would start by building a labelled corpus and running the calibration tool; until then, verdicts are the fixtures' verdicts.

## The API

```js
import { hash, compare, screen, parseT1, parseT2, cal, profileEncode, profileDecode } from '@pixagram/paph-js';

const a = hash(pixelsA, widthA, heightA);   // { t1, t2, detail }
const b = hash(pixelsB, widthB, heightB);
screen(a, b);                               // Tier 1 only: fast rejection
const report = compare(a, b);               // verdict, evidenceClass, assetRisk, channels, geometry
compare(a, b, { profile: profileDecode(bytes) });   // with a fitted calibration
```

`hash` also accepts an `ImageData` object. The input must be RGBA, 4 bytes per pixel, or the call throws. Fingerprints are plain byte arrays, so they can be stored next to a post's permlink, in a database or in a post's `json_metadata`; nothing in the chain's rules knows them.

## What exists and what does not

| | State |
|---|---|
| The library, its specification, tests and golden vectors | Published |
| A production calibration | Not done; the profile is provisional |
| Use in the app at publication time | Not implemented. The app bundles `@pixagram/pixahash` for content hashing only ([Search](../14-product/search.md#what-cannot-be-found)) |
| Use in the operator's search service | Not visible from the app; the service's code is not published |
| An index of fingerprints for every artwork on chain, and a similarity search over it | Not built. No code or specification exists; the planned pages of this section stay planned until it does ([Search and indexing](README.md)) |
| A chain rule that reads or stores fingerprints | None, and none planned; the chain stores posts, not judgements about them ([Data Model](../11-protocol-reference/data-model.md#application-only-what-the-pixagram-app-defines)) |

What this means for an artist today: nothing stops a copy of an artwork from being published as a new post, and nothing marks it. Provenance comes from the chain's order of events, the original being in an earlier block, and from the community's eyes ([Permanence and Provenance](../03-art-on-chain/permanence-and-provenance.md)). A program that wanted to detect copies could do it now with this library and the public API: hash every artwork from `bridge.get_ranked_posts` as it appears, keep the Tier 1 fingerprints, and `screen` new ones against them.

## Discrepancies in the repository

Recorded so that nobody is surprised by them; none affects the computed bytes.

- The README's title says "PAPH 5.1" and names the browser global `PAPH51`; the package is 5.3.1 and the bundle attaches `PAPH53`.
- The specification's verdict lattice says `Distinct`; the code and README say `Unrelated`.
- `index.d.ts` declares the asset-risk levels `LOW | ELEVATED | HIGH`; the code emits `POSSIBLE` for the middle one.
- The CHANGELOG stops at 5.3.0 (2026-08-28); the published 5.3.1 has no entry.
- pixa.org's library page lists version 5.3.0 and describes production use that does not exist.

## Inherited → changed

Hive has no perceptual hashing in its protocol or its reference front ends; copy detection, where it exists, is done by community curation projects outside the chain. Pixa's chain is the same in this respect. PAPH is a library in the Pixagram ecosystem, not a chain feature.

## Sources

- **Repository** [`pixagram-blockchain/paph-js`](https://github.com/pixagram-blockchain/paph-js) at commit [`8959a08`](https://github.com/pixagram-blockchain/paph-js/tree/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef): [`README.md`][readme], [`docs/SPEC-005.1.md`][spec], [`CHANGELOG.md`](https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/CHANGELOG.md), [`index.d.ts`](https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/index.d.ts), [`src/paph-js.cjs:1308`](https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/src/paph-js.cjs#L1308) (`POSSIBLE`), [`dist/paph53.browser.js:3205`](https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/dist/paph53.browser.js#L3205) (`PAPH53`), [`package.json`](https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/package.json).
- **npm:** [`@pixagram/paph-js`](https://www.npmjs.com/package/@pixagram/paph-js), version 5.3.1 on 2026-10-08.
- **App** at commit [`ca1d157`](https://github.com/pixagram-blockchain/pixagram-ui-dev/tree/ca1d15762b52ec08f33c69ca9afa34bb78c0df52): no import of `@pixagram/paph-js`; `@pixagram/pixahash` in [`png-db.js:1`](https://github.com/pixagram-blockchain/pixagram-ui-dev/blob/ca1d15762b52ec08f33c69ca9afa34bb78c0df52/src/js/utils/png-db.js#L1).
- **pixa.org:** the [library page](https://pixa.org/library.html#similarity) and the [interface page](https://pixa.org/interface.html), read on 2026-10-07.

[readme]: https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/README.md
[spec]: https://github.com/pixagram-blockchain/paph-js/blob/8959a08f4ce95fbe5a0c59c6bfbc157e52094eef/docs/SPEC-005.1.md
