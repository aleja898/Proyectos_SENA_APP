from django import forms
from .models import Aprendiz


class AprendizForm(forms.Form):
    documento_identidad = forms.CharField(
        max_length=20, 
        label="Documento de Identidad",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el documento de identidad'
        })
    )
    nombre = forms.CharField(
        max_length=100, 
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre'
        })
    )
    apellido = forms.CharField(
        max_length=100, 
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido'
        })
    )
    programa = forms.CharField(
        max_length=100, 
        label="Programa",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el programa de formación'
        })
    )
    telefono = forms.CharField(
        max_length=15, 
        label="Teléfono",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número de teléfono'
        })
    )
    correo = forms.EmailField(
        label="Correo Electrónico",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el correo electrónico'
        })
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    ciudad = forms.CharField(
        max_length=100, 
        required=False, 
        label="Ciudad",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la ciudad de residencia'
        })
    )
    
    #Validaciones personalizadas 
    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get('documento_identidad')
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')

        if not documento or not nombre or not apellido:
            raise forms.ValidationError("Los campos documento, nombre y apellido son obligatorios.")

        return cleaned_data
    
    def clean_documento_identidad(self):
        documento = self.cleaned_data['documento_identidad']
        if not documento.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        
        # Verificar si ya existe
        if Aprendiz.objects.filter(documento_identidad=documento).exists():
            raise forms.ValidationError("Ya existe un aprendiz con este documento.")
        
        return documento

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono

    
    #Crear un método para guardar los datos del formulario en la base de datos
    def save(self):
        print("=== EJECUTANDO save() EN AprendizForm ===")
        print(f"Datos a guardar: {self.cleaned_data}")
        
        try:
            aprendiz = Aprendiz.objects.create(
                documento_identidad=self.cleaned_data['documento_identidad'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                programa=self.cleaned_data['programa'],
                telefono=self.cleaned_data.get('telefono'),
                correo=self.cleaned_data.get('correo'),
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                ciudad=self.cleaned_data.get('ciudad')
            )
            print(f"=== APRENDIZ CREADO CON ID: {aprendiz.id} ===")
            return aprendiz
        except Exception as e:
            print(f"=== ERROR EN save() DE AprendizForm: {e} ===")
            raise