from django.db import models

class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name
