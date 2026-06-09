"""Centralised path configuration for the Copilot knowledge base."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_BASE = ROOT / "knowledge_base"

GOLD_DATASET_DIR = KNOWLEDGE_BASE / "project_references" / "gold_dataset"
RISK_LIBRARY_DIR = KNOWLEDGE_BASE / "risk_library"
COST_LIBRARY_DIR = KNOWLEDGE_BASE / "cost_library"
TECHNOLOGY_CARDS_DIR = KNOWLEDGE_BASE / "technology_cards"
TEMPLATES_DIR = KNOWLEDGE_BASE / "templates"

RISK_CATEGORIES = [
    "technical", "supply_chain", "grid_energy", "regulatory",
    "financial", "construction", "operational", "environmental"
]

COST_CATEGORIES = [
    "electrolyzer_system", "electrical_infrastructure", "water_systems",
    "hydrogen_processing", "civil_construction", "thermal_management",
    "instrumentation_controls", "indirect_owners_costs"
]
