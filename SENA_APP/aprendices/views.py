from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Aprendiz, Curso
from django.shortcuts import get_object_or_404
from instructores.models import Instructor
from programas.models import Programa

from aprendices.forms import AprendizForm
from django.views import generic

# Create your views here.

def aprendices(request):
    lista_aprendices = Aprendiz.objects.all().order_by('apellido', 'nombre')
    template = loader.get_template('lista_aprendices.html')
    
    context = {
        'lista_aprendices': lista_aprendices,
        'total_aprendices': lista_aprendices.count(),
    }
    return HttpResponse(template.render(context, request))

def inicio(request):
    # Estadísticas generales
    total_aprendices = Aprendiz.objects.count()
    total_instructores = Instructor.objects.count() 
    total_programas = Programa.objects.count()
    total_cursos = Curso.objects.count()
    cursos_activos = Curso.objects.filter(estado__in=['INI', 'EJE']).count()
    template = loader.get_template('inicio.html')
    
    context = {
        'total_aprendices': total_aprendices,
        'total_cursos': total_cursos,
        'cursos_activos': cursos_activos,
        'total_instructores': total_instructores,
        'total_programas': total_programas,
    }
    
    return HttpResponse(template.render(context, request))


def lista_cursos(request):
    cursos = Curso.objects.all().order_by('-fecha_inicio')
    template = loader.get_template('lista_cursos.html')
    
    context = {
        'lista_cursos': cursos,
        'total_cursos': cursos.count(),
        'titulo': 'Lista de Cursos'
    }
    
    return HttpResponse(template.render(context, request))

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    aprendices_curso = curso.aprendizcurso_set.all()
    instructores_curso = curso.instructorcurso_set.all()
    template = loader.get_template('detalle_curso.html')
    
    context = {
        'curso': curso,
        'aprendices_curso': aprendices_curso,
        'instructores_curso': instructores_curso,
    }
    
    return HttpResponse(template.render(context, request))

def detalle_aprendiz(request, aprendiz_id):
    aprendiz = get_object_or_404(Aprendiz, id=aprendiz_id) #Datos
    template = loader.get_template('detalle_aprendiz.html') #Template
    
    context = {
        'aprendiz': aprendiz,
    }
    
    return HttpResponse(template.render(context, request))

class AprendizFormView(generic.FormView):
    template_name = "agregar_aprendiz.html"
    form_class = AprendizForm
    success_url = reverse_lazy('aprendices:lista_aprendices')  # Usar reverse_lazy para mejor práctica
    
    def post(self, request, *args, **kwargs):
        print("=== POST REQUEST RECIBIDO PARA APRENDIZ ===")
        print(f"POST data: {request.POST}")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("=== FORMULARIO DE APRENDIZ VÁLIDO ===")
        print(f"Cleaned data: {form.cleaned_data}")
        
        try:
            # El método save() ya está definido en tu AprendizForm
            form.save()
            print("=== APRENDIZ GUARDADO EXITOSAMENTE ===")
            
            # Verificar que se guardó
            ultimo_aprendiz = Aprendiz.objects.last()
            print(f"Último aprendiz guardado: {ultimo_aprendiz.nombre} {ultimo_aprendiz.apellido}")
            
            messages.success(self.request, 'Aprendiz agregado exitosamente.')
            return super().form_valid(form)
        except Exception as e:
            print(f"=== ERROR AL GUARDAR APRENDIZ ===")
            print(f"Error: {str(e)}")
            
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")
            
            messages.error(self.request, f'Error al guardar el aprendiz: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        print("=== FORMULARIO DE APRENDIZ INVÁLIDO ===")
        print(f"Errores del formulario: {form.errors}")
        print(f"Errores no de campo: {form.non_field_errors()}")
        
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)