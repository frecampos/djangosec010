import re
from django.core.checks import messages
from django.db import reset_queries
from django.shortcuts import render
from .models import Categoria, Mascota, Galeria

# importar el modelo de tabla de usuario desde el administrador
from django.contrib.auth.models import User
# importar libreria de autentificacion
from django.contrib.auth import authenticate, logout, login as login_aut
# importar libreria decoradora que evita el ingreso a las paginas sin autorizacion
from django.contrib.auth.decorators import login_required,permission_required

import requests

# Create your views here.
def cerrar_sesion(request):
    logout(request)
    categorias = Categoria.objects.all()
    contexto = {"categorias":categorias}
    return render(request, "index.html", contexto)

def login(request):
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtUsuario")
        contra = request.POST.get("txtPass")
        us = authenticate(request,username=nombre,password=contra)
        if us is not None and us.is_active:
            login_aut(request,us)
            categorias = Categoria.objects.all()
            contexto = {"categorias":categorias}
            return render(request, "index.html", contexto)
        else:
            mensaje="usuario o contraseña incorrecto"
    contexto = {"mensaje":mensaje}
    return render(request,"login.html",contexto)

def index(request):
    categorias = Categoria.objects.all()
    mascotas = Mascota.objects.filter(publicar=True).order_by('-nombre')[:3]
    contexto = {"categorias":categorias,"mascotas":mascotas}
    # -- consumo de la API ----------------------------------------
    response = requests.get("http://127.0.0.1:8149/api/mascotas/")
    todas_las_mascotas = response.json()
    contexto["mascotas_api"] = todas_las_mascotas
    # -------------------------------------------------------------
    return render(request, "index.html", contexto)

def galeria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "galeria.html",contexto)

def filtro_categoria(request):
    mascotas = Mascota.objects.all()
    cant = Mascota.objects.all().count()
    categorias = Categoria.objects.all()
    if request.POST:
        categoria = request.POST.get("cboCategoria")
        obj_cate = Categoria.objects.get(nombre=categoria)
        mascotas = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True)
        #------------ consumir api --------------------------------------------------
        #response = requests.get("http://127.0.0.1:8149/api/categoria/"+categoria+"/")
        #mascotas = response.json()
        #----------------------------------------------------------------------------
        cant = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True).count()
    contexto = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",contexto)

def filtro_cate(request, id):
    categorias = Categoria.objects.all()   
    obj_cate = Categoria.objects.get(nombre=id)
    mascotas = Mascota.objects.filter(categoria=obj_cate)
    cant = Mascota.objects.filter(categoria=obj_cate).count()
    contexto = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",contexto)

def buscar_nombre(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    if request.POST:
        nombre = request.POST.get("txtNombre")
        mascotas = Mascota.objects.filter(nombre=nombre)
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "galeria.html",contexto)

def filtro_desc(request):
    mascotas = Mascota.objects.all()
    cant = Mascota.objects.all().count()
    categorias = Categoria.objects.all()
    if request.POST:
        desc = request.POST.get("txtDesc")
        mascotas = Mascota.objects.filter(descripcion__contains=desc)
        cant =Mascota.objects.filter(descripcion__contains=desc).count()
    contexto = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",contexto)

def formulario(request):
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        email = request.POST.get("txtEmail")
        usuario = request.POST.get("txtUsuario")
        pass1 = request.POST.get("txtPass1")

        try:
            usu = User.objects.get(username=usuario)
            mensaje = "usuario ya existe"
        except:
            usu = User()
            usu.first_name = nombre
            usu.last_name = apellido
            usu.email = email
            usu.username = usuario
            usu.set_password(pass1)
            usu.save()
            mensaje="Grabo Usuario"
    contexto ={"mensaje":mensaje}
    return render(request, "formulario.html",contexto)

def quienes(request):
    return render(request, "quienes_somos.html")

def ficha(request, id):
    #mascota = Mascota.objects.get(nombre=id)
    # -- consumir API Buscar Mascota -----------------------------------
    response = requests.get("http://127.0.0.1:8149/api/mascota/"+id+"/")
    mascota = response.json()
    # -----------------------------------------------------------------.
    contexto = {"mascota":mascota}
    galeria = Galeria.objects.filter(mascota=mascota)
    contexto["galeria"] = galeria
    return render(request, "ficha.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.add_mascota',login_url='/login/')
@permission_required('misPerris.delete_mascota',login_url='/login/')
def registro(request):
    mensaje=""
    usuario_actual = request.user.username
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        cate = request.POST.get("cboCategoria")
        imagen = request.FILES.get("txtImg")
        obj_categoria = Categoria.objects.get(nombre=cate) # select * from categoria where nombre='cate'
        
        try:
            mas = Mascota.objects.get(nombre=nombre)
            mensaje="mascota existe"
        except:
            #mas = Mascota()
            #mas.nombre = nombre
            #mas.edad = edad
            #mas.descripcion = desc
            #mas.categoria = obj_categoria
            #mas.usuario = usuario_actual 
            #if imagen is not None:
            #    mas.imagen = imagen
            
            #mas.save()
            # ---------- consumir API Grabar
            datos_json={
                "nombre":nombre,
                "edad":edad,
                "descripcion":desc,
                "categoria":obj_categoria,
                "usuario":usuario_actual
            }
            #if imagen is not None:
            #    datos_json["imagen"] = imagen
            response = requests.post("http://127.0.0.1:8149/api/mascotas_crear/",data=datos_json)
            # ------------------------------------------------------------
            mensaje="grabo"


    categorias = Categoria.objects.all() # select * from categoria
    
    mascotas = Mascota.objects.filter(usuario=usuario_actual)
    cant = Mascota.objects.filter(usuario=usuario_actual).count()
    contexto = {"categorias":categorias,"mensaje":mensaje,"mascotas":mascotas,"cant":cant}
    
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.delete_mascota',login_url='/login/')
def eliminar(request,id):
    try:
        mas = Mascota.objects.get(nombre=id)
        mas.delete()
        mensaje="elimino mascota"
    except:
        mensaje="no elimino mascota"

    categorias = Categoria.objects.all() # select * from categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    contexto = {"categorias":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.view_mascota',login_url='/login/')
def buscar_modificar(request,id):
    try:
        mas = Mascota.objects.get(nombre=id)
        categorias = Categoria.objects.all() # select * from categoria
        contexto = {"categorias":categorias,"mascota":mas}
        return render(request, "modificar.html",contexto)    
    except:
        mensaje="no elimino mascota"

    categorias = Categoria.objects.all() # select * from categoria
    mascotas = Mascota.objects.all()
    contexto = {"categorias":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.change_mascota',login_url='/login/')
def modificar(request):
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        cate = request.POST.get("cboCategoria")
        imagen = request.FILES.get("txtImg")
        obj_categoria = Categoria.objects.get(nombre=cate) # select * from categoria where nombre='cate'
        
        try:
            mas = Mascota.objects.get(nombre=nombre)
            mas.edad = edad
            mas.descripcion=desc
            mas.categoria=obj_categoria

            if imagen is not None:
                mas.imagen=imagen

            mas.comentario='--'
            mas.publicar=False
            mas.save()
            mensaje="modifico"
        except:
            mensaje="no modifico"

    categorias = Categoria.objects.all() # select * from categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    contexto = {"categorias":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

def adoptar(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.filter(publicar=True).get(nombre=id)
        mas.dueno = request.user.username
        mas.publicar = False
        mas.save()
        mensaje = "Adoptada"
    except:
        mensaje = "No pudo adoptar"
    
    mascota = Mascota.objects.get(nombre=id)
    contexto = {"mascota":mascota,"mensaje":mensaje}
    return render(request, "ficha.html",contexto)

def admin_usuario(request):
    mascotas = Mascota.objects.filter(dueno=request.user.username)
    contexto = {"mascotas":mascotas}
    return render(request,"admin_usuario.html",contexto)

def devolver(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.filter(publicar=False).get(nombre=id)
        mas.dueno='--'
        mas.save()
        mensaje="Mascota Devuelta"
    except:
        mensaje="No Pudo Devolver Mascota"

    mascotas = Mascota.objects.filter(dueno=request.user.username)
    contexto = {"mascotas":mascotas,"mensaje":mensaje}
    return render(request,"admin_usuario.html",contexto)
    
def insertar_galeria(request):
    mensaje=""
    if request.POST:
        nom_mascota = request.POST.get("txtMascota")
        imagen = request.FILES.get("txtImg")

        obj_mas = Mascota.objects.get(nombre=nom_mascota)
        gale = Galeria()
        gale.imagen = imagen
        gale.mascota = obj_mas
        gale.save()
        mensaje="Grabo Imagen para Mascota "+nom_mascota

    usuario_actual = request.user.username
    categorias = Categoria.objects.all() # select * from categoria  
    mascotas = Mascota.objects.filter(usuario=usuario_actual)
    cant = Mascota.objects.filter(usuario=usuario_actual).count()
    contexto = {"categorias":categorias,"mensaje":mensaje,"mascotas":mascotas,"cant":cant}  
    return render(request, "registro.html",contexto)
   





##########################################################################

class persona:
    def __init__(self,nombre,edad):
        self.nombre=nombre
        self.edad=edad
        super().__init__()