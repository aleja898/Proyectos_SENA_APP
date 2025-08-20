from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Proyecto
from .forms import ProyectoForm

# Create your views here.

def lista_proyectos(request):
    lista_proyectos = Proyecto.objects.all()
    template = loader.get_template('proyectos/lista_proyectos.html')
    context = {
        'lista_proyectos': lista_proyectos,
        'total_proyectos': lista_proyectos.count(),
    }
    return HttpResponse(template.render(context, request))

def detalle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    template = loader.get_template('proyectos/detalle_proyecto.html')
    context = {
        'proyecto': proyecto,
    }
    return HttpResponse(template.render(context, request))

def AgregarProyectoView(request):
        if request.method == 'POST':
            form = ProyectoForm(request.POST)
            if form.is_valid():
                proyecto = form.save()
                return redirect('proyectos:lista_proyectos')
        else:
            form = ProyectoForm()

        template = loader.get_template('proyectos/agregar_proyecto.html')
        context = {
            'form': form,
        }
        
        return HttpResponse(template.render(context, request))