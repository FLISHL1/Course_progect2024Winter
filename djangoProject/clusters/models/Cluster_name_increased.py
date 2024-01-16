from django.contrib.auth.models import User
from django.db import models


class NameIncreased(models.Model):
    type = models.CharField(max_length=4, blank=True, null=True)
    id_increased = models.IntegerField(blank=True, null=True)
    id_user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cluster_name_increased'