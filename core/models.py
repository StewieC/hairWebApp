# core/models.py
from django.db import models

class HairRoutine(models.Model):
    # Match quiz answers
    hair_type = models.CharField(max_length=20, choices=[
        ('straight', 'Straight'),
        ('wavy', 'Wavy'),
        ('curly', 'Curly'),
        ('coily', 'Coily'),
        ('any', 'Any'),
    ], default='any')
    
    scalp_type = models.CharField(max_length=20, choices=[
        ('dry', 'Dry'), ('oily', 'Oily'), ('normal', 'Normal'), ('combination', 'Combination'), ('any', 'Any')
    ], default='any')
    
    porosity = models.CharField(max_length=20, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('any', 'Any')
    ], blank=True, default='any')
    
    concerns = models.JSONField(default=list, blank=True)  # e.g. ["frizz", "breakage"]
    
    # The actual routine advice
    title = models.CharField(max_length=200, default="Your Custom Routine")
    wash_frequency = models.CharField(max_length=200)
    products_recommended = models.TextField()
    styling_tips = models.TextField()
    avoid_list = models.TextField(blank=True)
    priority = models.IntegerField(default=0)  # higher = more specific rule wins

    def __str__(self):
        return f"Routine for {self.hair_type} {self.scalp_type}"
    
    class Meta:
        ordering = ['-priority']