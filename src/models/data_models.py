"""Domain data models for the Copilot feasibility engine."""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class Technology(str, Enum):
    PEM = "PEM"
    ALKALINE = "Alkaline"
    PEM_ALKALINE = "PEM+Alkaline"
    AGNOSTIC = "technology_agnostic"


class ProjectStatus(str, Enum):
    OPERATIONAL = "operational"
    UNDER_CONSTRUCTION = "under_construction"
    PLANNED = "planned"
    DECOMMISSIONED = "decommissioned"
    CANCELLED = "cancelled"


class RiskClass(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConfidenceClass(str, Enum):
    A_ACTUAL = "A_actual_cost"
    B_CONTRACTED = "B_contracted_price"
    C_BENCHMARK = "C_industry_benchmark"
    D_ESTIMATE = "D_analyst_estimate"


class GateOutcome(str, Enum):
    PROCEED = "PROCEED"
    PROCEED_WITH_CAUTION = "PROCEED WITH CAUTION"
    DO_NOT_PROCEED = "DO NOT PROCEED"
    INSUFFICIENT_DATA = "INSUFFICIENT DATA"


@dataclass
class Query:
    country: str
    industry: str
    technology: str
    capacity_mw: float
    target_cod: int

    technology_enum: Technology = Technology.PEM
    offtake: str = ""
    scale_category: str = ""
    region: str = "europe"
    country_iso: str = ""


@dataclass
class ProjectReference:
    project_id: str
    project_name: str
    country: str
    region: str
    technology: str
    capacity_mw: float
    status: str
    primary_offtake: str
    secondary_offtakes: list[str] = field(default_factory=list)
    total_capex_eur: Optional[float] = None
    capex_per_kw_eur: Optional[float] = None
    narrative_summary: str = ""
    is_first_of_a_kind: bool = False
    data_completeness_tier: str = ""
    developer: str = ""
    oem: str = ""


@dataclass
class MatchedProject:
    project: ProjectReference
    rank: int
    composite_score: float
    tech_score: float
    industry_score: float
    capacity_score: float
    country_score: float
    maturity_score: float
    tier: str
    rationale: str


@dataclass
class RiskRecord:
    risk_id: str
    risk_name: str
    risk_category: str
    risk_subcategory: str
    probability: int
    impact: int
    detectability: int
    rpn: int
    risk_class: str
    description_summary: str
    consequences_summary: str
    mitigation_summary: str
    technology_types: list[str] = field(default_factory=list)
    project_scales: list[str] = field(default_factory=list)
    project_phases: list[str] = field(default_factory=list)
    reference_project_ids: list[str] = field(default_factory=list)
    foak_only: bool = False


@dataclass
class CostRecord:
    cost_id: str
    cost_name: str
    cost_category: str
    cost_subcategory: str
    cost_basis: str
    eur_per_kw: float
    eur_per_kw_low: float
    eur_per_kw_high: float
    cost_year: int
    technology_type: str
    project_scale_mw: float
    scale_is_extrapolated: bool
    confidence_level: str
    percentage_of_total_capex: Optional[float] = None
    learning_rate_percent: Optional[float] = None
    project_reference_id: Optional[str] = None
    greenfield_or_brownfield: Optional[str] = None
    sensitivity_to_scale: Optional[str] = None


@dataclass
class TechnologyCard:
    technology_id: str
    technology_name: str
    technology_type: str
    trl: int
    commercial_maturity: str
    system_efficiency_kwh_per_kg: float
    stack_lifetime_hours: int
    output_pressure_bar: float
    hydrogen_purity_percent: float
    degradation_rate_pct_per_year: float
    ramp_rate_pct_per_second: float
    min_load_percent: float
    cold_start_minutes: int
    capex_stack_central: float
    capex_stack_low: float
    capex_stack_high: float
    learning_rate_pct: float
    stack_replacement_eur_per_kw: float
    advantages: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    scaling_constraints: list[str] = field(default_factory=list)
    primary_applications: list[str] = field(default_factory=list)
    suitability_scores: dict = field(default_factory=dict)
