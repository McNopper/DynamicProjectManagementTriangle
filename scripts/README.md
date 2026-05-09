# Scripts

## `gen_images.py`

Regenerates all SVG diagrams in `../images/` from a single source of truth.

**Run from the repository root:**

```bash
python scripts/gen_images.py
```

This produces:

- `images/classic.svg` — neutral classic triangle (Scope/Time/Cost)
- `images/perm1_FFV.svg` … `images/perm6_VVF.svg` — the six valid Fixed/Variable configurations
- `images/degen_FFF.svg`, `images/degen_VVV.svg` — degenerate (non-viable) cases

**Conventions used in the diagrams:**

- Green node, top band  → Variable
- Blue node, bottom band → Fixed
- Red node, no triangle → Not viable (degenerate cases)
- Italic centre label *Quality* → emergent outcome of the constraint configuration
- Degenerate cases are rendered as a flat horizontal line (no triangle) to visually convey non-viability.

Edit this script when changing canvas size, colours, or node positions, then re-run to regenerate all SVGs in one pass.
