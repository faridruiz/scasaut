from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Maestro, Aula, Hora
from django import forms
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login

def start(request):
	return redirect('/login')

def login_inicio(request):
    return render(request, 'SCASA-UT/index.html')

def logout_fin(request):
	logout(request)
	return redirect('/')

def ciclo_escolar(request):
	return render(request, 'SCASA-UT/docs/crud/cicloescolar/update.html')

def login_verificar(request):
	NombreUsuario = request.POST['usuario']
	Contrasena = request.POST['contrasena']
	user = authenticate(username=NombreUsuario, password=Contrasena)
	if user is not None:
		login(request, user)
		return redirect('/dashboard')
	else:
		return redirect('/')

def dashboard(request):
	if request.user.is_authenticated:
		return render(request, 'SCASA-UT/docs/MenuDefault.html')
	else:
		return redirect('/')

def usuarios_nuevo(request):
	return render(request, 'SCASA-UT/docs/crud/usuarios/create.html', {'maestros': Maestro.objects.all()})

def usuarios_nuevo_crear(request):
	user = User.objects.create_user(request.POST['usuario'], '' ,request.POST['contrasena'])
	maestro = Maestro(nombre = request.POST['maestro'], user = user)
	maestro.save()
	return redirect('/usuarios')

def usuarios(request):
	if request.user.is_authenticated:
		user = User.objects.all()
		context = {'usuario':user}
		return render(request, 'SCASA-UT/docs/crud/usuarios/update.html', context)
	else:
		return redirect('/')

def usuarios_edicion(request, id):
	if request.user.is_authenticated:
		user = User.objects.get(id=id)
		maestro = Maestro.objects.get(user = user)
		return render(request, 'SCASA-UT/docs/crud/usuarios/editform.html', {'usuario':user, 'maestro':maestro} )
	else:
		return redirec('/')

def usuarios_edicion_modificar(request, id):
	if request.user.is_authenticated:
		maestro = Maestro.objects.get(user = id)
		maestro.user.username = request.POST['usuario']
		maestro.user.set_password(request.POST['contrasena'])
		maestro.nombre = request.POST['maestro']
		maestro.user.save()
		maestro.save()
		return redirect('/usuarios')
	else:
		return redirect('/')

def usuarios_edicion_eliminar(request, id):
	if request.user.is_authenticated:
		usuario = User.objects.get(id=id)
		usuario.delete()
		return redirect('/usuarios')
	else:
		return redirect('/')

def aulas_nuevo(request):
	if request.user.is_authenticated:
		return render(request, 'SCASA-UT/docs/crud/aulas/create.html')
	else:
		return redirect('/')

def aulas_nuevo_crear(request):
	if request.user.is_authenticated:
		aula = Aula(
			nombre=request.POST['username'],
			descripcion=request.POST['email'],
			)
		aula.save()
		return redirect('/aulas')
	else:
		return redirect('/')

def aulas(request):
	if request.user.is_authenticated:
		return render(request, 'SCASA-UT/docs/crud/aulas/update.html', {'aulas': Aula.objects.all()})
	else:
		return redirect('/')

def aulas_edicion(request, id):
	if request.user.is_authenticated:
		aula = Aula.objects.get(id=id)
		return render(request, 'SCASA-UT/docs/crud/aulas/editform.html', {'aula': aula})
	else:
		return redirect('/')

def aulas_edicion_modificar(request, id):
	if request.user.is_authenticated:
		aula = Aula.objects.get(id=id)
		aula.nombre = request.POST['username']
		aula.descripcion = request.POST['email']
		aula.save()
		return redirect('/aulas')
	else:
		return redirect('/')

def aulas_edicion_eliminar(request, id):
	if request.user.is_authenticated:
		aula = Aula.objects.get(id=id)
		aula.delete()
		return redirect('/aulas')
	else:
		return redirec('/')

# def grupos_nuevo(request):
# 	return render(request, 'SCASA-UT/docs/crud/grupos/create.html')

# def grupos_nuevo_crear(request):
# 	grupo = Grupo(
# 		nombre=request.POST['username'],
# 		descripcion=request.POST['email'],
# 	)
# 	grupo.save()
# 	return redirect('/grupos')

# def grupos(request):
# 	return render(request, 'SCASA-UT/docs/crud/grupos/update.html', {'grupos': Grupo.objects.all()})

# def grupos_edicion(request, id):
# 	grupo = Grupo.objects.get(id=id)
# 	return render(request, 'SCASA-UT/docs/crud/grupos/editform.html', {'grupo': grupo})

# def grupos_edicion_modificar(request, id):
# 	grupo = Grupo.objects.get(id=id)
# 	grupo.nombre = request.POST['username']
# 	grupo.descripcion = request.POST['email']
# 	grupo.save()
# 	return redirect('/grupos')

# def grupos_edicion_eliminar(request, id):
# 	grupo = Grupo.objects.get(id=id)
# 	grupo.delete()
# 	return redirect('/grupos')

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
	return render(request, 'SCASA-UT/docs/crud/horarios/scheduler.html', {'horas': numeroHoras, 'dias': DiaSemana, 'aulas': aulas,'maestros':maestros})

class Horarios(CreateView):
	model = Hora
	fields = ['hora','idmaestro','idaula']
	template_name = 'SCASA-UT/docs/crud/horarios/scheduler.html'

	def get_context_data(self, **kwargs):
		try:
			aulas = Aula.objects.all()
			maestros = Maestro.objects.all()
		except Exception as e:
			raise
		else:
			pass
		finally:
			pass
		DiaSemana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
		numeroHoras = []
		for i in range(8,9):
			numeroHoras.append(i)
		context = {'aulas':aulas, 'horas':numeroHoras, 'dias':DiaSemana, 'maestros':maestros}
		return  context
