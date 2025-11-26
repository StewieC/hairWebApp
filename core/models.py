# core/models.py
from django.db import models

HAIR_TYPES = [
    ('straight', 'Straight'),
    ('wavy', 'Wavy'),
    ('curly', 'Curly'),
    ('coily', 'Coily'),
]

SCALP_TYPES = [
    ('dry', 'Dry'),
    ('oily', 'Oily'),
    ('normal', 'Normal'),
    ('combination', 'Combination'),
]

class QuizResponse(models.Model):
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPES)
    scalp_type = models.CharField(max_length=20, choices=SCALP_TYPES)
    concerns = models.JSONField(default=list)  # e.g. ["frizz", "breakage"]
    porosity = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hair_type} - {self.scalp_type}"