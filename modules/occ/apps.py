# modules/occ/apps.py
from django.apps import AppConfig

class OccConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.occ'  # <--- MUST be 'modules.occ', not just 'occ'

