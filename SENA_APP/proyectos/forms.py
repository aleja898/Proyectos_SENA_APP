from django import forms
from .models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            'titulo', 'descripcion_detallada', 'area_proponente', 'responsable',
            'objetivos_generales', 'objetivos_especificos', 'alcance_limitaciones',
            'presupuesto_estimado', 'cronograma_tentativo', 'recursos_necesarios',
            'beneficiarios_esperados', 'indicadores_exito'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_detallada': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'area_proponente': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivos_generales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objetivos_especificos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alcance_limitaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'presupuesto_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cronograma_tentativo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recursos_necesarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'beneficiarios_esperados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'indicadores_exito': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'titulo': 'Título del Proyecto',
            'descripcion_detallada': 'Descripción detallada',
            'area_proponente': 'Área proponente',
            'responsable': 'Responsable del proyecto',
            'objetivos_generales': 'Objetivos generales',
            'objetivos_especificos': 'Objetivos específicos',
            'alcance_limitaciones': 'Alcance y limitaciones',
            'presupuesto_estimado': 'Presupuesto estimado',
            'cronograma_tentativo': 'Cronograma tentativo',
            'recursos_necesarios': 'Recursos necesarios',
            'beneficiarios_esperados': 'Beneficiarios esperados',
            'indicadores_exito': 'Indicadores de éxito'
        }