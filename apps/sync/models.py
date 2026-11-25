# backend/apps/sync/models.py
from django.db import models
from django.conf import settings

class Cerda(models.Model):
    ESTADOS = (
        ('vacia', 'Vacía'),
        ('gestante', 'Gestante'),
        ('lactando', 'Lactando'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cerdas'
    )
    id_local = models.CharField(max_length=100, help_text="ID en el dispositivo")
    arete = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    caracteristicas = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='vacia')
    corral_id = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    sincronizado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['usuario', 'id_local']
    
    def __str__(self):
        return f"{self.nombre} ({self.arete})"

class GrupoEngorda(models.Model):
    ORIGENES = (
        ('produccionPropia', 'Producción Propia'),
        ('compraExterna', 'Compra Externa'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grupos_engorda'
    )
    id_local = models.CharField(max_length=100, help_text="ID en el dispositivo")
    origen = models.CharField(max_length=20, choices=ORIGENES)
    cerda_id = models.CharField(max_length=100, blank=True, null=True)
    ciclo_id = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField()
    raza = models.CharField(max_length=100)
    peso_promedio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corral_id = models.CharField(max_length=100)
    etapa_alimento = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=200, blank=True, null=True)
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField()
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    sincronizado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['usuario', 'id_local']
    
    def __str__(self):
        return f"Grupo {self.raza} - {self.cantidad} cerdos"

class EventoCalendario(models.Model):
    TIPOS_EVENTO = (
        ('monta', 'Monta'),
        ('repeticionCelo', 'Repetición de Celo'),
        ('alertaParto', 'Alerta de Parto'),
        ('parto', 'Parto'),
        ('destete', 'Destete'),
        ('siguienteCelo', 'Siguiente Celo'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos'
    )
    id_local = models.CharField(max_length=100, help_text="ID en el dispositivo")
    cerda_id = models.CharField(max_length=100)
    cerda_nombre = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=20, choices=TIPOS_EVENTO)
    fecha = models.DateTimeField()
    notas = models.TextField(blank=True, null=True)
    completado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    sincronizado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['usuario', 'id_local']
    
    def __str__(self):
        return f"{self.tipo_evento} - {self.cerda_nombre} ({self.fecha})"