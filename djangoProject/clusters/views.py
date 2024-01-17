from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from sklearn.metrics import silhouette_score

from clusters.models import Food, Polyclinic, Clusters, Cluster_name, Cluster_name_increased
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore


@login_required
def update(request):
    return HttpResponse("Okl")



def test():
    Clusters.ClustersBundels.update_items()



def index(request):
    return render(request, 'clusters/mainClusters.html', {"clusters": Clusters.ClustersBundels.get_all_cluster(request.user)})


scheduler = BackgroundScheduler(timezone="Europe/Moscow")
jobstore = DjangoJobStore()
scheduler.add_jobstore(jobstore, 'default')
job = jobstore.lookup_job(job_id="job")
if job is None:
    scheduler.add_job(test, "interval", days=2, id="job")
scheduler.start()


def selected_cluster(request):
    if request.method == "GET":
        id_cluster = request.GET["id_cluster"]
        count = int(request.GET["count"])
        objects = Clusters.ClustersBundels.get_selection(id_cluster, count, request.user)
        return JsonResponse({"objects": objects})
    else:
        return HttpResponseBadRequest('Invalid request')


def map(request):
    return render(request, 'clusters/map.html', {"clusters": Clusters.ClustersBundels.get_all_cluster(request.user)})

@login_required
def update_name_cluster(request):
    if request.method == "GET":
        cluster = request.GET["id_cluster"]
        name = request.GET["name"]
        objects = Cluster_name.Name.objects.filter(cluster=cluster, id_user=request.user).all()
        if len(objects) == 0:
            Cluster_name.Name.objects.create(id_user=request.user, name=name, cluster=cluster)
        else:
            objects[0].name = name
            objects[0].save()
        return JsonResponse(data={"name": name}, status=200)
    else:
        pass

@login_required
def update_name_increased(request):
    if request.method == "GET":
        cluster = request.GET["id_increased"].split("-")
        name = request.GET["name"]
        objects = Cluster_name_increased.NameIncreased.objects.filter(type=cluster[0], id_increased=cluster[1], id_user=request.user).all()
        if len(objects) == 0:
            Cluster_name_increased.NameIncreased.objects.create(id_user=request.user, name=name, id_increased=cluster[1], type=cluster[0])
        else:
            objects[0].name = name
            objects[0].save()
        return JsonResponse(data={"name": name}, status=200)
    else:
        pass


def get_all_points(request):
    objects = Clusters.ClustersBundels.get_all_points(request.GET["id_cluster"])
    return JsonResponse(objects, safe=False)
