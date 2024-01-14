from django.urls import path, include

import clusters.views as views

urlpatterns = [
    path('update', views.update, name='update'),
    path('', views.index, name='main'),
    path('select_cluster', views.selected_cluster, name='select_cluster'),
    path('map', views.map, name='map'),
]
