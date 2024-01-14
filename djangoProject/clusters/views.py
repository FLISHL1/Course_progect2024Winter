import json

from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
import requests
import clusters.schedule
from clusters.models import Food, Polyclinic, Clusters
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore



@login_required
def update(request):
    Food.update_food()
    Polyclinic.update_polyclinic()
    return HttpResponse("Okl")

def test():
    Food.update_food()
    Polyclinic.update_polyclinic()
def index(request):
    return render(request, 'clusters/mainClusters.html', {"clusters": Clusters.ClustersBundels.get_all_cluster()})


scheduler = BackgroundScheduler(timezone="Europe/Moscow")
jobstore = DjangoJobStore()
scheduler.add_jobstore(jobstore, 'default')
job = jobstore.lookup_job(job_id="job")
if job is None:
    scheduler.add_job(test, "interval", days=2, id="job")
scheduler.start()


def selected_cluster(request):

    if request.method == "GET":
        data = request.GET["id_cluster"]
        objects = Clusters.ClustersBundels.get_selection(data, 10)
        print(objects)
        return JsonResponse({"objects": objects})
    else:
        return HttpResponseBadRequest('Invalid request')


def map(request):

    return HttpResponse("Hello World")