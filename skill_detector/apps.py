from django.apps import AppConfig
from .DB_operator import init_skill_vectors, get_skill_vectors


class SkillDetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skill_detector'


# init_skill_vectors()
SKILL_IDS, SKILL_VECTORS = get_skill_vectors()
