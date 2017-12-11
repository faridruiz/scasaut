from django.db.models import Count
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Usuario, Maestro, Aula, Hora, RegistroEntradaAulas, Configuracion
from django import forms
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login
import time, datetime
import locale
locale.setlocale(category=locale.LC_ALL, locale="Spanish")
def start(request):
	if request.user.is_authenticated:
		return redirect('/dashboard')
	else:
		return redirect('/login')

def login_inicio(request):
	if request.user.is_authenticated:
		return redirect('/dashboard')
	else:
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
	user = User.objects.create_user(request.POST['usuario'], 'pruebas@pruebas.com' ,request.POST['contrasena'])
	maestro = Maestro(nombre = request.POST['maestro'], user = user)
	maestro.save()
	return redirect('/usuarios')


def usuarios(request):	
	if request.user.is_authenticated:
		try:
			usuariostodos = Maestro.objects.all()
			try:
				peticion_pagina = str(request.GET["page"])
			except Exception as e:				
				peticion_pagina = 1
			if int(peticion_pagina) > 1:
				user = Maestro.objects.all().annotate(Count('id')).order_by('id')[((int(peticion_pagina) * 5)-5):((int(peticion_pagina) * 5))]
			else:
				user = Maestro.objects.all().annotate(Count('id')).order_by('id')[:5]
			paginado = Paginator(usuariostodos, 5)
			contador = []
			while len(contador) < paginado.num_pages:
				contador.append(len(contador) + 1);
			context = {'usuario':user, 'paginado':contador , 'num_page':paginado.num_pages , 'pagina_actual':peticion_pagina}
			return render(request, 'SCASA-UT/docs/crud/usuarios/update.html', context)
		except Exception as e:
			return redirect('/usuarios/')		
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
		try:
			aulastotales = Aula.objects.all()
			try:
				peticion_pagina = str(request.GET["page"])
			except Exception as e:
				peticion_pagina = 1
			if int(peticion_pagina) > 1:
				aula = Aula.objects.all().annotate(Count('id')).order_by('id')[((int(peticion_pagina) * 5)-5):((int(peticion_pagina) * 5))]
			else:
				aula = Aula.objects.all().annotate(Count('id')).order_by('id')[:5]
			paginado = Paginator(aulastotales, 5)
			contador = []			
			while (len(contador) < paginado.num_pages) :
				contador.append(len(contador) + 1);
			return render(request, 'SCASA-UT/docs/crud/aulas/update.html', {'aulas':aula, 'paginado':contador , 'num_page':paginado.num_pages, 'pagina_actual':peticion_pagina})
		except Exception as e:
			return redirect('/aulas/')
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

def verificarPin(request, pin):
	users = User.objects.all()
	for user in users:
		if user.check_password(pin):
			maestro = Maestro.objects.get(user=user)
			horas = Hora.objects.filter(maestro = maestro)
			for hora in horas:
				if datetime.datetime.now().strftime("%A") == hora.dia.lower():
					if datetime.datetime.now().hour == hora.hora:
						nuevo_registro = RegistroEntradaAulas(maestro = maestro, 
							aula = hora.aula, 
							fecha = datetime.datetime.now(),
							fecha_hora = datetime.datetime.now().hour, 
							fecha_dia=datetime.datetime.now().strftime("%A"),
							fecha_minuto=datetime.datetime.now().minute,
							nombre_maestro = maestro.nombre, 
							nombre_aula= hora.aula.nombre)
						nuevo_registro.save()
						return HttpResponse('true')
	return HttpResponse('false')

def registroHuella(request, pin):
	try:
		usuarios = User.objects.all()
		for u in usuarios:
			if u.check_password(pin):
				return HttpResponse("R:"+ str(u.id))
	except:
		return HttpResponse('No existe')
	return HttpResponse('No existe')

def scheduler(request, id):
	if request.user.is_authenticated:
		try:
			iden = id
			if id in ["0"]:
				aulas = Aula.objects.all()
				for aula in aulas:
					idaula=aula.id
					break
				return redirect('/scheduler/'+str(idaula))
			try:
				aulas = Aula.objects.all()
				maestros = Maestro.objects.all()
			except Exception as e:
				raise


			config = Configuracion.objects.get(id=1)

			DiaSemana = []

			if config.Lunes:
				DiaSemana.append('Lunes')
			if config.Martes:
				DiaSemana.append('Martes')
			if config.Miercoles:
				DiaSemana.append('Miercoles')
			if config.Jueves:
				DiaSemana.append('Jueves')
			if config.Viernes:
				DiaSemana.append('Viernes')
			if config.Sabado:
				DiaSemana.append('Sabado')
			if config.Domingo:
				DiaSemana.append('Domingo')

			try:
				aula = Aula.objects.get(id=id)
			except:
				return redirect('/scheduler/0')

			Lunes = Hora.objects.filter(aula=aula, dia='Lunes').values()
			Martes = Hora.objects.filter(aula=aula,dia='Martes').values()
			Miercoles = Hora.objects.filter(aula=aula,dia='Miercoles').values()
			Jueves = Hora.objects.filter(aula=aula,dia='Jueves').values()
			Viernes = Hora.objects.filter(aula=aula,dia='Viernes').values()
			Sabado = Hora.objects.filter(aula=aula,dia='Sabado').values()
			Domingo = Hora.objects.filter(aula=aula,dia='Domingo').values()

			

			numeroHoras = []
			for i in range(config.hora_inicio,config.hora_fin+1):
				numeroHoras.append(i)
			return render(request, 'SCASA-UT/docs/crud/horarios/scheduler.html', {
				'horas': numeroHoras,
				'dias': DiaSemana,
				'aulas': aulas,
				'maestros':maestros,
				'Lunes':Lunes,
				'Martes':Martes,
				'Miercoles':Miercoles,
				'Jueves':Jueves,
				'Viernes':Viernes,
				'Sabado':Sabado,
				'Domingo':Domingo,
				'aulaseleccionada':aula,
				'configuracion':config
				})
		except Exception as e:
			raise
			# return redirect('/scheduler/0')
		
	else:
		return redirect('/')

def horarios_crear(request, id):
	if request.user.is_authenticated:		
		aula = Aula.objects.get(id=id)
		maestro = Maestro.objects.get(id=request.POST['maestro'])
		try:
			horario = Hora.objects.get(aula = aula, hora = request.POST['hora'], dia=request.POST['dia'])
			if horario.nombre is None:
				nuevo_horario = Hora(aula=aula, maestro=maestro, hora=request.POST['hora'], dia=request.POST['dia'], nombre=maestro.nombre, nombre_aula=aula.nombre)
				nuevo_horario.save()
				return redirect('/scheduler/'+str(id))
			else:
				horario.maestro = maestro
				horario.nombre = maestro.nombre
				horario.nombre_aula = aula.nombre
				horario.save()
			return redirect('/scheduler/'+str(id))
		except:
			nuevo_horario = Hora(aula=aula, maestro=maestro, hora=request.POST['hora'], dia=request.POST['dia'], nombre=maestro.nombre, nombre_aula=aula.nombre)
			nuevo_horario.save()		
			return redirect('/scheduler/'+str(id))
	
def seleccionar_aula(request):
	if request.user.is_authenticated:
		aula = request.POST['aula']
		return redirect('/scheduler/'+str(aula))
	else:
		return redirec('/')

def pruebas(request, pin):
	users = User.objects.all()
	for user in users:
		if user.check_password(pin):
			maestro = Maestro.objects.get(user=user)
			horas = Hora.objects.filter(maestro = maestro)
			for hora in horas:
				if datetime.datetime.now().strftime("%A") == hora.dia.lower():
					if datetime.datetime.now().hour == hora.hora:
						return HttpResponse('true')
	return HttpResponse('true')

def ver_horario(request, idmaestro):
	if request.user.is_authenticated:

		DiaSemana = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
		try:
			maestro = Maestro.objects.get(id=idmaestro)
		except:
			raise
		Lunes = Hora.objects.filter(maestro=maestro, dia='Lunes').values()
		Martes = Hora.objects.filter(maestro=maestro,dia='Martes').values()
		Miercoles = Hora.objects.filter(maestro=maestro,dia='Miercoles').values()
		Jueves = Hora.objects.filter(maestro=maestro,dia='Jueves').values()
		Viernes = Hora.objects.filter(maestro=maestro,dia='Viernes').values()
		Sabado = Hora.objects.filter(maestro=maestro,dia='Sabado').values()
		Domingo = Hora.objects.filter(maestro=maestro,dia='Domingo').values()
		numeroHoras = []
		for i in range(8,22):
			numeroHoras.append(i)
		return render(request,'SCASA-UT/docs/crud/horarios/ver.html',{
					'horas': numeroHoras,
					'dias': DiaSemana,
					'Lunes':Lunes,
					'Martes':Martes,
					'Miercoles':Miercoles,
					'Jueves':Jueves,
					'Viernes':Viernes,
					'Sabado':Sabado,
					'Domingo':Domingo,
					})
	else:
		return redirect('/')
def configuracion(request):
	configuracion = Configuracion.objects.get(id=1)
	numero = []
	for i in range(0,25):
		numero.append(i)
	return render(request, 'SCASA-UT/docs/crud/configuracion.html', {'num':numero, 'config':configuracion})

def configuracion_modificar(request):
	configuracion = Configuracion.objects.get(id=1)
	try:
		configuracion.Lunes = request.POST.get('Lunes', False)
		configuracion.Martes = request.POST.get('Martes', False)
		configuracion.Miercoles = request.POST.get('Miercoles', False)
		configuracion.Jueves = request.POST.get('Jueves', False)
		configuracion.Viernes = request.POST.get('Viernes', False)
		configuracion.Sabado= request.POST.get('Sabado', False)
		configuracion.Domingo = request.POST.get('Domingo', False)
		configuracion.hora_inicio = request.POST.get('hora_inicio', 8)
		configuracion.hora_fin = request.POST.get('hora_fin', 22)
		if int(request.POST.get('hora_inicio', 8)) > int(request.POST.get('hora_fin', 22)):
			configuracion.hora_inicio = int(configuracion.hora_fin) - 1
			if configuracion.hora_inicio == -1:
				configuracion.hora_inicio = 0
		configuracion.save()
		return redirect('/scheduler/0')
	except:
		return redirect('/configuracion')

def registro_entradas(request, id):
	if request.user.is_authenticated:
		try:
			iden = id
			if id in ["0"]:
				aulas = Aula.objects.all()
				for aula in aulas:
					idaula=aula.id
					break
				return redirect('/registros/'+str(idaula))
			try:
				aulas = Aula.objects.all()
				maestros = Maestro.objects.all()
			except Exception as e:
				raise


			config = Configuracion.objects.get(id=1)

			DiaSemana = []

			if config.Lunes:
				DiaSemana.append('Lunes')
			if config.Martes:
				DiaSemana.append('Martes')
			if config.Miercoles:
				DiaSemana.append('Miercoles')
			if config.Jueves:
				DiaSemana.append('Jueves')
			if config.Viernes:
				DiaSemana.append('Viernes')
			if config.Sabado:
				DiaSemana.append('Sabado')
			if config.Domingo:
				DiaSemana.append('Domingo')

			try:
				aula = Aula.objects.get(id=id)
			except:
				return redirect('/registros/0')

			Lunes = RegistroEntradaAulas.objects.filter(aula=aula, fecha_dia='lunes').values()
			Martes = RegistroEntradaAulas.objects.filter(aula=aula,fecha_dia='martes').values()
			Miercoles = RegistroEntradaAulas.objects.filter(aula=aula,fecha_dia='miercoles').values()
			Jueves = RegistroEntradaAulas.objects.filter(aula=aula,fecha_dia='jueves').values()
			Viernes = RegistroEntradaAulas.objects.filter(aula=aula,fecha_dia='viernes').values()
			Sabado = RegistroEntradaAulas.objects.filter(aula=aula,fecha_dia='sabado').values()
			Domingo = RegistroEntradaAulas.objects.filter(aula=aula,fecha_dia='domingo').values()
			TodosLosDias = RegistroEntradaAulas.objects.filter(aula=aula)

			numeroHoras = []
			for i in range(config.hora_inicio,config.hora_fin+1):
				numeroHoras.append(i)
			
			return render(request, 'SCASA-UT/docs/crud/registro_entradas.html', {
				'horas': numeroHoras,
				'dias': DiaSemana,
				'aulas': aulas,
				'Lunes':Lunes,
				'Martes':Martes,
				'Miercoles':Miercoles,
				'Jueves':Jueves,
				'Viernes':Viernes,
				'Sabado':Sabado,
				'Domingo':Domingo,
				'aulaseleccionada':aula,
				'configuracion':config,
				'DiasSemana':TodosLosDias
				})
		except Exception as e:
			raise
			# return redirect('/scheduler/0')
		
	else:
		return redirect('/')

def seleccionar_aula_registros(request):
	if request.user.is_authenticated:
		aula = request.POST['aula']
		return redirect('/registros/'+str(aula))
	else:
		return redirec('/')