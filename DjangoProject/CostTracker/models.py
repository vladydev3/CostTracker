from django.db import models

class Cost(models.Model):
    category = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    file = models.FileField(upload_to='uploads/')