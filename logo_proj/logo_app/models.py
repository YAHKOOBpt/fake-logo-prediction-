
from django.db import models

class LogoPrediction(models.Model):
    image = models.ImageField(upload_to='logo_images/')
    result = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.result
    

