from django.contrib.auth.models import User

from django.db import models
from django.db import connection

import clusters.models.Clusters as clusters
from clusters.models import Food, Polyclinic, Cluster_archive, Cluster_name, Cluster_name_increased


class ClustersBundels(models.Model):
    type = models.CharField(primary_key=True, max_length=4)
    id = models.IntegerField()
    latitude = models.DecimalField(max_digits=19, decimal_places=17, blank=True, null=True)
    longitude = models.DecimalField(max_digits=19, decimal_places=17, blank=True, null=True)
    cluster = models.IntegerField(blank=True, null=True)

    @staticmethod
    def get_all_cluster(user: User = None):
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT DISTINCT cluster FROM clusters_bundels ORDER BY cluster")
        #     results = cursor.fetchall()
        #     cursor.close()
        results = clusters.ClustersBundels.objects.values("cluster").order_by("cluster").distinct()

        if user is not None:
            clusters_name = {}
            for cluster in Cluster_name.Name.objects.filter(id_user=user).distinct():
                clusters_name[cluster.cluster] = cluster.name

        result = {}
        for cluster in results:
            if cluster["cluster"] is None: continue

            if user is not None and cluster["cluster"] in list(clusters_name.keys()):
                result[cluster["cluster"]] = clusters_name[cluster["cluster"]]
            else:
                result[cluster["cluster"]] = cluster["cluster"]
        return result

    @staticmethod
    def get_selection(cluster_id: int, count: int = 10,
                      user: User = None):
        list = []
        objects = ClustersBundels.objects.filter(cluster=cluster_id).order_by("?")[:count].all()
        if str(cluster_id) == "-1":
            cluster_id = None
            objects = ClustersBundels.objects.filter(cluster=cluster_id).order_by("?").all()
        for i in objects:
            if cluster_id is None:
                object = Cluster_name_increased.NameIncreased.objects.filter(type=i.type, id_increased=i.id, id_user=user).all()
                if len(object) > 0:
                    object = object[0].name
                else:
                    object= None
            else:
                object = None

            match (str(i.type)):
                case "F":
                    food = Food.objects.get(id=i.id)
                    list.append({
                        'type': food.type.capitalize(),
                        'name': food.name.capitalize(),
                        'address': food.address,
                        'phone_number': (
                                "+7" + food.phone_number.capitalize()) if food.phone_number.capitalize() != "Нет телефона" else food.phone_number.capitalize(),
                        "id": f"F-{food.id}",
                        'id_name': object
                    })
                case "P":
                    polyclinic = Polyclinic.objects.get(id=i.id)
                    list.append({
                        'type': polyclinic.type.capitalize(),
                        'name': polyclinic.name.capitalize(),
                        'address': polyclinic.address,
                        'phone_number': (
                                "+7 " + polyclinic.phone_number) if polyclinic.phone_number is not None else "Нет номера телефона",
                        "id": f"P-{polyclinic.id}",
                        "id_name": object
                    })

        return list

    @staticmethod
    def update_items():

        ClustersBundels.objects.all().delete()

        Food.update_food()
        Polyclinic.update_polyclinic()

        with connection.cursor() as cursor:
            cursor.execute("CALL update_bundle();")
            cursor.execute("CALL runDBScanTest(0.029, 4);")
            cursor.close()
        print("Update successful")

    class Meta:
        managed = False
        db_table = 'clusters_bundels'
        unique_together = (('type', 'id'),)
