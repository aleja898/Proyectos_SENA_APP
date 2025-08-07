from django.http import HttpResponse
from django.template import loader
from .models import Aprendiz
from django.shortcuts import get_object_or_404, render
from django.db.models import Q


# Create your views here.

def aprendices(request):
    # Obtener parámetro de búsqueda
    busqueda = request.GET.get('buscar', '')
    
    # Filtrar aprendices si hay búsqueda
    if busqueda:
        lista_aprendices = Aprendiz.objects.filter(
            Q(nombre__icontains=busqueda) | 
            Q(apellido__icontains=busqueda) | 
            Q(documento_identidad__icontains=busqueda) |
            Q(programa__icontains=busqueda)
        ).order_by('apellido', 'nombre')
    else:
        lista_aprendices = Aprendiz.objects.all().order_by('apellido', 'nombre')
    
    template = loader.get_template('lista_aprendices.html')
    
    context = {
        'lista_aprendices': lista_aprendices,
        'total_aprendices': lista_aprendices.count(),
        'busqueda': busqueda,
    }
    return HttpResponse(template.render(context, request))

def detalle_aprendiz(request, aprendiz_id):
    aprendiz = get_object_or_404(Aprendiz, pk=aprendiz_id)
    return render(request, 'detalle_aprendiz.html', {'aprendiz': aprendiz})

def inicio(request):
    # Estadísticas generales
    total_aprendices = Aprendiz.objects.count()
    # Aprendices con programas asignados
    aprendices_con_programa = Aprendiz.objects.exclude(programa__isnull=True).exclude(programa__exact='').count()
    # Programas únicos
    programas_unicos = Aprendiz.objects.exclude(programa__isnull=True).exclude(programa__exact='').values_list('programa', flat=True).distinct().count()
    
    template = loader.get_template('inicio.html')
    
    context = {
        'total_aprendices': total_aprendices,
        'aprendices_con_programa': aprendices_con_programa,
        'programas_unicos': programas_unicos,
    }
    
    return HttpResponse(template.render(context, request))