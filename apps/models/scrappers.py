from django.db import models


class Scrappers(models.Model):
    class Meta:
        managed = False
        db_table = "scrappers"

    provider = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    url = models.TextField()
