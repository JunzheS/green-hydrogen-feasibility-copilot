"""OEM Intelligence engine — extracts OEM data already stored in project records."""
from collections import Counter, defaultdict


def build_oem_index(projects) -> dict:
    """Index all projects by their electrolyzer manufacturer OEM."""
    oems = defaultdict(list)
    for p in projects:
        raw = getattr(p, 'project_id', None)
        if raw is None:
            continue
        oem = _extract_oem(p)
        oems[oem].append(p)
    return dict(oems)


def _extract_oem(project) -> str:
    """Extract the primary OEM name from a project dataclass or dict."""
    if hasattr(project, 'oem'):
        return project.oem if project.oem else "Not Disclosed"
    return "Not Disclosed"


def search_oem(oem_index: dict, query: str = "") -> list:
    """Search OEMs by name substring."""
    results = []
    q = query.lower()
    for oem, projs in oem_index.items():
        if q in oem.lower():
            results.append((oem, projs))
    return sorted(results, key=lambda x: -len(x[1]))


def get_oem_summary(oems: dict) -> list[dict]:
    """Return a summary of each OEM with aggregated statistics."""
    summary = []
    for oem, projs in sorted(oems.items(), key=lambda x: -len(x[1])):
        techs = Counter(p.technology for p in projs)
        countries = Counter(p.country for p in projs)
        total_mw = sum(p.capacity_mw for p in projs if p.capacity_mw and p.capacity_mw < 5000)
        summary.append({
            "oem": oem,
            "project_count": len(projs),
            "total_mw": total_mw,
            "technologies": dict(techs),
            "countries": dict(countries),
            "projects": [{
                "project_id": p.project_id,
                "project_name": p.project_name,
                "technology": p.technology,
                "capacity_mw": p.capacity_mw,
                "country": p.country,
                "status": p.status,
            } for p in sorted(projs, key=lambda x: x.project_id)],
        })
    return summary


def build_developer_index(projects) -> dict:
    """Index all projects by their developer."""
    devs = defaultdict(list)
    for p in projects:
        raw_dev = getattr(p, 'developer', None) if hasattr(p, 'developer') else None
        if raw_dev is None:
            continue
        devs[raw_dev].append(p)
    return dict(devs)


def get_developer_summary(dev_index: dict) -> list[dict]:
    """Return aggregated developer portfolio statistics."""
    summary = []
    for dev, projs in sorted(dev_index.items(), key=lambda x: -len(x[1])):
        techs = Counter(p.technology for p in projs)
        total_mw = sum(p.capacity_mw for p in projs if p.capacity_mw and p.capacity_mw < 5000)
        countries = set(p.country for p in projs)
        statuses = Counter(p.status for p in projs)
        offtakes = Counter(p.primary_offtake for p in projs)
        summary.append({
            "developer": dev,
            "project_count": len(projs),
            "total_mw": total_mw,
            "countries_served": len(countries),
            "country_list": sorted(countries),
            "technologies": dict(techs),
            "statuses": dict(statuses),
            "offtakes": dict(offtakes),
            "projects": sorted([p.project_id for p in projs]),
        })
    return sorted(summary, key=lambda x: -x["project_count"])
