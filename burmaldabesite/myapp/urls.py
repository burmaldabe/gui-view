from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table_view, name='table_view'),
    path('roulette/', views.roulette_view, name='roulette'),
]