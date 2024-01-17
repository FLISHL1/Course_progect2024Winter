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
        results = ClustersBundels.objects.values("cluster").order_by("cluster").distinct()
        if user.is_authenticated:
            clusters_name = {}
            for cluster in Cluster_name.Name.objects.filter(id_user=user).distinct():
                clusters_name[cluster.cluster] = cluster.name

        result = {}
        for cluster in results:
            if cluster["cluster"] is None: continue

            if user.is_authenticated and cluster["cluster"] in list(clusters_name.keys()):
                result[cluster["cluster"]] = clusters_name[cluster["cluster"]]
            else:
                result[cluster["cluster"]] = cluster["cluster"]
        return result

    @staticmethod
    def get_all_points(cluster_id):
        if str(cluster_id) == "-1":
            result = ClustersBundels.objects.raw("""SELECT bund.*, ifnull (f.address, p.address) as address, ifnull (f.name, p.name) as name, ifnull (f.phone_number, p.phone_number) as phone_number, ifnull (f.name, p.name) as name, ifnull(f.type, p.type) as typeModel FROM clusters_bundels as bund
                                                        LEFT JOIN clusters_food as f ON bund.type = 'F' and bund.id = f.id
                                                        LEFT JOIN clusters_polyclinic as p ON bund.type = 'P' and bund.id = p.id
                                                        WHERE bund.cluster is null;""")
        else:
            result = ClustersBundels.objects.raw("""SELECT bund.*, ifnull (f.address, p.address) as address, ifnull (f.name, p.name) as name, ifnull (f.phone_number, p.phone_number) as phone_number, ifnull (f.name, p.name) as name, ifnull(f.type, p.type) as typeModel FROM clusters_bundels as bund
                                                        LEFT JOIN clusters_food as f ON bund.type = 'F' and bund.id = f.id
                                                        LEFT JOIN clusters_polyclinic as p ON bund.type = 'P' and bund.id = p.id
                                                        WHERE bund.cluster = %(cluster_id)s;""",
                                                 {"cluster_id": cluster_id})
        list = []
        for i in result:
            phone_number = "Нет телефона"
            if i.phone_number is not None and i.phone_number.capitalize() != phone_number:
                phone_number = "+7" + i.phone_number.capitalize()

            list.append({
                'type': i.typeModel.capitalize(),
                'name': i.name.capitalize(),
                'address': i.address,
                'phone_number': phone_number,
                "id": f"{i.type}-{i.id}",
                'cluster': i.cluster if i.cluster is not None else 0,
                'latitude': float(i.latitude),
                'longitude': float(i.longitude)
            })
        return list

    @staticmethod
    def get_selection(cluster_id: int, count: int = 10,
                      user: User = None):
        list = []

        if str(cluster_id) == "-1":
            cluster_id = None
            result = ClustersBundels.objects.raw("""SELECT bund.*, ifnull (f.address, p.address) as address, ifnull (f.name, p.name) as name, ifnull (f.phone_number, p.phone_number) as phone_number, ifnull (f.name, p.name) as name, ifnull(f.type, p.type) as typeModel FROM clusters_bundels as bund
                                                        LEFT JOIN clusters_food as f ON bund.type = 'F' and bund.id = f.id
                                                        LEFT JOIN clusters_polyclinic as p ON bund.type = 'P' and bund.id = p.id
                                                        WHERE bund.cluster is null;""")
        else:
            result = ClustersBundels.objects.raw("""SELECT bund.*, ifnull (f.address, p.address) as address, ifnull (f.name, p.name) as name, ifnull (f.phone_number, p.phone_number) as phone_number, ifnull (f.name, p.name) as name, ifnull(f.type, p.type) as typeModel FROM clusters_bundels as bund
                                                        LEFT JOIN clusters_food as f ON bund.type = 'F' and bund.id = f.id
                                                        LEFT JOIN clusters_polyclinic as p ON bund.type = 'P' and bund.id = p.id
                                                        WHERE bund.cluster = %(cluster_id)s
                                                        LIMIT %(count)s;""", {"cluster_id": cluster_id, "count": count})

        for i in result:
            object = None
            if cluster_id is None and user.is_authenticated:
                object = Cluster_name_increased.NameIncreased.objects.filter(type=i.type, id_increased=i.id,
                                                                             id_user=user).all()
                if len(object) > 0:
                    object = object[0].name
                else:
                    object = None
            phone_number = "Нет телефона"
            if i.phone_number is not None and i.phone_number.capitalize() != phone_number:
                phone_number = "+7" + i.phone_number.capitalize()

            list.append({
                'type': i.typeModel.capitalize(),
                'name': i.name.capitalize(),
                'address': i.address if i.address is not None else 'Адрес не найден',
                'phone_number': phone_number,
                "id": f"{i.type}-{i.id}",
                'id_name': object
            })
        return list

    @staticmethod
    def update_items():
        ClustersBundels.objects.all().delete()

        Food.update_food()
        Polyclinic.update_polyclinic()

        with connection.cursor() as cursor:
            cursor.execute("CALL update_bundle();")
            cursor.execute("CALL runDBScanTest(0.02, 4);")
            cursor.close()
        print("Update successful")

    class Meta:
        managed = False
        db_table = 'clusters_bundels'
        unique_together = (('type', 'id'),)
