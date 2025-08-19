# project_management/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Proyecto, Comentario, Documento, Usuario

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            'titulo', 'descripcion', 'area_proponente', 'responsable',
            'objetivos_generales', 'objetivos_especificos', 'alcance',
            'limitaciones', 'presupuesto_estimado', 'cronograma_tentativo',
            'recursos_necesarios', 'beneficiarios_esperados', 'indicadores_exito',
            'fecha_inicio_estimada', 'fecha_finalizacion_estimada'
        ]
        
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del proyecto'
            }),
            'area_proponente': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'objetivos_generales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Objetivos generales del proyecto'
            }),
            'objetivos_especificos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Objetivos específicos del proyecto'
            }),
            'alcance': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alcance del proyecto'
            }),
            'limitaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Limitaciones del proyecto (opcional)'
            }),
            'presupuesto_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'cronograma_tentativo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Cronograma tentativo del proyecto'
            }),
            'recursos_necesarios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Recursos necesarios para el proyecto'
            }),
            'beneficiarios_esperados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Beneficiarios esperados del proyecto'
            }),
            'indicadores_exito': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Indicadores de éxito del proyecto'
            }),
            'fecha_inicio_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_finalizacion_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar responsables activos
        self.fields['responsable'].queryset = Usuario.objects.filter(activo=True)
        
        # Hacer campos obligatorios
        required_fields = [
            'titulo', 'descripcion', 'area_proponente', 'responsable',
            'objetivos_generales', 'objetivos_especificos', 'alcance',
            'presupuesto_estimado', 'recursos_necesarios',
            'beneficiarios_esperados', 'indicadores_exito'
        ]
        
        for field in required_fields:
            self.fields[field].required = True
    
    def clean_presupuesto_estimado(self):
        presupuesto = self.cleaned_data.get('presupuesto_estimado')
        if presupuesto and presupuesto <= 0:
            raise forms.ValidationError("El presupuesto debe ser mayor a 0")
        return presupuesto
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio_estimada')
        fecha_fin = cleaned_data.get('fecha_finalizacion_estimada')
        
        if fecha_inicio and fecha_fin and fecha_inicio >= fecha_fin:
            raise forms.ValidationError(
                "La fecha de finalización debe ser posterior a la fecha de inicio"
            )
        
        return cleaned_data

class ActualizarProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            'descripcion', 'objetivos_generales', 'objetivos_especificos',
            'alcance', 'limitaciones', 'presupuesto_estimado',
            'cronograma_tentativo', 'recursos_necesarios',
            'beneficiarios_esperados', 'indicadores_exito',
            'estado', 'porcentaje_completitud',
            'fecha_inicio_estimada', 'fecha_finalizacion_estimada'
        ]
        
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objetivos_generales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objetivos_especificos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alcance': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'limitaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'presupuesto_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'cronograma_tentativo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recursos_necesarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'beneficiarios_esperados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'indicadores_exito': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'porcentaje_completitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100'
            }),
            'fecha_inicio_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_finalizacion_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'tipo', 'calificacion']
        
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escriba su comentario aquí...'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'placeholder': 'Calificación del 1 al 5'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['texto'].required = True
        self.fields['calificacion'].required = False
    
    def clean_calificacion(self):
        calificacion = self.cleaned_data.get('calificacion')
        tipo = self.cleaned_data.get('tipo')
        
        if tipo == 'evaluacion' and not calificacion:
            raise forms.ValidationError("La calificación es obligatoria para evaluaciones")
        
        if calificacion and (calificacion < 1 or calificacion > 5):
            raise forms.ValidationError("La calificación debe estar entre 1 y 5")
        
        return calificacion

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre_archivo', 'archivo', 'tipo', 'descripcion', 'version']
        
        widgets = {
            'nombre_archivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del documento'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del documento (opcional)'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1.0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_archivo'].required = True
        self.fields['archivo'].required = True
        self.fields['version'].required = True
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar tamaño (máximo 50MB)
            if archivo.size > 50 * 1024 * 1024:
                raise forms.ValidationError("El archivo no puede exceder 50MB")
        return archivo

class ProyectoFiltroForm(forms.Form):
    ESTADO_CHOICES = [('', 'Todos los estados')] + Proyecto.ESTADOS_CHOICES
    AREA_CHOICES = [('', 'Todas las áreas')] + Usuario.AREAS_CHOICES
    
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar proyectos...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    area = forms.ChoiceField(
        choices=AREA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    responsable = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(activo=True),
        required=False,
        empty_label="Todos los responsables",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )