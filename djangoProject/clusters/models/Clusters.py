from django.db import models

import requests
from django.db import models
from django.db import connection
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from clusters.models import Food, Polyclinic


class ClustersBundels(models.Model):
    type = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    latitude = models.DecimalField(max_digits=19, decimal_places=17, blank=True, null=True)
    longitude = models.DecimalField(max_digits=19, decimal_places=17, blank=True, null=True)
    cluster = models.IntegerField(blank=True, null=True)

    @staticmethod
    def get_all_cluster():
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT cluster FROM clusters_bundels ORDER BY cluster")
            results = cursor.fetchall()
            cursor.close()
        return [result[0] for result in results if result[0] is not None]
    @staticmethod
    def get_selection(cluster_id: int, count:int = 10):
        list = []
        if str(cluster_id) == "-1":
            cluster_id = None
        for i in ClustersBundels.objects.filter(cluster=cluster_id).order_by("?")[:count].all():
            match (str(i.type)):
                case "F":
                    food = Food.objects.get(id=i.id)
                    list.append({
                        'type': food.type.capitalize(),
                        'name': food.name.capitalize(),
                        'address': "",
                        'phone_number': ("+7" + food.phone_number.capitalize()) if food.phone_number.capitalize() != "Нет телефона" else food.phone_number.capitalize()
                    })
                case "P":
                    polyclinic = Polyclinic.objects.get(id=i.id)
                    list.append({
                        'type': polyclinic.type.capitalize(),
                        'name': polyclinic.name.capitalize(),
                        'address': "",
                        'phone_number': ("+7 " + polyclinic.phone_number) if polyclinic.phone_number is not None else "Нет номера телефона"
                    })

        return list

    class Meta:
        managed = False
        db_table = 'clusters_bundels'
        unique_together = (('type', 'id'),)
