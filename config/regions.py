from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .paths import EEZ_COUNTRY_DIR


BBOX_PAD: Mapping[str, float] = {"lon": 2.0, "lat": 2.0}

# Bounding boxes use lon in 0..360 (Pacific-centered convention)
BBOXES: Mapping[str, Mapping[str, float]] = {
    "ASM": {"west": 186.1, "east": 194.9, "south": -17.6, "north": -9.9},
    "COK": {"west": 191.2, "east": 205.4, "south": -25.6, "north": -5.5},
    "FJI": {"west": 172.5, "east": 184.0, "south": -25.5, "north": -9.5},
    "FSM": {"west": 135.0, "east": 166.0, "south": -1.5, "north": 14.0},
    "GUM": {"west": 141.0, "east": 149.0, "south": 10.0, "north": 16.0},
    "KIR": {"west": 167.5, "east": 213.5, "south": -14.5, "north": 8.5},
    "MHL": {"west": 157.0, "east": 176.0, "south": 1.6, "north": 18.2},
    "MNP": {"west": 141.0, "east": 150.0, "south": 12.0, "north": 24.0},
    "NCL": {"west": 156.0, "east": 170.7, "south": -26.3, "north": -14.7},
    "PACIFIC": {"west": 100.0, "east": 300.0, "south": -45.0, "north": 45.0},
    "PCN": {"west": 226.5, "east": 239.0, "south": -28.5, "north": -20.5},
    "PLW": {"west": 129.0, "east": 137.5, "south": 1.5, "north": 12.0},
    "PNG": {"west": 139.0, "east": 163.0, "south": -15.0, "north": 3.0},
    "PYF": {"west": 201.4, "east": 228.5, "south": -31.5, "north": -4.0},
    "SLB": {"west": 154.5, "east": 173.9, "south": -16.4, "north": -4.0},
    "TKL": {"west": 184.0, "east": 192.1, "south": -11.1, "north": -6.3},
    "TON": {"west": 180.5, "east": 189.0, "south": -26.0, "north": -14.0},
    "TUV": {"west": 172.5, "east": 183.5, "south": -13.5, "north": -3.5},
    "VUT": {"west": 163.0, "east": 173.7, "south": -21.9, "north": -11.9},
    "WLF": {"west": 179.4, "east": 185.9, "south": -16.0, "north": -9.7},
    "WSM": {"west": 185.4, "east": 189.6, "south": -16.0, "north": -10.8},
    "NIU": {"west": 187.5, "east": 194.0, "south": -22.9, "north": -16.5},
    "NRU": {"west": 163.3, "east": 169.7, "south": -4.0, "north": 2.8},
}

EEZ_FILES: Mapping[str, str] = {
    "ASM": "ASM.zip",
    "COK": "COK.zip",
    "FJI": "FJI.zip",
    "FSM": "FSM.zip",
    "GUM": "GUM.zip",
    "KIR": "KIR.zip",
    "MHL": "MHL.zip",
    "MNP": "MNP.zip",
    "NCL": "NCL.zip",
    "PACIFIC": "PAC_EEZ_v3.zip",
    "PCN": "PCN.zip",
    "PLW": "PLW.zip",
    "PNG": "PNG.zip",
    "PYF": "PYF.zip",
    "SLB": "SLB.zip",
    "TKL": "TKL.zip",
    "TON": "TON.zip",
    "TUV": "TUV.zip",
    "VUT": "VUT.zip",
    "WLF": "WLF.zip",
    "WSM": "WSM.zip",
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

    # Padding only for country zooms (everything except the full PACIFIC domain)
    if region != "PACIFIC":
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
