# project_management/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Usuario(models.Model):
    ROLES_CHOICES = [
        ('admin', 'Administrador'),
        ('coordinador', 'Coordinador de área'),
        ('colaborador', 'Colaborador'),
        ('consultor', 'Consultor'),
    ]
    
    AREAS_CHOICES = [
        ('sennova', 'SENNOVA'),
        ('centro_formacion', 'Centro de Formación'),
        ('direccion_regional', 'Dirección Regional'),
        ('direccion_general', 'Dirección General'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='colaborador')
    area = models.CharField(max_length=30, choices=AREAS_CHOICES)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_area_display()}"
    
    class Meta:
        verbose_name = 'Usuario del Sistema'
        verbose_name_plural = 'Usuarios del Sistema'

class Proyecto(models.Model):
    ESTADOS_CHOICES = [
        ('propuesto', 'Propuesto'),
        ('en_revision', 'En revisión'),
        ('aprobado', 'Aprobado'),
        ('en_ejecucion', 'En ejecución'),
        ('terminado', 'Terminado'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    area_proponente = models.CharField(max_length=30, choices=Usuario.AREAS_CHOICES)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos_responsable')
    colaboradores = models.ManyToManyField(Usuario, related_name='proyectos_colaborador', blank=True)
    
    # Información del proyecto
    objetivos_generales = models.TextField()
    objetivos_especificos = models.TextField()
    alcance = models.TextField()
    limitaciones = models.TextField(blank=True)
    presupuesto_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    cronograma_tentativo = models.TextField()
    recursos_necesarios = models.TextField()
    beneficiarios_esperados = models.TextField()
    indicadores_exito = models.TextField()
    
    # Control del proyecto
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='propuesto')
    porcentaje_completitud = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio_estimada = models.DateField(null=True, blank=True)
    fecha_finalizacion_estimada = models.DateField(null=True, blank=True)
    fecha_finalizacion_real = models.DateField(null=True, blank=True)
    
    # Metadatos
    activo = models.BooleanField(default=True)
    version = models.IntegerField(default=1)
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('project_management:proyecto_detalle', kwargs={'pk': self.pk})
    
    def get_dias_restantes(self):
        if self.fecha_finalizacion_estimada:
            dias = (self.fecha_finalizacion_estimada - timezone.now().date()).days
            return max(0, dias)
        return None
    
    def is_atrasado(self):
        if self.fecha_finalizacion_estimada and self.estado in ['aprobado', 'en_ejecucion']:
            return timezone.now().date() > self.fecha_finalizacion_estimada
        return False
    
    def get_total_comentarios(self):
        return self.comentarios.filter(activo=True).count()
    
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-fecha_creacion']

class Comentario(models.Model):
    TIPOS_CHOICES = [
        ('comentario', 'Comentario'),
        ('sugerencia', 'Sugerencia'),
        ('evaluacion', 'Evaluación'),
        ('aprobacion', 'Aprobación'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios_autor')
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES, default='comentario')
    calificacion = models.IntegerField(null=True, blank=True)  # 1-5 para evaluaciones
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    # Para threading de comentarios
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')
    
    def __str__(self):
        return f"{self.autor} - {self.proyecto.titulo} ({self.fecha_creacion.strftime('%Y-%m-%d')})"
    
    def can_edit(self, usuario):
        # Puede editar dentro de 30 minutos de creación
        tiempo_limite = timezone.now() - timezone.timedelta(minutes=30)
        return self.autor == usuario and self.fecha_creacion > tiempo_limite
    
    def get_respuestas(self):
        return self.respuestas.filter(activo=True).order_by('fecha_creacion')
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-fecha_creacion']

class Documento(models.Model):
    TIPOS_CHOICES = [
        ('propuesta', 'Propuesta Técnica'),
        ('presupuesto', 'Presupuesto'),
        ('cronograma', 'Cronograma'),
        ('informe', 'Informe de Avance'),
        ('entregable', 'Entregable'),
        ('otro', 'Otro'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='documentos')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='documentos_autor')
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='proyectos/documentos/%Y/%m/')
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES, default='otro')
    descripcion = models.TextField(blank=True)
    version = models.CharField(max_length=10, default='1.0')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre_archivo} - {self.proyecto.titulo}"
    
    def get_size_mb(self):
        if self.archivo:
            return round(self.archivo.size / (1024 * 1024), 2)
        return 0
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_subida']

class HistorialProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado_anterior = models.CharField(max_length=20, blank=True)
    estado_nuevo = models.CharField(max_length=20, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.proyecto.titulo} - {self.accion} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = 'Historial de Proyecto'
        verbose_name_plural = 'Historiales de Proyectos'
        ordering = ['-fecha']
