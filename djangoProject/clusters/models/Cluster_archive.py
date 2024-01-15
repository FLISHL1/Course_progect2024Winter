from django.db import models




class ClusterArchive(models.Model):
    type = models.CharField(primary_key=True, max_length=4)  # The composite primary key (type, id, date_archive) found, that is not supported. The first column is selected.
    id = models.IntegerField()
    cluster = models.IntegerField(blank=True, null=True)
    date_archive = models.DateField()

    class Meta:
        managed = False
        db_table = 'cluster_archive'
        unique_together = (('type', 'id', 'date_archive'),)