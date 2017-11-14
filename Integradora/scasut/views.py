from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from .models import Maestro
from .models import LoginForm
from .models import Aula
from .models import Grupo
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
	maestro = Maestro(nombre = request.POST['maestro'])
	maestro.save()
	usuariosnuevo = Usuario(
		usuario = request.POST['usuario'],
		contrasena= request.POST['contrasena'],
		idmaestro = maestro
	)
	usuariosnuevo.save()
	return redirect('/usuarios')

def usuarios(request):
	user = Usuario.objects.all()
	context = {'usuario':user}
	return render(request, 'SCASA-UT/docs/crud/usuarios/update.html', context)

def usuarios_edicion(request, id):
	usuario = Usuario.objects.get(id=id)
	return render(request, 'SCASA-UT/docs/crud/usuarios/editform.html', {'usuario':usuario})

def usuarios_edicion_modificar(request, id):
	usuario = Usuario.objects.get(id=id)
	usuario.usuario = request.POST['usuario']
	usuario.contrasena = request.POST['contrasena']
	usuario.idmaestro.nombre = request.POST['maestro']
	usuario.idmaestro.save()
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

def grupos_nuevo(request):
	return render(request, 'SCASA-UT/docs/crud/grupos/create.html')

def grupos_nuevo_crear(request):
	grupo = Grupo(
		nombre=request.POST['username'],
		descripcion=request.POST['email'],
	)
	grupo.save()
	return redirect('/grupos')

def grupos(request):
	return render(request, 'SCASA-UT/docs/crud/grupos/update.html', {'grupos': Grupo.objects.all()})

def grupos_edicion(request, id):
	grupo = Grupo.objects.get(id=id)
	return render(request, 'SCASA-UT/docs/crud/grupos/editform.html', {'grupo': grupo})

def grupos_edicion_modificar(request, id):
	grupo = Grupo.objects.get(id=id)
	grupo.nombre = request.POST['username']
	grupo.descripcion = request.POST['email']
	grupo.save()
	return redirect('/grupos')

def grupos_edicion_eliminar(request, id):
	grupo = Grupo.objects.get(id=id)
	grupo.delete()
	return redirect('/grupos')

def verificarPin(request, pin):
	try:
		usuario = Usuario.objects.get(contrasena=pin)
		if usuario is None:
			return HttpResponse('false');
		else:
			return HttpResponse('true');
	except:
		return HttpResponse('false');

def registroHuella(request, pin):
	try:
		usuarios = Usuario.objects.get(contrasena = pin)
		if usuarios is None:
			return HttpResponse('No existe')
		else:
			return HttpResponse(usuarios.id)
	except:
		return HttpResponse('No existe')

def scheduler(request):
	try:
		aulas = Aula.objects.all()
		maestros = Maestro.objects.all()
		grupos = Grupo.objects.all()
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass
	DiaSemana = ['Lunes',
    'Martes',
    'Miercoles',
    'Jueves',
    'Viernes',
    'Sabado',
    'Domingo']

	numeroHoras = []
	for i in range(8,19):
		numeroHoras.append(i)
	return render(request, 'SCASA-UT/docs/crud/horarios/scheduler.html', {'horas': numeroHoras, 'dias': DiaSemana, 'aulas': aulas, 'grupos':grupos,'maestros':maestros})