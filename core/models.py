from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Videojuego(models.Model):
    tipo_videojuego = models.CharField(max_length=255)
    comentario = models.TextField()
    puntuacion = models.IntegerField(default=0, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)  # Usamos el ID del primer usuario como valor predeterminado

    def __str__(self):
        return self.tipo_videojuego
    

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero = models.CharField(max_length=15)
    correo = models.EmailField()
    genero = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)