from django.db import models


class Users(models.Model):

    class Meta:
        db_table = "cms_users"

    id = models.AutoField(primary_key=True, null=False, empty=False)
    username = models.CharField(max_length=255, null=False)
