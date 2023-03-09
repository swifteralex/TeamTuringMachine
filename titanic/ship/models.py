import datetime

from django.db import models
from django.utils import timezone
from django import forms

class Operator(models.Model):
    operator_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.operator_text

class ShipName(models.Model):
    ship_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.ship_name