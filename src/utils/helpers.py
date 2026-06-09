"""Utility functions: country mapping, offtake mapping, scoring helpers."""
import math
from typing import Optional

# === Country normalisation ===
COUNTRY_MAP: dict[str, str] = {
    "france": "France", "fr": "France", "french": "France",
    "germany": "Germany", "de": "Germany", "deutschland": "Germany",
    "spain": "Spain", "es": "Spain", "españa": "Spain", "espana": "Spain",
    "netherlands": "Netherlands", "nl": "Netherlands", "holland": "Netherlands",
    "belgium": "Belgium", "be": "Belgium",
    "portugal": "Portugal", "pt": "Portugal",
    "denmark": "Denmark", "dk": "Denmark",
    "italy": "Italy", "it": "Italy",
}

# === Industry-to-offtake mapping ===
INDUSTRY_OFFTAKE_MAP: dict[str, str] = {
    "steel": "steel", "steel industry": "steel", "green steel": "steel",
    "refinery": "refinery", "refining": "refinery", "oil refining": "refinery",
    "ammonia": "ammonia", "fertilizer": "ammonia", "fertilizers": "ammonia",
    "methanol": "methanol",
    "mobility": "mobility", "transport": "mobility", "transportation": "mobility",
    "chemicals": "ammonia", "chemical industry": "ammonia",
    "industrial hydrogen": "refinery", "industrial_hydrogen": "refinery",
    "industrial heat": "industrial_heat", "industrial_heating": "industrial_heat",
    "grid injection": "grid_injection", "power generation": "grid_injection",
    "export": "export",
}

# === Broad industry → multi-match ===
BROAD_INDUSTRY_MAP: dict[str, list[tuple[str, float]]] = {
    "chemicals": [("ammonia", 1.0), ("methanol", 1.0), ("refinery", 0.4)],
    "chemical industry": [("ammonia", 1.0), ("methanol", 1.0), ("refinery", 0.4)],
    "industrial hydrogen": [("refinery", 1.0), ("steel", 1.0), ("ammonia", 1.0), ("industrial_heat", 0.7)],
    "industrial_hydrogen": [("refinery", 1.0), ("steel", 1.0), ("ammonia", 1.0), ("industrial_heat", 0.7)],
}

# === Offtake related groups ===
OFFTAKE_GROUPS: dict[str, list[str]] = {
    "industrial": ["refinery", "steel", "ammonia", "methanol"],
    "energy_mobility": ["mobility", "grid_injection", "industrial_heat"],
    "trade": ["export"],
}

# === Country neighbour matrix ===
NEIGHBOURS: dict[str, list[str]] = {
    "France": ["Germany", "Spain", "Belgium", "Italy"],
    "Germany": ["France", "Netherlands", "Denmark", "Belgium", "Poland"],
    "Spain": ["France", "Portugal"],
    "Netherlands": ["Germany", "Belgium"],
    "Belgium": ["France", "Germany", "Netherlands"],
    "Portugal": ["Spain"],
    "Denmark": ["Germany"],
}

# === Sub-region groupings ===
SUB_REGIONS: dict[str, list[str]] = {
    "Western Europe": ["France", "Germany", "Netherlands", "Belgium"],
    "Southern Europe": ["Spain", "Portugal", "Italy"],
    "Northern Europe": ["Denmark", "Sweden", "Norway", "Finland"],
}


def normalise_country(raw: str) -> str:
    """Map free-text country input to ISO short name."""
    return COUNTRY_MAP.get(raw.strip().lower(), raw.strip())


def normalise_industry(raw: str) -> str:
    """Map free-text industry to offtake enum value."""
    key = raw.strip().lower()
    if key in BROAD_INDUSTRY_MAP:
        return key  # preserve for multi-match
    return INDUSTRY_OFFTAKE_MAP.get(key, raw.strip())


def get_industry_matches(industry: str) -> list[tuple[str, float]]:
    """Get offtake match targets for an industry query.
    Returns list of (offtake_enum, score) tuples."""
    key = industry.strip().lower()
    if key in BROAD_INDUSTRY_MAP:
        return BROAD_INDUSTRY_MAP[key]
    mapped = INDUSTRY_OFFTAKE_MAP.get(key, key)
    return [(mapped, 1.0)]


def compute_capacity_score(query_mw: float, project_mw: float) -> float:
    """Logarithmic capacity similarity score. Symmetric, bounded [0,1]."""
    if project_mw <= 0 or query_mw <= 0:
        return 0.0
    ratio = query_mw / project_mw
    score = 1.0 - 0.5 * abs(math.log10(ratio))
    return max(0.0, min(1.0, score))


def compute_country_score(query_country: str, project_country: str) -> float:
    """Geographic proximity score."""
    if query_country == project_country:
        return 1.00
    neighbours = NEIGHBOURS.get(query_country, [])
    if project_country in neighbours:
        return 0.70
    for region_countries in SUB_REGIONS.values():
        if query_country in region_countries and project_country in region_countries:
            return 0.50
    return 0.40  # same continent (all current projects are Europe)


def compute_maturity_score(status: str, target_cod: Optional[int] = None) -> float:
    """Project maturity score with optional target_cod boost."""
    base = {
        "under_construction": 1.00,
        "operational": 0.80,
        "planned": 0.50,
        "decommissioned": 0.30,
        "cancelled": 0.20,
    }
    score = base.get(status, 0.40)
    if target_cod and target_cod <= 2027:
        if status == "operational":
            score = 1.00
        elif status == "under_construction":
            score = 0.90
    if target_cod and target_cod >= 2030:
        if status == "planned":
            score = 0.60
    return score


def is_in_same_offtake_group(query_offtake: str, project_offtake: str) -> bool:
    """Check if two offtakes belong to the same related group."""
    for members in OFFTAKE_GROUPS.values():
        if query_offtake in members and project_offtake in members:
            return True
    return False


CAPACITY_CATEGORIES = [
    (10, "small_<10mw"),
    (100, "medium_10-100mw"),
    (500, "large_100-500mw"),
    (float("inf"), "very_large_>500mw"),
]


def get_scale_category(mw: float) -> str:
    for threshold, label in CAPACITY_CATEGORIES:
        if mw <= threshold:
            return label
    return "very_large_>500mw"
