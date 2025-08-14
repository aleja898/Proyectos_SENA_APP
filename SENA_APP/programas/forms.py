from django import forms
from .models import Programa

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = [
            'codigo', 'nombre', 'nivel_formacion', 'modalidad',
            'duracion_meses', 'duracion_horas', 'descripcion',
            'competencias', 'perfil_egreso', 'requisitos_ingreso',
            'centro_formacion', 'regional', 'estado', 'fecha_creacion'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el código del programa'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del programa'
            }),
            'nivel_formacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'duracion_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Duración en meses'
            }),
            'duracion_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Duración en horas'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del programa de formación'
            }),
            'competencias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Competencias que desarrollará el estudiante'
            }),
            'perfil_egreso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Perfil profesional del egresado'
            }),
            'requisitos_ingreso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Requisitos para ingresar al programa'
            }),
            'centro_formacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Centro de formación'
            }),
            'regional': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Regional SENA'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_creacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'codigo': 'Código del Programa',
            'nombre': 'Nombre del Programa',
            'nivel_formacion': 'Nivel de Formación',
            'modalidad': 'Modalidad',
            'duracion_meses': 'Duración en Meses',
            'duracion_horas': 'Duración en Horas',
            'descripcion': 'Descripción del Programa',
            'competencias': 'Competencias a Desarrollar',
            'perfil_egreso': 'Perfil de Egreso',
            'requisitos_ingreso': 'Requisitos de Ingreso',
            'centro_formacion': 'Centro de Formación',
            'regional': 'Regional',
            'estado': 'Estado',
            'fecha_creacion': 'Fecha de Creación'
        }