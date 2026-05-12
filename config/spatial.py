from __future__ import annotations

import numpy as np


def subset_to_bbox(lat, lon_wrapped, values, bbox):
    """Subset a 2D array to a bbox.

    Expects:
    - lat: 1D array (south..north)
    - lon_wrapped: 1D array in 0..360
    - values: 2D array [lat, lon]
    - bbox: dict with west/east/south/north
    """
    lat_mask = (lat >= bbox["south"]) & (lat <= bbox["north"])
    lon_mask = (lon_wrapped >= bbox["west"]) & (lon_wrapped <= bbox["east"])

    lat_sub = lat[lat_mask]
    lon_sub = lon_wrapped[lon_mask]
    values_sub = values[lat_mask, :][:, lon_mask]

    lon2d, lat2d = np.meshgrid(lon_sub, lat_sub)
    return lon2d, lat2d, values_sub
