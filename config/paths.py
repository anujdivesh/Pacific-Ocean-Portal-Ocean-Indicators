from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

# Non-Python assets live under config/shapefiles/...
SHAPEFILES_DIR = ROOT_DIR / "config" / "shapefiles"

# EEZ zipped layers per-country live here
EEZ_COUNTRY_DIR = SHAPEFILES_DIR / "final_eez_country"
