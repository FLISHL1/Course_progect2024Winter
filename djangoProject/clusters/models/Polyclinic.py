from django.db import models
import requests
from django.db import connection


class Polyclinic(models.Model):
    name = models.TextField()
    type = models.CharField(max_length=100)
    bed_fund = models.TextField()
    is_price = models.BooleanField()
    is_pharmacy_kiosk = models.BooleanField()
    is_ambulance = models.BooleanField()
    longitude = models.DecimalField(max_digits=19, decimal_places=17)
    latitude = models.DecimalField(max_digits=19, decimal_places=17)
    phone_number = models.CharField(max_length=25, null=True)
    address = models.TextField(null=True)
    URL_DATASET = ['https://apidata.mos.ru/v1/datasets/505/features?api_key=edeed7c9-a0b7-4bab-b12b-75fff06ca260',
                   'https://apidata.mos.ru/v1/datasets/506/features?api_key=edeed7c9-a0b7-4bab-b12b-75fff06ca260',
                   'https://apidata.mos.ru/v1/datasets/503/features?api_key=edeed7c9-a0b7-4bab-b12b-75fff06ca260',
                   'https://apidata.mos.ru/v1/datasets/502/features?api_key=edeed7c9-a0b7-4bab-b12b-75fff06ca260']

    @staticmethod
    def update_polyclinic():
        Polyclinic.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE clusters_polyclinic AUTO_INCREMENT = 1;")

        for url in Polyclinic.URL_DATASET:
            response = requests.get(url)
            response = response.json()
            Polyclinic.objects.bulk_create([Polyclinic.create_polyclinic(feature) for feature in response['features']])

    @staticmethod
    def create_polyclinic(feature):
        coordinates = feature['geometry']['coordinates'][0]
        attribute = feature['properties']['attributes']

        polyclinic = Polyclinic(
            name=attribute['ShortName'],
            type=attribute['Category'],
            bed_fund=attribute['BedSpace'],
            is_price=False if attribute['PaidServiceInfo'] == "" else True,
            is_pharmacy_kiosk=False if attribute['DrugStore'] == "нет" else True,
            is_ambulance=False if attribute['AmbulanceStation'] == "нет" else True,
            longitude=float(coordinates[0]),
            latitude=float(coordinates[1]))

        polyclinic.phone_number = attribute['PublicPhone'][0]["PublicPhone"] if len(
            attribute['PublicPhone']) > 0 else None
        polyclinic.address = attribute["ObjectAddress"][0]["Address"] if len(attribute["ObjectAddress"]) > 0 else None
        return polyclinic
