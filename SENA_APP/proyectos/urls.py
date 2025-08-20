from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('proyecto/<int:proyecto_id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('agregar_proyecto/', views.AgregarProyectoView, name='agregar_proyecto'),
]