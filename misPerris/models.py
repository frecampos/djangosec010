from django.db import models
from django.db.models.fields import NullBooleanField

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(primary_key=True,max_length=25)
    anno = models.IntegerField()
    imagen = models.ImageField(upload_to='cate',null=True)

    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    nombre = models.CharField(primary_key=True,max_length=25)
    edad = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas',default='mascotas/sinimagen.jpg')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    publicar = models.BooleanField(default=False)
    comentario = models.TextField(default='--')
    usuario = models.CharField(null=True,max_length=45)
    dueno = models.CharField(max_length=45,default='--')

    def __str__(self):
        return self.nombre

class Galeria(models.Model):
    auto_inc = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='galeria')
    mascota = models.ForeignKey(Mascota,on_delete=models.CASCADE)

    def __str__(self):
        return "Numero:"+str(self.auto_inc)