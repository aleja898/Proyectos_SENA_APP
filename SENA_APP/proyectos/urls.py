# project_management/urls.py
from django.urls import path
from . import views

app_name = 'project_management'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    
    # Gestión de proyectos
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:pk>/', views.detalle_proyecto, name='proyecto_detalle'),
    path('proyectos/<int:pk>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('proyectos/<int:pk>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),
    
    # Gestión de documentos
    path('proyectos/<int:pk>/documento/', views.subir_documento, name='subir_documento'),
    
    # Gestión de comentarios
    path('comentarios/<int:comentario_id>/responder/', views.responder_comentario, name='responder_comentario'),
    
    # Reportes y estadísticas
    path('reportes/', views.reportes, name='reportes'),
    path('mis-proyectos/', views.mis_proyectos, name='mis_proyectos'),
    
    # APIs para AJAX
    path('api/proyecto/<int:pk>/estadisticas/', views.api_proyecto_estadisticas, name='api_proyecto_estadisticas'),
    path('api/buscar-usuarios/', views.api_buscar_usuarios, name='api_buscar_usuarios'),
]