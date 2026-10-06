# Contributing

> **Status: Live.** How to report a mistake, propose a change and report a security problem. Last checked 2026-10-06.

Anyone can propose a change to these pages through a pull request on GitHub. The owners named in `CODEOWNERS` are asked to review it. A security problem is the exception: it is never reported in public.

## Report a mistake

Open an issue in this repository. Name the page and the sentence, and say what the chain, the code or a source shows instead, with a link or the API call you used. A mistake about a number is easiest to check when you give the block or the date you read it.

## Propose a change

1. **Fork the repository**, or create a branch if you have write access.
2. **Edit the Markdown files.** Follow the [Style Guide](style-guide.md). Above all:
   - every page opens with a title and a status line;
   - every protocol number matches [Chain Parameters](../11-reference/chain-parameters.md) and links there, or is a live value with its API call and date;
   - anything that describes PXS first says that PXS promises no price;
   - concept pages end with the inherited → changed table and their sources.
3. **Add a page** with a lowercase file name joined by hyphens, in the folder where it belongs. List it in that folder's `README.md` and in the contents of the repository's [README](../README.md#contents). A page that is not written yet stays in those lists as plain text.
4. **Run the checks** from the repository's root. They need only Python 3:

   ```bash
   python3 .github/scripts/check_docs.py
   ```

   They fail on a broken link or anchor, a reference link with no definition, a file name that is not lowercase, a page with no title or status line, and a page missing from its folder's index or from the contents. They warn about some retired names, such as pixagram.io, PixaFlat, "stablecoin" and "pegged"; check the rest against the [Style Guide](style-guide.md#retired-names-and-claims). <!-- retired-ok -->
   The last line counts the pages, errors and warnings:

   ```text
   … pages in … Markdown files, 0 errors, 0 warnings
   ```

5. **Open a pull request.** Say what changed and why, and give a source for every new fact: a permalink at a fixed commit, an API call with its date, or the document and section.

## How changes are reviewed

- **The checks run on every pull request** and on every push to `main` ([`check.yml`](../.github/workflows/check.yml)).
- **Owners review their paths.** [`CODEOWNERS`](../.github/CODEOWNERS) asks the owner to review every change, and the chain maintainer to review changes to `09-developers`, `10-node-operators` and `11-reference` as well. Where two owners are listed, the approval of either satisfies the rule.
- **Approval becomes binding** when `main` is protected with "Require a pull request before merging" and "Require review from Code Owners". That is a setting of the repository, not of these files.

## What never goes into a page, an issue or a pull request

- **Secrets:** private keys, WIFs, recovery phrases, passwords, internal hostnames or IP addresses. Examples use placeholders such as `5K...`.
- **Unfixed vulnerabilities**, in any form, including hints in a commit message.
- **Legal classifications** of PIXA, Pixa Power or PXS, and correspondence with regulators ([Style Guide](style-guide.md#tokens-rewards-and-money)).
- **Images** the project does not own or that carry no clear licence ([Style Guide](style-guide.md#diagrams-and-images)).

## Report a security problem

Do not open an issue or a pull request, and do not post it in a portal, including the app's Security and Bug Reports portals, or in a chat.

1. Go to the repository where the problem lies: [pixagram-blockchain/pixagram](https://github.com/pixagram-blockchain/pixagram) for the chain, [pixagram-blockchain/pixagram-ui-dev](https://github.com/pixagram-blockchain/pixagram-ui-dev) for the app, or this one for the documentation.
2. Open its **Security** tab and choose **Report a vulnerability**. The report is visible only to you and the maintainers.
3. Describe the problem: the component and the commit or version, the steps to reproduce it, and what an attacker could do. Reproduce it on your own node if you can ([Run a Node](../10-node-operators/run-a-node.md)), never against other people's accounts.

The report stays private until a fix is live on the network. The pages describe the problem only after that ([Style Guide](style-guide.md#security-and-disclosure)).

## Licence

The pages are published under the [MIT License](../LICENSE).
