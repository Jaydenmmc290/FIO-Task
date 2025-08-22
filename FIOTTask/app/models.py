from django.db import models

# Create your models here.
class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.CharField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10)
    updated_date = models.DateTimeField(auto_now=True)
    adpi_response = models.TextField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    
    def __str__(self):
        return f"{self.city} - {self.temperature}°C, {self.description}"