"""PDF/HTML export component for assessment reports."""
from datetime import datetime


def generate_html_report(query: dict, report: dict) -> str:
    """Generate a self-contained HTML report for browser print-to-PDF."""

    q = query
    tech = report.get("technology_assessment", {})
    capex = report.get("capex_assessment", {})
    lcoh = report.get("lcoh_assessment", {})
    risk = report.get("risk_assessment", {})
    pm = report.get("pm_review", {})
    matching = report.get("similar_projects", {})
    ranked = matching.get("ranked_projects", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    def esc(text):
        if not text:
            return ""
        return (str(text).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    gate = pm.get("gate_outcome", "-")
    g_color = {"PROCEED": "#2E7D32", "PROCEED WITH CAUTION": "#F9A825",
               "DO NOT PROCEED": "#C62828", "INSUFFICIENT DATA": "#78909C"}.get(gate, "#78909C")

    proj_rows = "".join(
        f"<tr><td>{p['rank']}</td><td>{esc(p['project_name'])}</td><td>{esc(p['country'])}</td>"
        f"<td>{p['capacity_mw']} MW</td><td>{esc(p['technology'])}</td>"
        f"<td style='text-align:right'>{p['composite_score']:.2f}</td><td>{esc(p['tier'])}</td></tr>"
        for p in ranked
    )

    risk_rows = "".join(
        f"<tr><td><span class='badge'>{r['risk_class'].upper()}</span></td>"
        f"<td>{esc(r['risk_name'][:80])}</td><td style='text-align:center'>{r['rpn']}</td>"
        f"<td>{esc(r.get('category','').replace('_',' ').title())}</td></tr>"
        for r in risk.get("top_risks", [])[:8]
    )

    capex_rows = "".join(
        f"<tr><td>{esc(b['category'])}</td><td style='text-align:right'>{b['eur_per_kw']:.0f}</td>"
        f"<td style='text-align:right'>{b['eur_m']:.1f}</td><td style='text-align:right'>{b['pct_of_total']:.1f}%</td></tr>"
        for b in capex.get("breakdown", [])
    )

    lcoh_rows = "".join(
        f"<tr><td>{esc(d['component'])}</td><td style='text-align:right'>{d['eur_per_kg']:.2f}</td>"
        f"<td style='text-align:right'>{d['pct']:.0f}%</td></tr>"
        for d in lcoh.get("decomposition", [])
    )

    dims = pm.get("dimension_scores", {})
    dim_labels = {"project_references": "References", "technology": "Technology",
                  "risk": "Risk", "economics": "Economics"}
    dim_rows = "".join(
        f"<tr><td>{dim_labels.get(k,k)}</td><td>{d.get('quality','-')}</td>"
        f"<td>{d.get('confidence',0):.2f}</td></tr>"
        for k, d in dims.items()
    )

    gaps_critical = "".join(
        f'<div class="gap-critical"><strong>CRITICAL:</strong> {esc(g)}</div>'
        for g in pm.get("critical_gaps", [])
    )
    gaps_important = "".join(
        f'<div class="gap-important"><strong>IMPORTANT:</strong> {esc(g)}</div>'
        for g in pm.get("important_gaps", [])
    )
    conditions_list = "".join(
        f"<li>{esc(c)}</li>" for c in pm.get("conditions", [])
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>H2 Pre-Feasibility Assessment - {esc(q.get('country',''))} {q.get('capacity_mw','')} MW {esc(q.get('technology',''))}</title>
<style>
body {{ font-family:'Segoe UI',Arial,sans-serif; max-width:900px; margin:40px auto; padding:0 20px; color:#333; line-height:1.5; }}
h1 {{ color:#1a1a2e; border-bottom:3px solid {g_color}; padding-bottom:10px; }}
h2 {{ color:#1B5E20; margin-top:30px; border-bottom:1px solid #ddd; padding-bottom:5px; }}
table {{ width:100%; border-collapse:collapse; margin:10px 0 20px; }}
th,td {{ padding:8px 12px; border:1px solid #ddd; text-align:left; }}
th {{ background:#F1F8E9; font-weight:600; }}
tr:nth-child(even) {{ background:#FAFAFA; }}
.gate-banner {{ background:{g_color}; color:white; padding:20px; border-radius:8px; margin:20px 0; text-align:center; }}
.gate-banner h2 {{ color:white; margin:0; border:none; }}
.metric-row {{ display:flex; gap:20px; margin:15px 0; }}
.metric {{ flex:1; background:#F1F8E9; padding:15px; border-radius:8px; text-align:center; }}
.metric-value {{ font-size:1.5em; font-weight:700; color:#1B5E20; }}
.metric-label {{ font-size:0.85em; color:#558B2F; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:4px; color:white; font-size:0.85em; font-weight:600; }}
.gap-critical {{ background:#FFEBEE; padding:8px; border-left:4px solid #C62828; margin:5px 0; }}
.gap-important {{ background:#FFFDE7; padding:8px; border-left:4px solid #F9A825; margin:5px 0; }}
.footer {{ margin-top:40px; padding-top:20px; border-top:1px solid #ddd; font-size:0.85em; color:#999; }}
@media print {{ body {{ margin:0; padding:0; }} }}
</style>
</head>
<body>

<h1>Green Hydrogen Pre-Feasibility Assessment</h1>
<p><strong>Project:</strong> {esc(q.get('capacity_mw',''))} MW {esc(q.get('technology',''))} Electrolysis | {esc(q.get('country',''))} | {esc(q.get('industry',''))} | COD {q.get('target_cod','')}</p>
<p><strong>Generated:</strong> {now} | <strong>Copilot Engine v1.0</strong></p>

<div class="gate-banner">
  <h2>{gate}</h2>
  <p>Confidence: {pm.get('overall_confidence',{}).get('label','')} ({pm.get('overall_confidence',{}).get('score',0):.2f})</p>
</div>

<div class="metric-row">
  <div class="metric"><div class="metric-value">EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M</div><div class="metric-label">CAPEX (Central)</div></div>
  <div class="metric"><div class="metric-value">EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg</div><div class="metric-label">LCOH (Central)</div></div>
  <div class="metric"><div class="metric-value">TRL {tech.get('trl','')}</div><div class="metric-label">Technology Readiness</div></div>
  <div class="metric"><div class="metric-value">{risk.get('total_filtered',0)}</div><div class="metric-label">Risks Assessed</div></div>
</div>

<h2>1. Technology Assessment</h2>
<p><strong>Technology:</strong> {esc(tech.get('technology_name',''))} (TRL {tech.get('trl','')} - {esc(tech.get('commercial_maturity',''))})</p>
<p><strong>Suitability for {esc(q.get('industry',''))}:</strong> {tech.get('application_suitability','').upper()}</p>
<p>{esc(tech.get('trl_rationale',''))}</p>
<p><strong>Scale:</strong> {esc(tech.get('scale_status','').replace('_',' '))} (max: {tech.get('max_proven_mw','')} MW)</p>

<h2>2. Reference Projects (Top {len(ranked)})</h2>
<table><tr><th>#</th><th>Project</th><th>Country</th><th>Capacity</th><th>Tech</th><th>Score</th><th>Relevance</th></tr>{proj_rows}</table>

<h2>3. Risk Assessment</h2>
<p>Critical: {risk.get('risk_count_by_class',{}).get('critical',0)} | High: {risk.get('risk_count_by_class',{}).get('high',0)} | Medium: {risk.get('risk_count_by_class',{}).get('medium',0)} | Low: {risk.get('risk_count_by_class',{}).get('low',0)}</p>
<table><tr><th>Class</th><th>Risk</th><th>RPN</th><th>Category</th></tr>{risk_rows}</table>

<h2>4. CAPEX Assessment</h2>
<p><strong>Central:</strong> EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M (EUR {capex.get('total',{}).get('central_eur_per_kw',0):.0f}/kW)</p>
<p><strong>Range:</strong> EUR {capex.get('total',{}).get('p10_eur_m',0):.0f}M - EUR {capex.get('total',{}).get('p90_eur_m',0):.0f}M</p>
<table><tr><th>Category</th><th>EUR/kW</th><th>EUR M</th><th>%</th></tr>{capex_rows}</table>

<h2>5. LCOH Assessment</h2>
<p><strong>Central:</strong> EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg (P10: EUR {lcoh.get('p10_eur_per_kg',0):.2f} - P90: EUR {lcoh.get('p90_eur_per_kg',0):.2f})</p>
<p><strong>Dominant Driver:</strong> {lcoh.get('dominant_driver','').replace('_',' ').title()}</p>
<table><tr><th>Component</th><th>EUR/kg</th><th>%</th></tr>{lcoh_rows}</table>
<p><em>{esc(str(lcoh.get('data_quality_note',''))[:250])}</em></p>

<h2>6. PM Review</h2>
<table><tr><th>Dimension</th><th>Quality</th><th>Confidence</th></tr>{dim_rows}</table>

<h3>Knowledge Gaps</h3>
{gaps_critical}{gaps_important}

<h3>Conditions for Advancement</h3>
<ol>{conditions_list}</ol>

<div class="footer">
<p>Generated by Green Hydrogen Project Feasibility Copilot - Engine v1.0</p>
<p>KB: 10 projects | 30 risks | 30 cost records | 2 tech cards</p>
<p>Pre-feasibility estimate. CAPEX: AACE Class 4. LCOH: Class D. Not for investment decisions.</p>
</div>
</body>
</html>"""
