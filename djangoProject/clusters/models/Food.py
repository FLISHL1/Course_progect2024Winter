import requests
from django.db import models
from django.db import connection
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
class Food(models.Model):
    name = models.TextField()
    type = models.CharField(max_length=50)
    count_seats = models.IntegerField()
    is_social = models.BooleanField(default=False)
    longitude = models.DecimalField(max_digits=19, decimal_places=17)
    latitude = models.DecimalField(max_digits=19, decimal_places=17)
    is_net_object = models.BooleanField()
    phone_number = models.CharField(max_length=30, null=True, default=None)

    @staticmethod
    def update_food():
        Food.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE clusters_food AUTO_INCREMENT = 1;")
        count_response = int(requests.get(
            'https://apidata.mos.ru/v1/datasets/1903/count?api_key=edeed7c9-a0b7-4bab-b12b-75fff06ca260').text)
        foods = []
        for i in range(0, count_response, 1000):
            print(i)
            response = requests.get(
                f'https://apidata.mos.ru/v1/datasets/1903/features?api_key=edeed7c9-a0b7-4bab-b12b-75fff06ca260&$skip={i}')
            response = response.json()
            for feature in response['features']:
                foods.append(Food.create_food(feature))
        Food.objects.bulk_create(foods)
    @staticmethod
    def create_food(feature):
        coordinates = feature['geometry']['coordinates']
        attribute = feature['properties']['attributes']
        food = Food(name=attribute['Name'],
                    type=attribute['TypeObject'],
                    count_seats=attribute['SeatsCount'],
                    is_social=False if attribute['SocialPrivileges'] == "нет" else True,
                    is_net_object=False if attribute['IsNetObject'] == "нет" else True,
                    longitude=float(coordinates[0]),
                    latitude=float(coordinates[1]))
        food.phone_number = attribute['PublicPhone'][0]["PublicPhone"] if len(attribute['PublicPhone']) > 0 else None

        return food

