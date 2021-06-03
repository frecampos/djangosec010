from django.shortcuts import render
from rest_framework import generics
from misPerris.models import Categoria, Mascota
from .serializers import MascotasSerializers

# Create your views here.

class MascotasViewSet(generics.ListAPIView):
    queryset = Mascota.objects.all() # registros a mostrar
    serializer_class = MascotasSerializers # bajo que formato

class MascotasCreateViewSet(generics.ListCreateAPIView):
    queryset = Mascota.objects.all()
    serializer_class = MascotasSerializers

class MascotaBuscarViewSet(generics.ListAPIView):
    serializer_class = MascotasSerializers
    def get_queryset(self):
        nombre_mascota = self.kwargs['nombre']
        return Mascota.objects.filter(nombre=nombre_mascota)

class MascotaCategoriaViewSet(generics.ListAPIView):
    serializer_class = MascotasSerializers
    def get_queryset(self):
        categoria = self.kwargs['categoria']
        try:
            obj_cate = Categoria.objects.get(nombre=categoria)
            return Mascota.objects.filter(categoria=obj_cate).filter(publicar=True)
        except:
            return Mascota.objects.all()