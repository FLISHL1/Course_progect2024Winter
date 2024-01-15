from django.urls import path, include

import clusters.views as views

urlpatterns = [
    path('update', views.update, name='update'),
    path('', views.index, name='main'),
    path('select_cluster', views.selected_cluster, name='select_cluster'),
    path('update_name_cluster', views.update_name_cluster, name='update_name_cluster'),
    path('update_name_increased', views.update_name_increased, name='update_name_increased'),
    path('map', views.map, name='map'),
]
