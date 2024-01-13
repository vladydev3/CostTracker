from django.db import models

class Cost(models.Model):
    """
    Represents a cost.

    Attributes:
        category (str): The category of the cost.
        amount (float): The amount of the cost.
        date (datetime): The date of the cost.
    """
    category = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    file = models.FileField(upload_to='uploads/')