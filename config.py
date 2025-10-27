"""Configuration constants for AI Prompt Studio."""

APP_NAME = "AI PROMPT STUDIO"
PRIMARY_COLOR = "#188d6d"
FONT_FAMILY = "Work Sans"

ADMIN_ROUTE = "admincoreteam50"
COPILOT_URL = "https://copilot.microsoft.com"  # Placeholder

# Seeds
SEED_METIERS = [
    {"id": "sales", "name": "Sales", "icon": "sales.svg", "is_active": True}
]

SEED_CATEGORIES = [
    {"metier_id": "sales", "name": "Prospection", "is_active": True},
    {"metier_id": "sales", "name": "Account Planning", "is_active": True},
    {"metier_id": "sales", "name": "Négociation", "is_active": True},
]

SEED_AUTHORS = [
    {"id": "mansouryoum", "display_name": "MansourYoum", "is_active": True}
]


