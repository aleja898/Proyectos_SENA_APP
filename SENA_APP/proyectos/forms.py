from django import forms
from .models import Proyecto

class ProyectoForm(forms.Form):
    titulo = forms.CharField(max_length=255, label="Título del Proyecto")
    descripcion_detallada = forms.CharField(label="Descripción detallada")
    area_proponente = forms.CharField(max_length=255, label="Área proponente")
    responsable = forms.CharField(max_length=255, label="Responsable del proyecto")
    objetivos_generales = forms.CharField(label="Objetivos generales")
    objetivos_especificos = forms.CharField(label="Objetivos específicos")
    alcance_limitaciones = forms.CharField(label="Alcance y limitaciones")
    presupuesto_estimado = forms.DecimalField(max_digits=10, decimal_places=2, label="Presupuesto estimado")
    cronograma_tentativo = forms.CharField(label="Cronograma tentativo")
    recursos_necesarios = forms.CharField(label="Recursos necesarios")
    beneficiarios_esperados = forms.CharField(label="Beneficiarios esperados")
    indicadores_exito = forms.CharField(label="Indicadores de éxito")
    fecha_creacion = forms.DateField( label="Fecha de Creación")

    def save(self):
        proyecto = Proyecto.objects.create(
            titulo=self.cleaned_data['titulo'],
            descripcion_detallada=self.cleaned_data['descripcion_detallada'],
            area_proponente=self.cleaned_data['area_proponente'],
            responsable=self.cleaned_data['responsable'],
            objetivos_generales=self.cleaned_data['objetivos_generales'],
            objetivos_especificos=self.cleaned_data['objetivos_especificos'],
            alcance_limitaciones=self.cleaned_data['alcance_limitaciones'],
            presupuesto_estimado=self.cleaned_data['presupuesto_estimado'],
            cronograma_tentativo=self.cleaned_data['cronograma_tentativo'],
            recursos_necesarios=self.cleaned_data['recursos_necesarios'],
            beneficiarios_esperados=self.cleaned_data['beneficiarios_esperados'],
            indicadores_exito=self.cleaned_data['indicadores_exito'],
            fecha_creacion=self.cleaned_data['fecha_creacion'],
        )
        return proyecto