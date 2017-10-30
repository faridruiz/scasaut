from django.shortcuts import render, redirect
from .models import Usuario
from .models import Maestro
from .models import LoginForm
from django import forms

def render_login(request):
    return render(request, 'SCASA-UT/index.html')

def menudefault(request):
	return render(request, 'SCASA-UT/docs/MenuDefault.html')

def aula_c(request):
	return render(request, 'SCASA-UT/docs/crud/aulas/create.html')

def aula_u(request):
	return render(request, 'SCASA-UT/docs/crud/aulas/update.html')

def cicloescolar(request):
	return render(request, 'SCASA-UT/docs/crud/cicloescolar/update.html')

def grupos_c(request):
	return render(request, 'SCASA-UT/docs/crud/grupos/create.html')

def grupos_u(request):
	return render(request, 'SCASA-UT/docs/crud/grupos/update.html')

def horarios(request):
	return render(request, 'SCASA-UT/docs/crud/horarios/schedule.html')

def usuarios_u(request):
	user = Usuario.objects.all()
	context = {'usuario':user}
	return render(request, 'SCASA-UT/docs/crud/usuarios/update.html', context)

def usuarios_c(request):	
	maestro = Maestro.objects.all()
	contextm = { 'maestros':maestro}
	return render(request, 'SCASA-UT/docs/crud/usuarios/create.html', contextm)

def login(request):
	NombreUsuario = request.POST['usuario']
	Contrasena = request.POST['contrasena']
	Usuario.objects
	ret = Usuario.objects.filter(usuario=NombreUsuario, contrasena=Contrasena).count()
	if ret == 1:
		return redirect('/MenuDefault')
	else:
		return redirect('/')

def alta_usuario(request):	
	user = Usuario.objects.all()
	context = {'usuario':user}
	NombreUsuario = request.POST['usuario']
	Contrasena = request.POST['contrasena']
	maes = Maestro.objects.get(id=request.POST['maestro'])
	usuariosnuevo = Usuario(usuario = NombreUsuario, contrasena= Contrasena, idmaestro = maes)
	usuariosnuevo.save()
	return render(request, 'SCASA-UT/docs/crud/usuarios/update.html', context)