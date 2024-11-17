from django.contrib.gis.db import models

class Lieu(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    location = models.PointField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lieu : {self.name}"

    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"    