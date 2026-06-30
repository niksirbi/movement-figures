"""Layered, medium-aware matplotlib styling."""

from importlib.resources import files

import matplotlib.pyplot as plt

AVAILABLE_MEDIA: tuple[str, ...] = ("manuscript", "poster", "presentation")

_STYLE_DIR = files("movement_figures") / "styles"

# ColorBrewer Set2 — movement's brand categorical palette (matches the base
# axes.prop_cycle in movement-base.mplstyle).
SET2: tuple[str, ...] = (
    "#66c2a5",
    "#fc8d62",
    "#8da0cb",
    "#e78ac3",
    "#a6d854",
    "#ffd92f",
    "#e5c494",
    "#b3b3b3",
)

# Semantic colors drawn from the cohesive Set2 / Dark2 / Pastel2 family.
PALETTE: dict[str, str] = {
    "primary": "#66c2a5",  # Set2 teal
    "secondary": "#fc8d62",  # Set2 orange
    "accent": "#e7298a",  # Dark2 magenta (vivid)
    "muted": "#b3b3b3",  # Set2 grey
    "highlight": "#f4cae4",  # Pastel2 pink (light marks on dark)
    "ink": "#666666",  # Dark2 grey (dark neutral)
}

# Figure dimensions in inches, per medium.
FIGSIZES: dict[str, dict[str, tuple[float, float]]] = {
    "manuscript": {"single": (3.5, 2.6), "double": (7.0, 4.0)},
    "poster": {"single": (8.0, 6.0), "double": (16.0, 9.0)},
    "presentation": {"single": (6.0, 4.0), "double": (12.0, 6.75)},
}


def apply_style(medium: str = "manuscript") -> None:
    """Apply the shared base style plus a medium-specific override.

    Parameters
    ----------
    medium : str
        One of ``AVAILABLE_MEDIA``. Defaults to ``"manuscript"``.

    Raises
    ------
    ValueError
        If ``medium`` is not a known medium.
    """
    if medium not in AVAILABLE_MEDIA:
        raise ValueError(f"Unknown medium {medium!r}; choose from {AVAILABLE_MEDIA}.")
    base = str(_STYLE_DIR / "movement-base.mplstyle")
    override = str(_STYLE_DIR / f"movement-{medium}.mplstyle")
    plt.style.use([base, override])
