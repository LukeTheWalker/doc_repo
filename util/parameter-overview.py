#!/usr/bin/env python3
"""
This script extracts lists of input parameters from all models and creates an
overview that can be copied to our Jekyll docs. This way, comments on the input
parameters in the code are directly reflected in the documentation.

Original bash version: (c) Matthias Hoelzl, 2019
Python port preserves the original logic.

Usage: ./util/parameter-overview.py

Run from the repository root (the directory containing the `models/` folder).
"""

import os
import re
import sys
import glob
from pathlib import Path

# Models to skip
SKIP_MODELS = {
    "001", "002", "003", "004", "005",
    "303", "305", "306", "307", "333",
    "401", "500", "501", "502",
}

OUTFILE = "input.md"

JEKYLL_HEADER = """---
title: "List of input parameters"
nav_order: 2
parent: "Compiling and Running"
layout: default
render_with_liquid: false
---

<!--
  AUTO-GENERATED FILE - DO NOT EDIT BY HAND.
  Regenerate by running ./util/parameter-overview.py from the repo root.
-->

<style>
  .params-table { table-layout: fixed; width: 100%; font-size: 0.9em; }
  .params-table th, .params-table td {
      word-wrap: break-word; vertical-align: top; padding: 4px 6px;
  }
  .params-table th:nth-child(1), .params-table td:nth-child(1) { width: 12%; }
  .params-table th:nth-child(2), .params-table td:nth-child(2) { width: 10%; }
  .params-table th:nth-child(3), .params-table td:nth-child(3) { width: 38%; }
  .params-table th:nth-child(n+4), .params-table td:nth-child(n+4) {
      width: 2.5em; text-align: center;
  }
</style>

# List of input parameters

> **⚠️ Auto-generated file — do not edit manually.**
> This page is generated from the Fortran sources. Any manual changes will be
> overwritten the next time the generator runs. To update it, run
> `./util/parameter-overview.py` from the repository root and commit the result.

"""


def extract_namelist_params(model_file):
    """
    Reproduces the bash pipeline:
        grep /in1/ <file> -A 999 | grep -v "^#" | grep "&" -A 1 | ...

    Starts at the first line containing "/in1/", then keeps every line that is
    part of a namelist continuation (lines containing "&" and the line right
    after them). Splits the resulting blob on whitespace/commas/ampersands and
    returns a sorted set of unique parameter names.
    """
    try:
        with open(model_file, "r", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return set()

    # Find the first line containing "/in1/"
    start = None
    for i, line in enumerate(lines):
        if "/in1/" in line:
            start = i
            break
    if start is None:
        return set()

    # Mimic `grep -A 999`: take up to 999 lines after the match (inclusive)
    region = lines[start:start + 1000]

    # Drop preprocessor lines (grep -v "^#")
    region = [ln for ln in region if not ln.lstrip().startswith("#")]

    # Mimic `grep "&" -A 1`: keep lines containing '&' and the line immediately
    # after each such match.
    kept = []
    keep_next = False
    for ln in region:
        if "&" in ln:
            kept.append(ln)
            keep_next = True
        elif keep_next:
            kept.append(ln)
            keep_next = False

    # Concatenate into a single string, then strip everything up to the last
    # "/ " segment (the bash sed: 's|^.*/ ||').
    blob = "".join(kept).replace("\n", "")
    # Replace ampersands and commas with spaces, collapse tabs/whitespace.
    blob = re.sub(r"[&,]", " ", blob)
    blob = blob.replace("\t", " ")
    blob = re.sub(r"\s+", " ", blob)

    # 's|^.*/ ||' — strip everything up to and including the last "/ "
    idx = blob.rfind("/ ")
    if idx != -1:
        blob = blob[idx + 2:]

    tokens = [t for t in blob.split(" ") if t]
    return set(tokens)


def find_variables(file_path):
    """
    Reproduces:
        grep -B 9999 'contains' $file | egrep '^[^!]*::' | sed ... | tr ' ' '\n'

    Returns the ordered list of variable names declared before the first
    `contains` line in a Fortran source file.
    """
    try:
        with open(file_path, "r", errors="replace") as f:
            content = f.read()
    except OSError:
        return []

    lines = content.split("\n")

    # Find the first "contains" line (case sensitive, like the original grep
    # without -i) and only consider lines before it.
    contains_idx = None
    for i, ln in enumerate(lines):
        if "contains" in ln:
            contains_idx = i
            break
    if contains_idx is not None:
        lines = lines[:contains_idx + 1]  # grep -B includes the matching line

    # egrep '^[^!]*::' — lines whose first non-comment portion contains '::'
    # The pattern means: from start, zero or more non-'!' chars, then '::'.
    decl_re = re.compile(r"^[^!]*::")
    decls = [ln for ln in lines if decl_re.search(ln)]

    out_tokens = []
    for ln in decls:
        # 's/^.*:://' — strip everything up to and including the last '::'
        ln = re.sub(r"^.*::", "", ln)
        # 's/!.*$//' — strip trailing comment
        ln = re.sub(r"!.*$", "", ln)
        # 's/([^)]*)//g' — strip parenthesised dimension specs like (3)
        ln = re.sub(r"\([^)]*\)", "", ln)
        # 's/=.*//' — strip initialisation
        ln = re.sub(r"=.*", "", ln)
        # 's/&//' — strip continuation marker
        ln = ln.replace("&", "")
        # 's/,/ /g' — commas become spaces
        ln = ln.replace(",", " ")
        ln = ln.replace("\t", " ")
        ln = re.sub(r"\s+", " ", ln).strip()
        if ln:
            out_tokens.extend(ln.split(" "))

    return [t for t in out_tokens if t]


def build_comm_text():
    """Concatenate broadcast_phys.f90 with the broadcast_vacuum subroutine."""
    parts = []
    try:
        with open("communication/broadcast_phys.f90", "r", errors="replace") as f:
            parts.append(f.read())
    except OSError:
        print("Warning: could not read communication/broadcast_phys.f90",
              file=sys.stderr)

    try:
        with open("vacuum/vacuum.f90", "r", errors="replace") as f:
            vac = f.read()
        # Extract from `subroutine broadcast_vacuum` to `end subroutine broadcast_vacuum`
        m = re.search(
            r"^ *subroutine broadcast_vacuum.*?end subroutine broadcast_vacuum",
            vac, flags=re.DOTALL | re.MULTILINE,
        )
        if m:
            parts.append(m.group(0))
    except OSError:
        print("Warning: could not read vacuum/vacuum.f90", file=sys.stderr)

    return "\n".join(parts)


def is_communicated(param, comm_text):
    r"""
    Replicates: egrep -i "^[^!]*\([ \t]*$param[ ,(]" tmp_$$_comm
    Returns True if any non-comment line contains "(<ws>param" followed by
    space, comma, or another '('.
    """
    pat = re.compile(
        r"^[^!]*\([ \t]*" + re.escape(param) + r"[ ,(]",
        re.IGNORECASE | re.MULTILINE,
    )
    return bool(pat.search(comm_text))


def get_description(file_path, param):
    """
    Replicates:
        egrep -i "^[^!]* $param[( ]" $file | grep "!" | sed ...

    Pulls inline comments from declaration lines for `param`.
    """
    try:
        with open(file_path, "r", errors="replace") as f:
            lines = f.read().split("\n")
    except OSError:
        return ""

    pat = re.compile(
        r"^[^!]* " + re.escape(param) + r"[( ]",
        re.IGNORECASE,
    )

    descs = []
    for ln in lines:
        if not pat.search(ln):
            continue
        if "!" not in ln:
            continue
        # 's/^.*![< ]*//' — strip everything up to '!' and any following '<' or spaces
        m = re.search(r"!", ln)
        if not m:
            continue
        rest = ln[m.end():]
        rest = re.sub(r"^[< ]*", "", rest)
        # 's/\\f//g' — strip backslash-f
        rest = rest.replace("\\f", "")
        descs.append(rest)

    joined = ";".join(descs)
    # Trailing-semicolon strip, plus the small bash cosmetic substitutions.
    joined = re.sub(r";$", "", joined)
    joined = joined.replace("((", "( (").replace("))", ") )")
    joined = joined.replace("//", "/ /")
    return joined.strip()


def get_phys_default(param):
    """
    Replicates:
        egrep -i "^[^!] $param[ =(]" models/preset_parameters.f90 | sed ...

    Note the original bash uses "^[^!]" (no '*'), which means: starts with a
    single non-'!' character, then a literal space and the parameter. We
    preserve that behaviour exactly.
    """
    file_path = "models/preset_parameters.f90"
    try:
        with open(file_path, "r", errors="replace") as f:
            lines = f.read().split("\n")
    except OSError:
        return ""

    pat = re.compile(
        r"^[^!] " + re.escape(param) + r"[ =(]",
        re.IGNORECASE,
    )

    parts = []
    for ln in lines:
        if not pat.search(ln):
            continue
        # 's/^[^!]*= *//' — strip everything up to the first '=' (and trailing space)
        m = re.search(r"=\s*", ln)
        if not m:
            continue
        rest = ln[m.end():]
        # 's/!.*$//' — drop trailing comment
        rest = re.sub(r"!.*$", "", rest)
        # 's| *(/ *||' and 's| */) *||' — strip array constructor brackets
        rest = re.sub(r" *\(/ *", "", rest)
        rest = re.sub(r" */\) *", "", rest)
        # 's/d0//g' — strip Fortran double-precision suffix
        rest = rest.replace("d0", "")
        # 's/rst_hdf5_version_supported//'
        rest = rest.replace("rst_hdf5_version_supported", "")
        rest = rest.rstrip()
        parts.append(rest)

    return " ".join(parts).strip()


def get_vacuum_default(param):
    """
    Replicates the bash pipeline that pulls defaults from the
    `vacuum_preset` subroutine in vacuum/vacuum.f90.
    """
    try:
        with open("vacuum/vacuum.f90", "r", errors="replace") as f:
            content = f.read()
    except OSError:
        return ""

    m = re.search(
        r"^ *subroutine vacuum_preset.*?end subroutine vacuum_preset",
        content, flags=re.DOTALL | re.MULTILINE,
    )
    if not m:
        return ""
    region = m.group(0).split("\n")

    # grep "$param[ =(]" — bare grep, no anchors, case sensitive
    pat = re.compile(re.escape(param) + r"[ =(]")

    parts = []
    for ln in region:
        if not pat.search(ln):
            continue
        # 's/^[^!]*= *//'
        m2 = re.search(r"=\s*", ln)
        if not m2:
            continue
        rest = ln[m2.end():]
        # 's/!.*$//'
        rest = re.sub(r"!.*$", "", rest)
        # 's/d0//g'
        rest = rest.replace("d0", "")
        parts.append(rest.strip())

    return " ".join(parts).strip()


def insert_header(out, models):
    """Write the table header row."""
    parts = ["parameter", "default", "description"] + list(models)
    out.write("| " + " | ".join(parts) + " |\n")
    out.write("|" + "|".join(["---"] * len(parts)) + "|\n")


def md_escape(text):
    """Minimal escaping so the description doesn't break a markdown table."""
    if text is None:
        return ""
    # Pipes break tables; replace with the HTML entity.
    return text.replace("|", "\\|").strip()


def emit_section(out, title, params, models, model_params,
                 description_source, default_fn, comm_text):
    """
    Render one of the two sections (`phys_module` or `vacuum`) as a markdown
    subsection with a single table. Only parameters that appear in at least
    one model's namelist are emitted.
    """
    out.write(f"## {title}\n\n")
    insert_header(out, models)

    seen = set()
    for param in params:
        # Preserve original ordering but skip duplicates from multiple decls.
        if param in seen:
            continue
        seen.add(param)

        # Special case: bcs is documented separately on its own wiki page,
        # so we don't enumerate which models use it or look up its default.
        if param.lower() == "bcs":
            description = md_escape(description_source(param))
            default = "see [its wiki page](/docs/howto/choose_boundary_conditions.md)"
            row = [f"**{param}**", default, description] + [""] * len(models)
            out.write("| " + " | ".join(row) + " |\n")
            continue

        # Only emit params that appear in at least one model namelist.
        in_any = any(param.lower() in {p.lower() for p in model_params[m]}
                     for m in models)
        if not in_any:
            continue

        if not is_communicated(param, comm_text):
            print(f"Warning: Parameter {param} might not get communicated!",
                  file=sys.stderr)

        description = md_escape(description_source(param))
        default = md_escape(default_fn(param))

        row = [f"**{param}**", default, description]
        for model in models:
            present = param.lower() in {p.lower() for p in model_params[model]}
            row.append("x" if present else "")
        out.write("| " + " | ".join(row) + " |\n")

    # Attach CSS class to the table (kramdown IAL on the line right after).
    out.write("{: .params-table}\n\n")


def main():
    if not os.path.isdir("models"):
        print("Error: 'models/' directory not found. Run this script from the "
              "repository root.", file=sys.stderr)
        sys.exit(1)

    # Collect models, sorted by their numeric/string id (matches `ls -1d`).
    model_dirs = sorted(glob.glob("models/model*/initialise_parameters.f90"))
    models = []
    model_params = {}
    for path in model_dirs:
        m = re.search(r"models/model([^/]+)/initialise_parameters\.f90$", path)
        if not m:
            continue
        model_id = m.group(1)
        if model_id in SKIP_MODELS:
            continue
        models.append(model_id)
        model_params[model_id] = extract_namelist_params(path)

    if not models:
        print("Error: no model directories found.", file=sys.stderr)
        sys.exit(1)

    comm_text = build_comm_text()

    phys_vars = find_variables("models/phys_module.f90")
    vacu_vars = find_variables("vacuum/vacuum.f90")

    with open(OUTFILE, "w") as out:
        out.write(JEKYLL_HEADER)

        emit_section(
            out, "phys_module", phys_vars, models, model_params,
            description_source=lambda p: get_description("models/phys_module.f90", p),
            default_fn=get_phys_default,
            comm_text=comm_text,
        )

        emit_section(
            out, "vacuum", vacu_vars, models, model_params,
            description_source=lambda p: get_description("vacuum/vacuum.f90", p),
            default_fn=get_vacuum_default,
            comm_text=comm_text,
        )

    print(f"Wrote {OUTFILE}")


if __name__ == "__main__":
    main()