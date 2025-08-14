from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Programa
from .forms import ProgramaForm


# Create your views here.

def programas(request):
    lista_programas = Programa.objects.all()
    template = loader.get_template('lista_programas.html')
    context = {
    'lista_programas': lista_programas,
    'total_programas': lista_programas.count(),
    }
    return HttpResponse(template.render(context, request))

def detalle_programa(request, programa_id):
    programa = get_object_or_404(Programa, id=programa_id)
    cursos = programa.curso_set.all().order_by('-fecha_inicio')
    template = loader.get_template('detalle_programa.html')
    
    context = {
        'programa': programa,
        'cursos': cursos,
    }
    
    return HttpResponse(template.render(context, request))

class AgregarProgramaView(FormView):
    template_name = 'agregar_programa.html'
    form_class = ProgramaForm
    success_url = reverse_lazy('programas:lista_programas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Programa de Formación'
        return context
    
    def post(self, request, *args, **kwargs):
        print("=== POST REQUEST RECIBIDO ===")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        print("=== FORMULARIO VÁLIDO ===")
        print(f"Cleaned data: {form.cleaned_data}")
        
        try:
            # Intentar guardar
            programa = form.save()
            print(f"=== PROGRAMA GUARDADO EXITOSAMENTE ===")
            print(f"ID del programa: {programa.id}")
            print(f"Nombre del programa: {programa.nombre}")
            
            messages.success(self.request, 'Programa agregado exitosamente.')
            return super().form_valid(form)
        except Exception as e:
            print(f"=== ERROR AL GUARDAR ===")
            print(f"Error: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            
            # Agregar más detalles del error
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")
            
            messages.error(self.request, f'Error al guardar el programa: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        print("=== FORMULARIO INVÁLIDO ===")
        print(f"Errores del formulario: {form.errors}")
        print(f"Errores no de campo: {form.non_field_errors()}")
        
        # Mostrar qué campos tienen errores
        for field, errors in form.errors.items():
            print(f"Campo '{field}': {errors}")
        
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

# Vista basada en función como alternativa
agregar_programa = AgregarProgramaView.as_view()