from django.db import models


class TypeOfTour(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name_of_type',)

    def __str__(self):
        return self.name

# class Tour(models.Model):
