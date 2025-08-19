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

class AgregarProyectoView(FormView):
    template_name = 'proyectos/agregar_proyecto.html'
    form_class = ProyectoForm
    success_url = reverse_lazy('proyectos:lista_proyectos')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Proyecto agregado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)