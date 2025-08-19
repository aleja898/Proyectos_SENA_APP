# project_management/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Proyecto, Comentario, Documento, Usuario, HistorialProyecto
from .forms import (
    ProyectoForm, ActualizarProyectoForm, ComentarioForm, 
    DocumentoForm, ProyectoFiltroForm
)

@login_required
def dashboard(request):
    """Dashboard principal con métricas generales"""
    # Obtener usuario del sistema
    try:
        usuario_sistema = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no registrado en el sistema de proyectos")
        return redirect('admin:index')
    
    # Estadísticas generales
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    proyectos_activos = Proyecto.objects.filter(
        activo=True, 
        estado__in=['aprobado', 'en_ejecucion']
    ).count()
    
    proyectos_por_estado = {}
    for estado, nombre in Proyecto.ESTADOS_CHOICES:
        proyectos_por_estado[nombre] = Proyecto.objects.filter(
            activo=True, estado=estado
        ).count()
    
    # Proyectos por área
    proyectos_por_area = {}
    for area, nombre in Usuario.AREAS_CHOICES:
        proyectos_por_area[nombre] = Proyecto.objects.filter(
            activo=True, area_proponente=area
        ).count()
    
    # Proyectos del usuario
    mis_proyectos = Proyecto.objects.filter(
        activo=True,
        responsable=usuario_sistema
    ).count()
    
    proyectos_colaboro = Proyecto.objects.filter(
        activo=True,
        colaboradores=usuario_sistema
    ).count()
    
    # Proyectos recientes
    proyectos_recientes = Proyecto.objects.filter(
        activo=True
    ).order_by('-fecha_creacion')[:5]
    
    # Proyectos con alertas (atrasados)
    proyectos_atrasados = []
    for proyecto in Proyecto.objects.filter(
        activo=True, 
        estado__in=['aprobado', 'en_ejecucion'],
        fecha_finalizacion_estimada__lt=timezone.now().date()
    ):
        proyectos_atrasados.append(proyecto)
    
    context = {
        'usuario_sistema': usuario_sistema,
        'total_proyectos': total_proyectos,
        'proyectos_activos': proyectos_activos,
        'proyectos_por_estado': proyectos_por_estado,
        'proyectos_por_area': proyectos_por_area,
        'mis_proyectos': mis_proyectos,
        'proyectos_colaboro': proyectos_colaboro,
        'proyectos_recientes': proyectos_recientes,
        'proyectos_atrasados': proyectos_atrasados[:5],
    }
    
    return render(request, 'project_management/dashboard.html', context)

@login_required
def lista_proyectos(request):
    """Lista de proyectos con filtros y búsqueda"""
    form = ProyectoFiltroForm(request.GET)
    proyectos = Proyecto.objects.filter(activo=True)
    
    if form.is_valid():
        # Filtro por búsqueda
        if form.cleaned_data['buscar']:
            buscar = form.cleaned_data['buscar']
            proyectos = proyectos.filter(
                Q(titulo__icontains=buscar) |
                Q(descripcion__icontains=buscar) |
                Q(objetivos_generales__icontains=buscar)
            )
        
        # Filtro por estado
        if form.cleaned_data['estado']:
            proyectos = proyectos.filter(estado=form.cleaned_data['estado'])
        
        # Filtro por área
        if form.cleaned_data['area']:
            proyectos = proyectos.filter(area_proponente=form.cleaned_data['area'])
        
        # Filtro por responsable
        if form.cleaned_data['responsable']:
            proyectos = proyectos.filter(responsable=form.cleaned_data['responsable'])
        
        # Filtro por fechas
        if form.cleaned_data['fecha_desde']:
            proyectos = proyectos.filter(fecha_creacion__gte=form.cleaned_data['fecha_desde'])
        
        if form.cleaned_data['fecha_hasta']:
            proyectos = proyectos.filter(fecha_creacion__lte=form.cleaned_data['fecha_hasta'])
    
    # Ordenar por fecha de creación
    proyectos = proyectos.order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(proyectos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'proyectos': page_obj,
    }
    
    return render(request, 'project_management/lista_proyectos.html', context)

@login_required
def detalle_proyecto(request, pk):
    """Detalle completo del proyecto"""
    proyecto = get_object_or_404(Proyecto, pk=pk, activo=True)
    
    # Verificar permisos de visualización
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    # Comentarios del proyecto
    comentarios = proyecto.comentarios.filter(
        activo=True, 
        comentario_padre__isnull=True
    ).order_by('-fecha_creacion')
    
    # Documentos del proyecto
    documentos = proyecto.documentos.filter(activo=True).order_by('-fecha_subida')
    
    # Historial del proyecto
    historial = proyecto.historial.all()[:10]
    
    # Formulario para comentarios
    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.proyecto = proyecto
            comentario.autor = usuario_sistema
            comentario.save()
            
            # Registrar en historial
            HistorialProyecto.objects.create(
                proyecto=proyecto,
                usuario=usuario_sistema,
                accion='Comentario agregado',
                descripcion=f'Nuevo comentario: {comentario.tipo}'
            )
            
            messages.success(request, 'Comentario agregado exitosamente')
            return redirect('project_management:proyecto_detalle', pk=proyecto.pk)
    else:
        comentario_form = ComentarioForm()
    
    context = {
        'proyecto': proyecto,
        'comentarios': comentarios,
        'documentos': documentos,
        'historial': historial,
        'comentario_form': comentario_form,
        'usuario_sistema': usuario_sistema,
    }
    
    return render(request, 'project_management/detalle_proyecto.html', context)

@login_required
def crear_proyecto(request):
    """Crear nuevo proyecto"""
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.save()
            
            # Registrar en historial
            HistorialProyecto.objects.create(
                proyecto=proyecto,
                usuario=usuario_sistema,
                accion='Proyecto creado',
                descripcion=f'Proyecto "{proyecto.titulo}" creado en estado propuesto'
            )
            
            messages.success(request, 'Proyecto creado exitosamente')
            return redirect('project_management:proyecto_detalle', pk=proyecto.pk)
    else:
        form = ProyectoForm()
    
    context = {
        'form': form,
        'titulo_pagina': 'Crear Nuevo Proyecto'
    }
    
    return render(request, 'project_management/crear_proyecto.html', context)

@login_required
def editar_proyecto(request, pk):
    """Editar proyecto existente"""
    proyecto = get_object_or_404(Proyecto, pk=pk, activo=True)
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    # Verificar permisos de edición
    if (proyecto.responsable != usuario_sistema and 
        usuario_sistema.rol not in ['admin', 'coordinador']):
        messages.error(request, 'No tiene permisos para editar este proyecto')
        return redirect('project_management:proyecto_detalle', pk=proyecto.pk)
    
    if request.method == 'POST':
        form = ActualizarProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            # Verificar cambio de estado
            estado_anterior = proyecto.estado
            proyecto_actualizado = form.save(commit=False)
            
            # Incrementar versión si hay cambios significativos
            if form.has_changed():
                proyecto_actualizado.version += 1
            
            proyecto_actualizado.save()
            
            # Registrar cambios en historial
            if 'estado' in form.changed_data:
                HistorialProyecto.objects.create(
                    proyecto=proyecto_actualizado,
                    usuario=usuario_sistema,
                    accion='Estado actualizado',
                    descripcion=f'Estado cambiado de {estado_anterior} a {proyecto_actualizado.estado}',
                    estado_anterior=estado_anterior,
                    estado_nuevo=proyecto_actualizado.estado
                )
            
            if form.changed_data:
                campos_cambiados = ', '.join(form.changed_data)
                HistorialProyecto.objects.create(
                    proyecto=proyecto_actualizado,
                    usuario=usuario_sistema,
                    accion='Proyecto actualizado',
                    descripcion=f'Campos modificados: {campos_cambiados}'
                )
            
            messages.success(request, 'Proyecto actualizado exitosamente')
            return redirect('project_management:proyecto_detalle', pk=proyecto.pk)
    else:
        form = ActualizarProyectoForm(instance=proyecto)
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'titulo_pagina': f'Editar Proyecto: {proyecto.titulo}'
    }
    
    return render(request, 'project_management/editar_proyecto.html', context)

@login_required
def eliminar_proyecto(request, pk):
    """Eliminación lógica del proyecto"""
    proyecto = get_object_or_404(Proyecto, pk=pk, activo=True)
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    # Solo admin y coordinadores pueden eliminar
    if usuario_sistema.rol not in ['admin', 'coordinador']:
        messages.error(request, 'No tiene permisos para eliminar proyectos')
        return redirect('project_management:proyecto_detalle', pk=proyecto.pk)
    
    if request.method == 'POST':
        proyecto.activo = False
        proyecto.save()
        
        # Registrar eliminación
        HistorialProyecto.objects.create(
            proyecto=proyecto,
            usuario=usuario_sistema,
            accion='Proyecto eliminado',
            descripcion=f'Proyecto "{proyecto.titulo}" eliminado lógicamente'
        )
        
        messages.success(request, 'Proyecto eliminado exitosamente')
        return redirect('project_management:lista_proyectos')
    
    context = {
        'proyecto': proyecto,
    }
    
    return render(request, 'project_management/confirmar_eliminar.html', context)

@login_required
def subir_documento(request, pk):
    """Subir documento al proyecto"""
    proyecto = get_object_or_404(Proyecto, pk=pk, activo=True)
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.proyecto = proyecto
            documento.autor = usuario_sistema
            documento.save()
            
            # Registrar en historial
            HistorialProyecto.objects.create(
                proyecto=proyecto,
                usuario=usuario_sistema,
                accion='Documento subido',
                descripcion=f'Nuevo documento: {documento.nombre_archivo}'
            )
            
            messages.success(request, 'Documento subido exitosamente')
            return redirect('project_management:proyecto_detalle', pk=proyecto.pk)
    else:
        form = DocumentoForm()
    
    context = {
        'form': form,
        'proyecto': proyecto,
    }
    
    return render(request, 'project_management/subir_documento.html', context)

@login_required
def responder_comentario(request, comentario_id):
    """Responder a un comentario"""
    comentario_padre = get_object_or_404(Comentario, pk=comentario_id, activo=True)
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.proyecto = comentario_padre.proyecto
            respuesta.autor = usuario_sistema
            respuesta.comentario_padre = comentario_padre
            respuesta.save()
            
            messages.success(request, 'Respuesta agregada exitosamente')
            return redirect('project_management:proyecto_detalle', 
                          pk=comentario_padre.proyecto.pk)
    
    return redirect('project_management:proyecto_detalle', 
                  pk=comentario_padre.proyecto.pk)

@login_required
def reportes(request):
    """Panel de reportes y estadísticas"""
    # Métricas ejecutivas
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    presupuesto_total = Proyecto.objects.filter(activo=True).aggregate(
        total=models.Sum('presupuesto_estimado')
    )['total'] or 0
    
    # Proyectos por estado
    proyectos_por_estado = []
    for estado, nombre in Proyecto.ESTADOS_CHOICES:
        count = Proyecto.objects.filter(activo=True, estado=estado).count()
        if count > 0:
            proyectos_por_estado.append({
                'estado': nombre,
                'cantidad': count,
                'porcentaje': round((count / total_proyectos) * 100, 1) if total_proyectos > 0 else 0
            })
    
    # Proyectos por área
    proyectos_por_area = []
    for area, nombre in Usuario.AREAS_CHOICES:
        count = Proyecto.objects.filter(activo=True, area_proponente=area).count()
        presupuesto = Proyecto.objects.filter(
            activo=True, area_proponente=area
        ).aggregate(total=models.Sum('presupuesto_estimado'))['total'] or 0
        
        if count > 0:
            proyectos_por_area.append({
                'area': nombre,
                'cantidad': count,
                'presupuesto': presupuesto,
                'porcentaje': round((count / total_proyectos) * 100, 1) if total_proyectos > 0 else 0
            })
    
    # Usuarios más activos
    usuarios_activos = Usuario.objects.annotate(
        proyectos_responsable=Count('proyectos_responsable', filter=Q(proyectos_responsable__activo=True)),
        comentarios_count=Count('comentarios_autor', filter=Q(comentarios_autor__activo=True))
    ).filter(activo=True).order_by('-proyectos_responsable')[:10]
    
    # Proyectos recientes con más actividad
    proyectos_activos = Proyecto.objects.filter(
        activo=True
    ).annotate(
        comentarios_count=Count('comentarios', filter=Q(comentarios__activo=True))
    ).order_by('-comentarios_count', '-fecha_creacion')[:10]
    
    # Estadísticas temporales (últimos 6 meses)
    hace_6_meses = timezone.now() - timedelta(days=180)
    proyectos_recientes = Proyecto.objects.filter(
        activo=True,
        fecha_creacion__gte=hace_6_meses
    )
    
    estadisticas_mensuales = {}
    for i in range(6):
        fecha_inicio = hace_6_meses + timedelta(days=30*i)
        fecha_fin = hace_6_meses + timedelta(days=30*(i+1))
        mes_nombre = fecha_inicio.strftime('%B %Y')
        
        count = proyectos_recientes.filter(
            fecha_creacion__gte=fecha_inicio,
            fecha_creacion__lt=fecha_fin
        ).count()
        
        estadisticas_mensuales[mes_nombre] = count
    
    context = {
        'total_proyectos': total_proyectos,
        'presupuesto_total': presupuesto_total,
        'proyectos_por_estado': proyectos_por_estado,
        'proyectos_por_area': proyectos_por_area,
        'usuarios_activos': usuarios_activos,
        'proyectos_activos': proyectos_activos,
        'estadisticas_mensuales': estadisticas_mensuales,
    }
    
    return render(request, 'project_management/reportes.html', context)

@login_required
def mis_proyectos(request):
    """Proyectos del usuario actual"""
    usuario_sistema = get_object_or_404(Usuario, user=request.user)
    
    # Proyectos como responsable
    proyectos_responsable = Proyecto.objects.filter(
        activo=True,
        responsable=usuario_sistema
    ).order_by('-fecha_creacion')
    
    # Proyectos como colaborador
    proyectos_colaborador = Proyecto.objects.filter(
        activo=True,
        colaboradores=usuario_sistema
    ).order_by('-fecha_creacion')
    
    context = {
        'proyectos_responsable': proyectos_responsable,
        'proyectos_colaborador': proyectos_colaborador,
        'usuario_sistema': usuario_sistema,
    }
    
    return render(request, 'project_management/mis_proyectos.html', context)

# API Views para AJAX
@login_required
def api_proyecto_estadisticas(request, pk):
    """API para estadísticas del proyecto"""
    proyecto = get_object_or_404(Proyecto, pk=pk, activo=True)
    
    estadisticas = {
        'comentarios_total': proyecto.comentarios.filter(activo=True).count(),
        'documentos_total': proyecto.documentos.filter(activo=True).count(),
        'colaboradores_total': proyecto.colaboradores.count(),
        'dias_restantes': proyecto.get_dias_restantes(),
        'is_atrasado': proyecto.is_atrasado(),
        'porcentaje_completitud': proyecto.porcentaje_completitud,
    }
    
    return JsonResponse(estadisticas)

@login_required
def api_buscar_usuarios(request):
    """API para búsqueda de usuarios"""
    query = request.GET.get('q', '')
    usuarios = Usuario.objects.filter(
        activo=True,
        user_username_icontains=query
    )[:10]
    
    results = []
    for usuario in usuarios:
        results.append({
            'id': usuario.id,
            'text': f"{usuario.user.get_full_name() or usuario.user.username} - {usuario.get_area_display()}"
        })
    
    return JsonResponse({'results': results})