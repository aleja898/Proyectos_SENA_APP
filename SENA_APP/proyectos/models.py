from django.db import models

class Proyecto(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título del Proyecto")
    descripcion_detallada = models.TextField(verbose_name="Descripción detallada")
    area_proponente = models.CharField(max_length=255, verbose_name="Área proponente")
    responsable = models.CharField(max_length=255, verbose_name="Responsable del proyecto")
    objetivos_generales = models.TextField(verbose_name="Objetivos generales")
    objetivos_especificos = models.TextField(verbose_name="Objetivos específicos")
    alcance_limitaciones = models.TextField(verbose_name="Alcance y limitaciones")
    presupuesto_estimado = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="Presupuesto estimado")
    cronograma_tentativo = models.TextField(verbose_name="Cronograma tentativo")
    recursos_necesarios = models.TextField(verbose_name="Recursos necesarios")
    beneficiarios_esperados = models.TextField(verbose_name="Beneficiarios esperados")
    indicadores_exito = models.TextField(verbose_name="Indicadores de éxito")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
