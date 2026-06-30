# Pupil-Tracking Poster Figure — Design

**Date:** 2026-06-30
**Status:** Approved
**Branch:** `pupil-poster-figure`

## Purpose

A lean two-panel poster figure showcasing movement's eye-tracking analysis on the
`black` (dark surround) rotating-mouse dataset: (1) an example video frame with
the four tracked keypoints plus the pupil centroid overlaid, and (2) the
x-component of the normalized pupil-centroid velocity over time. Adapted from an
older sphinx-gallery draft (`draft_pupil_figure.py`), but reduced to the minimum
code for these two panels and rewritten as a Quarto document.

## Key Decisions

| Decision | Choice |
|----------|--------|
| File | `figures/pupil_tracking_poster.qmd` (flat, one figure per qmd) |
| Medium | `apply_style("poster")`; figure size `FIGSIZES["poster"]["double"]` (16×9) |
| Dataset | `black` only (`DLC_rotating-mouse_eye-tracking_stim-black.predictions.h5`), `with_video=True` |
| Layout | One row, two panels: `plt.subplots(1, 2, ...)` |
| Panel 1 | First frame (`video[0]`) + 4 keypoints at `position.isel(time=0)` + pupil-centroid marker |
| Panel 2 | x-velocity of normalized pupil centroid, time window `slice(10, 25)` s |
| Centroid color | `PALETTE["accent"]`, distinct `x` marker, labeled "centroid" |
| Export | `save_figure(fig, "pupil_tracking_poster")` → vector pdf+svg in `outputs/` |

## Data Flow

```python
from movement import sample_data
from movement.kinematics import compute_velocity
import sleap_io as sio

ds = sample_data.fetch_dataset(
    "DLC_rotating-mouse_eye-tracking_stim-black.predictions.h5",
    with_video=True,
)
frame0 = sio.load_video(ds.video_path)[0]          # first video frame
pos0 = ds.position.isel(time=0)                    # keypoints at frame 0
```

- **Panel 1** overlays keypoints from `pos0` (squeezing the singleton
  `individuals` dim) on `frame0`. The pupil centroid at frame 0 is
  `pos0.sel(keypoints=["pupil-L", "pupil-R"]).mean("keypoints")`. `isel(time=0)`
  guarantees the keypoints align with `video[0]`.
- **Panel 2** normalizes positions by subtracting the eye midpoint, takes the
  pupil centroid, computes velocity, and plots its x-component over the time
  window:

```python
eye_mid  = ds.position.sel(keypoints=["eye-L", "eye-R"]).mean("keypoints")
pos_norm = ds.position - eye_mid
pupil_c  = pos_norm.sel(keypoints=["pupil-L", "pupil-R"]).mean("keypoints")
velocity = compute_velocity(pupil_c)
velocity.sel(space="x").squeeze().sel(time=slice(10, 25)).plot.line(ax=ax_vel)
```

`with_video=True` downloads the video via pooch (cached; gitignored). Nothing
data-heavy is committed — only the rendered vector figure.

## Components

- **`figures/pupil_tracking_poster.qmd`** — the single deliverable. A short
  narrative + one `{python}` cell that loads the data, builds the two panels,
  styles, and saves. Mirrors the structure of `figures/example_trajectory.qmd`.

## Panel Details

**Panel 1 (`ax_frame`):**
- `imshow(frame0, cmap="gray")`.
- Scatter each of the 4 keypoints (labeled) → legend.
- Scatter the pupil centroid as an `x` in `PALETTE["accent"]`, labeled "centroid".
- `invert_yaxis()` (dataset captured flipped); ticks removed; short title.

**Panel 2 (`ax_vel`):**
- Line plot of normalized pupil-centroid x-velocity over `slice(10, 25)` s.
- Title; x-label "time (s)"; y-label "velocity (px/s)".

## Out of Scope (YAGNI — explicitly NOT ported from the draft)

- The second (`uniform`) dataset and any `xr.concat`/`lighting` dimension.
- Pupil-diameter, blink/squint distance, and rolling-filter smoothing sections.
- Normalized-position line plots and centroid-trajectory-on-video panels.
- `seaborn` styling and the draft's PNG `plt.savefig` calls (replaced by the
  shared style + `save_figure`).
- The draft file itself is reference-only; it is not part of the deliverable.

## Verification

- `uv run quarto render figures/pupil_tracking_poster.qmd` succeeds and writes
  `outputs/pupil_tracking_poster.pdf` and `.svg`.
- The full project still builds: `uv run quarto render` (the new figure appears
  in the gallery).
- Pre-commit hooks pass on the new `.qmd` (note: ruff does not lint `.qmd` cells,
  so the cell code is kept tidy by hand).
- Existing test suite remains green: `uv run pytest -q` → 12 passed.
