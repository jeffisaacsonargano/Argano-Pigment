#!/usr/bin/env python3
"""Lint Pigment formulas against house formula rules.

Usage:
  lint_formula.py [--name BLOCK_NAME] < formula.txt
  lint_formula.py [--name BLOCK_NAME] --formula "IFBLANK('X', FALSE)"
  lint_formula.py --jsonl formulas.jsonl [--summary]
      one JSON object per line with "formula" and optional "name"

Options:
  --constant-prefix "CON "          prefix of manual-input constant blocks (default "CON ")
  --exempt-prefixes "ARM_,BP_,SEC_" block-name prefixes exempt from the hard-code rule

Exit code 1 if any HIGH finding, else 0. Standard library only.
Rule ids match the rules in SKILL.md and references/rules-background.md.
"""
import argparse
import json
import re
import sys
from collections import Counter

MODIFIERS = r"(BY|ADD|REMOVE|FILTER|EXCLUDE|SELECT|KEEP)"


def strip_comments(text):
    """Drop // comments, leaving quoted strings and identifiers intact."""
    out, i, quote = [], 0, None
    while i < len(text):
        c = text[i]
        if quote:
            out.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            out.append(c)
        elif text.startswith("//", i):
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        else:
            out.append(c)
        i += 1
    return "".join(out)


def call_args(text, open_idx):
    """Split the arguments of the call whose '(' is at open_idx. Returns (args, close_idx)."""
    depth, quote, start, args = 0, None, open_idx + 1, []
    for i in range(open_idx, len(text)):
        c = text[i]
        if quote:
            if c == quote:
                quote = None
            continue
        if c in "\"'":
            quote = c
        elif c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
            if depth == 0:
                args.append(text[start:i].strip())
                return args, i
        elif c == "," and depth == 1:
            args.append(text[start:i].strip())
            start = i + 1
    return args, len(text)


def snippet(text, start, end):
    s = " ".join(text[start:end].split())
    return s if len(s) <= 110 else s[:107] + "..."


def lint(formula, name="", con_prefix="CON ", exempt=("ARM_", "BP_", "SEC_")):
    findings = []
    code = strip_comments(formula)
    con = f"'{con_prefix}<List>: <Item>'"

    def add(sev, rule, msg, start=None, end=None):
        snip = snippet(code, start, end) if start is not None else ""
        findings.append({"severity": sev, "rule": rule, "message": msg, "snippet": snip})

    # R01 IFBLANK: house style is IF(ISDEFINED(x), ...)
    for m in re.finditer(r"\bIFBLANK\s*\(", code, re.I):
        args, close = call_args(code, m.end() - 1)
        fb = args[1] if len(args) > 1 else ""
        if re.fullmatch(r"(?i)FALSE|TRUE", fb):
            add("HIGH", "R01", f"IFBLANK(x, {fb.upper()}) fills every empty cell with a boolean (dense) "
                "and stores FALSE. Use the flag itself, or IF(ISDEFINED(x), TRUE).", m.start(), close + 1)
        elif re.fullmatch(r'"[^"]*"', fb):
            add("HIGH", "R01", 'IFBLANK(x, "text") fills every empty cell (dense). For optional-tag text keys, '
                "split the optional checks into their own metrics instead of joining IFBLANK(...,\"\") pieces.",
                m.start(), close + 1)
        elif re.fullmatch(r"-?\d+(\.\d+)?", fb):
            add("HIGH", "R01", f"IFBLANK(x, {fb}) fills every empty cell with a number (dense). "
                "Leave it blank, or scope it: IF(ISDEFINED(x), ...).", m.start(), close + 1)
        elif re.fullmatch(r"(?i)BLANK", fb):
            add("MED", "R01", "IFBLANK(x, BLANK) is just x.", m.start(), close + 1)
        elif con_prefix and fb.startswith("'" + con_prefix):
            add("HIGH", "R01", "IFBLANK(x, <constant>) broadcasts a scalar into every empty cell (dense). "
                "Scope it with IF(ISDEFINED(...)) on the driving metric.", m.start(), close + 1)
        else:
            add("MED", "R01", "House style: write IF(ISDEFINED(A), A, B) instead of IFBLANK(A, B). "
                "Fine semantically only when B is sparse.", m.start(), close + 1)

    # R02 ISBLANK / ISNOTBLANK are always dense
    for m in re.finditer(r"\bIS(NOT)?BLANK\s*\(", code, re.I):
        args, close = call_args(code, m.end() - 1)
        add("HIGH", "R02", "ISBLANK/ISNOTBLANK return TRUE/FALSE in every cell (dense). Use ISDEFINED(x), "
            "IF(ISDEFINED(x), ...), or [EXCLUDE: ...].", m.start(), close + 1)

    # R03 IF(..., ..., FALSE) and IF(..., ..., 0)
    for m in re.finditer(r"(?<![A-Za-z_])IF\s*\(", code):
        args, close = call_args(code, m.end() - 1)
        if len(args) >= 3:
            other = args[2]
            if re.fullmatch(r"(?i)FALSE", other):
                add("HIGH", "R03", "Check booleans are TRUE or BLANK, never FALSE. Drop the else: IF(cond, TRUE).",
                    m.start(), close + 1)
            elif re.fullmatch(r"0(\.0+)?", other):
                add("MED", "R03", "Else-zero densifies. Drop the else unless the user asked for 0 here "
                    "(e.g. amounts on invalid lines).", m.start(), close + 1)
            elif re.fullmatch(r'""', other):
                add("MED", "R03", 'Else-"" densifies. Drop the else.', m.start(), close + 1)

    # R04 comparisons to TRUE/FALSE
    for m in re.finditer(r"(=|<>)\s*(TRUE|FALSE)\b", code, re.I):
        add("LOW", "R04", "Compare-to-boolean is redundant. Use the flag directly "
            "([FILTER: 'Flag?'], [EXCLUDE: 'Flag?']).", max(0, m.start() - 40), m.end())

    # R05 hard-coded list items / text compares (security blocks exempt)
    if not (exempt and name.startswith(tuple(exempt))):
        for m in re.finditer(r"'[^'\n]+'\s*\.\s*\"[^\"\n]+\"", code):
            add("HIGH", "R05", f"Hard-coded list item. Reference a constant such as {con} "
                "(manual input, in the constants folder).", m.start(), m.end())
        for m in re.finditer(r"\bITEM\s*\(\s*\"", code, re.I):
            args, close = call_args(code, code.index("(", m.start()))
            add("HIGH", "R05", "ITEM(\"literal\") is a hard-coded member. Use a constant.", m.start(), close + 1)
        for m in re.finditer(r"\.\s*'?(Name|Code|ID)'?\s*(=|<>)\s*\"[^\"]+\"", code):
            add("MED", "R05", "Text compare against a hard-coded name/code. Use a constant or a property flag.",
                max(0, m.start() - 30), m.end())

    # R06 picking a version by list order
    for m in re.finditer(r"(FIRST|LAST)NONBLANK\s*:\s*'?Version", code, re.I):
        add("HIGH", "R06", "Version picked by list order breaks when versions are added, renamed or deleted. "
            "Use [SELECT: Version = <version constant>].", m.start(), m.end())

    # R07 hard-coded dates
    for m in re.finditer(r"\bDATE\s*\(\s*\d{4}", code, re.I):
        add("HIGH", "R07", "Hard-coded date. Use a Date- or Dimension-typed constant input.", m.start(), m.end() + 10)

    # R08 modifier stacking
    mods = re.findall(r"\[\s*" + MODIFIERS + r"\b[^:\]]*:\s*([^\]\n]{0,60})", code, re.I)
    if len(mods) >= 6:  # the count alone is only a hint
        add("INFO", "R08", f"{len(mods)} modifiers. Could the source metric carry some of this (push it upstream)? "
            "Don't rewrite for the count alone; verify any compact rewrite against data.")

    def first_dim(v):
        v = re.sub(r"'[^']+'::", "", v)  # drop cross-app prefix
        m = re.search(r"'[^']+'|[A-Za-z_][\w.]*", v)
        return m.group(0) if m else ""

    seen = Counter((k.upper(), first_dim(v)) for k, v in mods)
    for (kind, dim), n in seen.items():
        if n > 1 and dim:
            add("MED", "R08", f"[{kind}: {dim} ...] appears {n} times. Apply it once.")

    # R09 needs a one-line explanation
    if "//" not in formula:
        add("LOW", "R09", "No // comment. Add a one-line explanation.")

    # R10 existence via net sums
    for m in re.finditer(r"<>\s*0\b", code):
        add("INFO", "R10", "If this tests whether something exists, count rows instead. Offsetting lines "
            "net to 0 and vanish.", max(0, m.start() - 50), m.end())

    return findings


ORDER = {"HIGH": 0, "MED": 1, "LOW": 2, "INFO": 3}


def report(findings, name):
    if not findings:
        print(f"OK  {name or '(formula)'}: no findings")
        return
    print(f"--  {name or '(formula)'}: {len(findings)} finding(s)")
    for f in sorted(findings, key=lambda f: ORDER[f["severity"]]):
        print(f"  {f['severity']:<4} {f['rule']}  {f['message']}")
        if f["snippet"]:
            print(f"            at: {f['snippet']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="")
    ap.add_argument("--formula")
    ap.add_argument("--jsonl")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--constant-prefix", default="CON ")
    ap.add_argument("--exempt-prefixes", default="ARM_,BP_,SEC_")
    a = ap.parse_args()
    exempt = tuple(p for p in (s.strip() for s in a.exempt_prefixes.split(",")) if p)

    items = []
    if a.jsonl:
        seen = set()
        with open(a.jsonl) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                o = json.loads(line)
                f = o.get("formula") or ""
                if f and f not in seen:
                    seen.add(f)
                    items.append((o.get("name") or "", f))
    else:
        items.append((a.name, a.formula if a.formula is not None else sys.stdin.read()))

    any_high = False
    totals, formulas_hit = Counter(), Counter()
    for name, f in items:
        fs = lint(f, name, a.constant_prefix, exempt)
        any_high |= any(x["severity"] == "HIGH" for x in fs)
        for x in fs:
            totals[(x["severity"], x["rule"])] += 1
        for key in {(x["severity"], x["rule"]) for x in fs}:
            formulas_hit[key] += 1
        if not a.summary:
            report(fs, name)

    if a.summary or len(items) > 1:
        print(f"\n{len(items)} formula(s) linted")
        for (sev, rule), n in sorted(totals.items(), key=lambda kv: (ORDER[kv[0][0]], kv[0][1])):
            print(f"  {sev:<4} {rule}: {n} finding(s) in {formulas_hit[(sev, rule)]} formula(s)")
    sys.exit(1 if any_high else 0)


if __name__ == "__main__":
    main()
