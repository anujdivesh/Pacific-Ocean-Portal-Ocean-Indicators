from __future__ import annotations

import os
from typing import Optional

import geopandas as gpd
import numpy as np
import requests


def getEEZ(
    ax,
    m=None,
    local_path: Optional[str] = None,
    geojson_url: Optional[str] = None,
    color: str = "black",
    linewidth: float = 1,
    linestyle: str = "--",
):
    """Plot EEZ boundaries from a local file (preferred) or a GeoServer GeoJSON URL."""
    gdf = None

    if local_path is not None and os.path.exists(local_path):
        try:
            if local_path.endswith(".zip"):
                gdf = gpd.read_file(f"zip://{local_path}")
            else:
                gdf = gpd.read_file(local_path)
        except Exception as exc:  # pragma: no cover
            print(f"Failed to read local file {local_path}: {exc}")

    if gdf is None and geojson_url is not None:
        try:
            geojson_response = requests.get(geojson_url, timeout=60)
            if geojson_response.status_code == 200:
                geojson_data = geojson_response.json()
                gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
            else:  # pragma: no cover
                print(
                    f"Failed to retrieve GeoJSON from {geojson_url} (HTTP {geojson_response.status_code})"
                )
        except Exception as exc:  # pragma: no cover
            print(f"Error fetching GeoJSON from {geojson_url}: {exc}")

    if gdf is None:
        print("No EEZ data available to plot.")
        return

    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    else:
        gdf = gdf.to_crs("EPSG:4326")

    for geom in gdf.geometry:
        if geom is None:
            continue
        if not geom.is_valid:
            geom = geom.buffer(0)

        def _plot_xy(x, y):
            x = np.asarray(x)
            x = np.where(x < 0, x + 360, x)
            ax.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle)

        geom_type = geom.geom_type
        if geom_type == "LineString":
            x, y = geom.xy
            _plot_xy(x, y)
        elif geom_type == "MultiLineString":
            for line in geom.geoms:
                x, y = line.xy
                _plot_xy(x, y)
        elif geom_type == "Polygon":
            x, y = geom.exterior.xy
            _plot_xy(x, y)
        elif geom_type == "MultiPolygon":
            for poly in geom.geoms:
                x, y = poly.exterior.xy
                _plot_xy(x, y)
