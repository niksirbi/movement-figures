"""Shared style and helpers for movement research figures."""

from movement_figures.io import data_dir, save_figure
from movement_figures.layout import (
    move_colorbar_to_divider,
    reserve_colorbar_space,
)
from movement_figures.style import (
    AVAILABLE_MEDIA,
    PALETTE,
    SET2,
    WIDTHS,
    apply_style,
    figure_size,
)

__all__ = [
    "AVAILABLE_MEDIA",
    "PALETTE",
    "SET2",
    "WIDTHS",
    "apply_style",
    "data_dir",
    "figure_size",
    "move_colorbar_to_divider",
    "reserve_colorbar_space",
    "save_figure",
]
