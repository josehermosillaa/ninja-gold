from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('condiciones',views.condiciones),
    path('ninja_gold',views.ninja_gold),
    path('process_money',views.process_money),
    path('reset',views.reset),
    path('end',views.end),
    path('logout',views.logout)
]
