from django.contrib import admin
from django.urls import path,include
from .views import insertar_galeria, devolver, admin_usuario,adoptar, modificar, buscar_modificar, eliminar,cerrar_sesion, login, filtro_cate,filtro_desc,buscar_nombre,filtro_categoria, index, galeria,ficha, formulario,quienes,registro

urlpatterns = [
    path('',index,name='IND'),
    path('gale/',galeria,name='GALE'),
    path('formu/',formulario,name='FORMU'),
    path('quienes_somos/',quienes,name='QUIEN'),
    path('registro/',registro,name='REG'),
    path('ficha/<id>/',ficha,name='FICHA'),
    path('filtro_categoria/',filtro_categoria,name='FILTROC'),
    path('buscar_nombre/',buscar_nombre,name='BUSCARN'),
    path('filtro_descripcion/',filtro_desc,name='FILTROD'),
    path('filtro_cate/<id>/',filtro_cate,name='FILTROCATE'),
    path('login/',login,name='LOGIN'),
    path('cerrar/',cerrar_sesion,name='CERRAR'),
    path('eliminar/<id>/',eliminar,name='ELIMINA'),
    path('buscar_modificar/<id>/',buscar_modificar,name='BUSCARM'),
    path('modificar/',modificar,name='MODI'),
    path('adoptar/<id>/',adoptar,name='ADOPTAR'),
    path('admin_usuario/',admin_usuario,name='ADMINUSUARIO'),
    path('devolver/<id>/',devolver,name='DEVOLVER'),
    path('insertar_galeria/',insertar_galeria,name='INSERTARG'),
]


#  {% url ' ' %}