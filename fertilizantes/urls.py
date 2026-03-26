from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # 
    path('', views.listaFertilizantes, name='fertilizantes'),
    path('saudacao/<str:nome>/', views.saudacao, name='saudacao'),
    path('informar/<int:id>/', views.informar, name='informar'),
    path('mensagem', views.mensagem, name='mensagem'),
    path('novo_fertilizante/', views.novo_fertilizante, name='novo_fertilizante'),
    path('editar_fertilizante/<int:id>/', views.editar_fertilizante, name='editar_fertilizante'),
]