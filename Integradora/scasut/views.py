from django.shortcuts import render, redirect
from .models import Usuario
from .models import Maestro
from .models import LoginForm
from .models import Aula
from django import forms


def start(request):
	return redirect('/login')

def login(request):
    return render(request, 'SCASA-UT/index.html')

def login_verificar(request):
	NombreUsuario = request.POST['usuario']
	Contrasena = request.POST['contrasena']
	ret = Usuario.objects.filter(usuario=NombreUsuario, contrasena=Contrasena).count()
	if ret == 1:
		return redirect('/dashboard')
	else:
		return redirect('/')

def dashboard(request):
	return render(request, 'SCASA-UT/docs/MenuDefault.html')

def usuarios_nuevo(request):
	return render(request, 'SCASA-UT/docs/crud/usuarios/create.html', {'maestros': Maestro.objects.all()})

def usuarios_nuevo_crear(request):
	usuariosnuevo = Usuario(
		usuario = request.POST['usuario'],
		contrasena= request.POST['contrasena'],
		idmaestro = Maestro.objects.get(id=request.POST['maestro'])
	)
	usuariosnuevo.save()
	return redirect('/usuarios')

def usuarios(request):
	user = Usuario.objects.all()
	context = {'usuario':user}
	return render(request, 'SCASA-UT/docs/crud/usuarios/update.html', context)

def usuarios_edicion(request):
	#TODO: anexar vista a formulario de edición
	pass

def usuarios_edicion_modificar(request, id):
	usuario = Usuario.objects.get(id=id)
	usuario.usuario = request.POST['usuario']
	usuario.contrasena = request['contrasena']
	usuario.idmaestro = Maestro.objects.get(id=request['maestro'])
	usuario.save()
	return redirect('/usuarios')

def usuarios_edicion_eliminar(request, id):
	usuario = Usuario.objects.get(id=id)
	usuario.delete()
	return redirect('/usuarios')

def aulas_nuevo(request):
	return render(request, 'SCASA-UT/docs/crud/aulas/create.html')

def aulas_nuevo_crear(request):
	aula = Aula(
		nombre=request.POST['username'],
		descripcion=request.POST['email'],
	)
	aula.save()
	return redirect('/aulas')

def aulas(request):
	return render(request, 'SCASA-UT/docs/crud/aulas/update.html', {'aulas': Aula.objects.all()})

def aulas_edicion(request, id):
	aula = Aula.objects.get(id=id)
	return render(request, 'SCASA-UT/docs/crud/aulas/editform.html', {'aula': aula})

def aulas_edicion_modificar(request, id):
	aula = Aula.objects.get(id=id)
	aula.nombre = request.POST['username']
	aula.descripcion = request.POST['email']
	aula.save()
	return redirect('/aulas')

def aulas_edicion_eliminar(request, id):
	aula = Aula.objects.get(id=id)
	aula.delete()
	return redirect('/aulas')
