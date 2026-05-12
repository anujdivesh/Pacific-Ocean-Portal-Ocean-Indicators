from __future__ import annotations

from typing import Any, Dict, List


# Minimal station metadata used by notebooks.
# Source: GeoJSON FeatureCollection provided in chat (EPSG:4326).
# Note: filenames are derived from station_id to avoid inconsistencies.
STATIONS: List[Dict[str, Any]] = [
    {
        "spotter_id": "INT_TP001",
        "country_co": "CK",
        "country_na": "Cook Islands",
        "location": "Avatiu",
        "station_id": "IDO70051",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP003",
        "country_co": "FJ",
        "country_na": "Fiji",
        "location": "Lautoka",
        "station_id": "IDO70054",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP004",
        "country_co": "FJ",
        "country_na": "Fiji",
        "location": "Suva",
        "station_id": "IDO70063",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP002",
        "country_co": "FM",
        "country_na": "Federated States of Micronesia",
        "location": "Dekehtik",
        "station_id": "IDO70057",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP005",
        "country_co": "KI",
        "country_na": "Kiribati",
        "location": "Tarawa (Betio)",
        "station_id": "IDO70060",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP007",
        "country_co": "NR",
        "country_na": "Nauru",
        "location": "Nauru",
        "station_id": "IDO70055",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP023",
        "country_co": "SB",
        "country_na": "Solomon Islands",
        "location": "Honiara",
        "station_id": "IDO70061",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP025",
        "country_co": "TO",
        "country_na": "Tonga",
        "location": "Nuku'alofa",
        "station_id": "IDO70053",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP026",
        "country_co": "TV",
        "country_na": "Tuvalu",
        "location": "Funafuti",
        "station_id": "IDO70056",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP027",
        "country_co": "VU",
        "country_na": "Vanuatu",
        "location": "Port Vila",
        "station_id": "IDO70059",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP022",
        "country_co": "WS",
        "country_na": "Samoa",
        "location": "Apia",
        "station_id": "IDO70062",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_TP015",
        "country_co": "PNG",
        "country_na": "Papua New Guinea",
        "location": "Lombrum",
        "station_id": "IDO70058",
        "is_active": "Y",
    },
    {
        "spotter_id": "INT_EB066",
        "country_co": "MH",
        "country_na": "Marshall Islands",
        "location": "Uliga",
        "station_id": "IDO70052",
        "is_active": "Y",
    },
]


def active_stations() -> List[Dict[str, Any]]:
    return [s for s in STATIONS if str(s.get("is_active", "Y")).upper() == "Y"]


def get_station(station_id: str) -> Dict[str, Any]:
    station_id = station_id.strip()
    for station in STATIONS:
        if station.get("station_id") == station_id:
            return station
    raise KeyError(f"Unknown station_id: {station_id}")


def default_filename(station_id: str) -> str:
    station_id = station_id.strip()
    return f"{station_id}SLD.txt"


def build_bom_url(station_id: str) -> str:
    station_id = station_id.strip()
    filename = default_filename(station_id)
    return f"https://reg.bom.gov.au/ntc/{station_id}/{filename}"
