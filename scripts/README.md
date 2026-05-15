# Scripts

## `gen_images.py`

Regenerates all diagrams in `../figures/` from a single source of truth.
Each diagram is written as both SVG (used by the README) and PDF (included
in `paper.tex`).

**Run from the repository root:**

```bash
python scripts/gen_images.py
```

Requires the `cairosvg` Python package for the SVG → PDF conversion.

This produces, for each of:

- `classic` — neutral classic triangle (Scope/Time/Cost)
- `perm1_FFV` … `perm6_VVF` — the six valid Fixed/Variable configurations
- `degen_FFF`, `degen_VVV` — degenerate (non-viable) cases

both a `.svg` and a `.pdf` file in `figures/`.

**Conventions used in the diagrams:**

- Green node, top band  → Variable
- Blue node, bottom band → Fixed
- Red node, no triangle → Not viable (degenerate cases)
- Italic centre label *Quality* → emergent outcome of the constraint configuration
- Degenerate cases are rendered as a flat horizontal line (no triangle) to visually convey non-viability.

Edit this script when changing canvas size, colours, or node positions, then re-run to regenerate all SVGs in one pass.
