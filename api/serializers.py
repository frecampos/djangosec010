from django.db.models import fields
from misPerris.models import Mascota
from rest_framework import serializers

# el serializador permite definir el modelo
# a presentar de datos en la API REST
class MascotasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mascota # de que tabla vienen los datos
        #fields = ["nombre","edad","descripcion","usuario","publicar"] # que campos ver serializados
        fields = "__all__"