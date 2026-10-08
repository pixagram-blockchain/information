#!/usr/bin/env python3
"""Check the documentation in this repository.

Errors (the check fails):
  - a relative link or anchor that does not resolve, or a reference link
    with no definition;
  - a page whose file name is not lowercase, that does not open with a title
    and a status line, or that is missing from its folder's README.md or from
    the repository's README.md.

Warnings (reported, not fatal):
  - retired names and claims from the Style Guide, except on lines that end
    with <!-- retired-ok --> and on the pages that list them on purpose.

Standard library only:  python3 .github/scripts/check_docs.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDED_DIRS = {".git", ".github", "node_modules"}
SECTION = re.compile(r"^\d\d-[a-z0-9-]+$")
INDEX = "README.md"

INLINE_LINK = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*<?([^)\s>]+)>?(\s+\"[^\"]*\")?\s*\)")
REF_DEF = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(\S+)(.*)$")
REF_LABEL = re.compile(r"^\s{0,3}\[([^\]]+)\]:")
REF_USE = re.compile(r"\]\[([^\]]+)\]")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
STATUS = re.compile(r"^> \*\*Status:")

# Retired names and claims from the Style Guide.
RETIRED = {
    r"pixagram\.io": "pixagram.com / pixa.org",
    r"PixaFlat|PixaSupra\b": "Pixa Supra (PXS)",
    r"Pixa Operations": "Pixa Rex S.A.",
    r"\bpixa\.ico\b": "pixa.rex",
    r"Pixagram AG\b": "Pixagram SA",
    r"Decentralized Proposal Fund": "Decentralized Pixa Fund (DPF)",
    r"\b72 ?kB\b": "Chain Parameters, transaction size",
    r"\bdeflationary\b": "issuance and burn figures",
    r"\bstablecoins?\b": "Big Mac referenced supracoin; see Writing about PXS",
    r"\bpegged\b": "PXS has no peg; see Writing about PXS",
}
# Pages that name retired terms in order to correct them.
RETIRED_ALLOWED = {
    "22-about/style-guide.md",
    "21-reference/glossary.md",
    "21-reference/chain-parameters.md",
}
RETIRED_OK = "<!-- retired-ok -->"


def markdown_files(root: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith("."))
        found += [Path(dirpath) / n for n in sorted(filenames) if n.endswith(".md")]
    return found


def strip_code(lines: list[str]) -> list[str]:
    """Blank out fenced code blocks and inline code so that links inside them are ignored."""
    out, in_fence = [], False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line))
    return out


def slugify(text: str) -> str:
    """GitHub's heading anchor: drop link targets and markup, lowercase, keep word characters, spaces and hyphens."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    result, in_fence = set(), False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        m = None if in_fence else HEADING.match(line)
        if not m:
            continue
        slug = slugify(m.group(2))
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        result.add(slug if n == 0 else f"{slug}-{n}")
    return result


def is_relative(target: str) -> bool:
    return not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) and not target.startswith("//")


def link_targets(page: Path) -> set[Path]:
    """Every file or folder a page links to, resolved."""
    result = set()
    for line in strip_code(page.read_text(encoding="utf-8").splitlines()):
        targets = [m.group(3) for m in INLINE_LINK.finditer(line)]
        ref = REF_DEF.match(line)
        if ref:
            targets.append(ref.group(2))
        for target in targets:
            path_part = target.partition("#")[0]
            if path_part and is_relative(target):
                result.add((page.parent / path_part).resolve())
    return result


def check(root: Path) -> tuple[list[str], list[str], int]:
    errors, warnings = [], []
    files = markdown_files(root)
    anchor_cache: dict[Path, set[str]] = {}

    def anchors_of(p: Path) -> set[str]:
        if p not in anchor_cache:
            anchor_cache[p] = anchors(p)
        return anchor_cache[p]

    # Links, anchors, reference links and retired terms, on every Markdown file.
    for page in files:
        rel = page.relative_to(root).as_posix()
        lines = strip_code(page.read_text(encoding="utf-8").splitlines())
        defined = {m.group(1).lower() for m in (REF_LABEL.match(l) for l in lines) if m}
        for lineno, line in enumerate(lines, 1):
            if not REF_LABEL.match(line):
                for label in REF_USE.findall(line):
                    if label.lower() not in defined:
                        errors.append(f"{rel}:{lineno}: reference link [{label}] has no definition")
            targets = [m.group(3) for m in INLINE_LINK.finditer(line)]
            ref = REF_DEF.match(line)
            if ref:
                targets.append(ref.group(2))
            for target in targets:
                if not is_relative(target):
                    continue
                path_part, _, anchor = target.partition("#")
                dest = page if not path_part else (page.parent / path_part).resolve()
                if not dest.exists():
                    errors.append(f"{rel}:{lineno}: broken link '{target}'")
                elif anchor and dest.suffix == ".md" and anchor not in anchors_of(dest):
                    errors.append(f"{rel}:{lineno}: missing anchor '#{anchor}' in {dest.relative_to(root).as_posix()}")
        if rel in RETIRED_ALLOWED:
            continue
        for lineno, line in enumerate(lines, 1):
            if RETIRED_OK in line:
                continue
            for pattern, use in RETIRED.items():
                if re.search(pattern, line, flags=re.IGNORECASE):
                    warnings.append(f"{rel}:{lineno}: retired term /{pattern}/ (use: {use})")

    # Pages: names, title, status line, and listing in the indexes.
    root_index = root / INDEX
    root_links = link_targets(root_index) if root_index.exists() else set()
    sections = sorted(d for d in root.iterdir() if d.is_dir() and SECTION.match(d.name))
    pages = 0
    for section in sections:
        index = section / INDEX
        if not index.exists():
            errors.append(f"{section.name}: no {INDEX}")
            continue
        if index.resolve() not in root_links:
            errors.append(f"{INDEX}: does not link {section.name}/{INDEX}")
        section_links = link_targets(index)
        for page in sorted(section.glob("*.md")):
            if page.name == INDEX:
                continue
            pages += 1
            rel = page.relative_to(root).as_posix()
            if page.name != page.name.lower():
                errors.append(f"{rel}: file name is not lowercase")
            text = page.read_text(encoding="utf-8").splitlines()
            if not text or not text[0].startswith("# "):
                errors.append(f"{rel}: does not open with a '# ' title")
            if not any(STATUS.match(l) for l in text[:6]):
                errors.append(f"{rel}: no status line ('> **Status: …') under the title")
            if page.resolve() not in section_links:
                errors.append(f"{section.name}/{INDEX}: does not list {page.name}")
            if page.resolve() not in root_links:
                errors.append(f"{INDEX}: does not list {rel}")
    return errors, warnings, pages


def main() -> int:
    errors, warnings, pages = check(ROOT)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{pages} pages in {len(markdown_files(ROOT))} Markdown files, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
