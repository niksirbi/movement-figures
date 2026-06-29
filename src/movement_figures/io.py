"""Consistent vector export for figures."""

from collections.abc import Sequence
from pathlib import Path

from matplotlib.figure import Figure


def save_figure(
    fig: Figure,
    name: str,
    formats: Sequence[str] = ("pdf", "svg"),
    output_dir: str | Path = "outputs",
) -> list[Path]:
    """Save ``fig`` as vector files named ``<name>.<fmt>`` in ``output_dir``.

    Returns the list of written paths. Creates ``output_dir`` if absent.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for fmt in formats:
        path = output_dir / f"{name}.{fmt}"
        fig.savefig(path)
        paths.append(path)
    return paths
