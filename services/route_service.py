import os, requests, logging
from typing import Tuple

log = logging.getLogger(__name__)

PROVIDER    = os.getenv("ROUTE_PROVIDER", "ors")             # "ors" | "google"
ORS_KEY     = os.getenv("ORS_API_KEY", "")
GOOGLE_KEY  = os.getenv("GOOGLE_MAPS_API_KEY", "")

def _call_ors(pickup: str, drop: str) -> Tuple[int, int, str]:
    # lat,lng → lng,lat for ORS
    p_lng, p_lat = pickup.split(",")[1], pickup.split(",")[0]
    d_lng, d_lat = drop.split(",")[1],   drop.split(",")[0]
    body = {"coordinates": [[float(p_lng), float(p_lat)], [float(d_lng), float(d_lat)]]}
    r = requests.post(
        f"https://api.openrouteservice.org/v2/directions/driving-car",
        json=body,
        headers={"Authorization": ORS_KEY, "Content-Type": "application/json"},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    seg  = data["routes"][0]["summary"]
    poly = data["routes"][0]["geometry"]
    return int(seg["distance"]), int(seg["duration"]), poly

def _call_google(pickup: str, drop: str):
    r = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params={"origin": pickup, "destination": drop, "key": GOOGLE_KEY},
        timeout=10
    )
    r.raise_for_status()
    data = r.json()
    leg  = data["routes"][0]["legs"][0]
    distance_m = leg["distance"]["value"]
    duration_s = leg["duration"]["value"]
    poly       = data["routes"][0]["overview_polyline"]["points"]
    return distance_m, duration_s, poly

def compute_route(pickup: str, drop: str):
    try:
        if PROVIDER == "google":
            return _call_google(pickup, drop)
        return _call_ors(pickup, drop)
    except Exception as exc:
        log.warning("Route API failed: %s", exc)
        return None, None, None
