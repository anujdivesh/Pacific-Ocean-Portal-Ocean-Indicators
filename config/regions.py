from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .paths import EEZ_COUNTRY_DIR


BBOX_PAD: Mapping[str, float] = {"lon": 2.0, "lat": 2.0}

# Bounding boxes use lon in 0..360 (Pacific-centered convention)
BBOXES: Mapping[str, Mapping[str, float]] = {
    "PACIFIC": {"west": 100.0, "east": 300.0, "south": -45.0, "north": 45.0},
    "NIU": {"west": 187.5, "east": 194.0, "south": -22.9, "north": -16.5},
    "NRU": {"west": 163.3, "east": 169.7, "south": -4.0, "north": 2.8},
}

EEZ_FILES: Mapping[str, str] = {
    "PACIFIC": "PAC_EEZ_v3.zip",
    "NRU": "NRU.zip",
    "NIU": "NIU.zip",
}


@dataclass(frozen=True)
class RegionSettings:
    region: str
    bbox: Dict[str, float]
    eez_zip_path: str


def region_bbox(region: str) -> Dict[str, float]:
    """Return bbox for region (optionally padded for country zooms)."""
    if region not in BBOXES:
        raise ValueError(f"Unknown region={region!r}. Known: {sorted(BBOXES.keys())}")

    bbox = dict(BBOXES[region])

    # Padding only for country zooms
    if region in ("NRU", "NIU"):
        bbox["west"] -= float(BBOX_PAD["lon"])
        bbox["east"] += float(BBOX_PAD["lon"])
        bbox["south"] -= float(BBOX_PAD["lat"])
        bbox["north"] += float(BBOX_PAD["lat"])

    return bbox


def eez_zip_path(region: str, eez_dir: Path | None = None) -> str:
    """Return absolute path to the EEZ zip for a region."""
    if region not in EEZ_FILES:
        raise ValueError(f"Unknown region={region!r}. Known: {sorted(EEZ_FILES.keys())}")

    base_dir = eez_dir or EEZ_COUNTRY_DIR
    return str(Path(base_dir) / EEZ_FILES[region])


def resolve_region_settings(region: str, *, eez_dir: Path | None = None) -> Tuple[Dict[str, float], str]:
    """Convenience helper used by notebooks."""
    return region_bbox(region), eez_zip_path(region, eez_dir=eez_dir)
