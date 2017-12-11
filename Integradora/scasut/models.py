from django.db import models
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, null=True)

class Maestro(models.Model):
    nombre = models.CharField(max_length=20)
    user = models.OneToOneField(User, unique=True, null = True)

class Hora(models.Model):
    hora = models.IntegerField()
    maestro = models.ForeignKey(Maestro, null=True)
    nombre = models.CharField(null=True, max_length=100)
    aula = models.ForeignKey(Aula)
    nombre_aula = models.CharField(null=True, max_length=100)
    dia = models.CharField(default=True, max_length=100);

class Usuario(models.Model):
    usuario = models.CharField(max_length=20)
    contrasena = models.IntegerField()    
    idmaestro = models.ForeignKey(Maestro, null = True)
    EsAdministrador = models.BooleanField(default = False)

class RegistroEntradaAulas(models.Model):
    maestro = models.ForeignKey(Maestro)
    aula = models.ForeignKey(Aula)
    fecha = models.DateTimeField(null=True)
    fecha_dia = models.CharField(null=True, max_length=100)
    fecha_hora = models.CharField(null=True, max_length=100)
    fecha_minuto = models.CharField(null=True, max_length=100)
    nombre_maestro = models.CharField(null=True, max_length=100)
    nombre_aula = models.CharField(null=True, max_length=100)

class Configuracion(models.Model):
    hora_inicio = models.IntegerField(default=8)
    hora_fin = models.IntegerField(default=22)
    Lunes = models.BooleanField(default=True)
    Martes = models.BooleanField(default=True)
    Miercoles = models.BooleanField(default=True)
    Jueves = models.BooleanField(default=True)
    Viernes = models.BooleanField(default=True)
    Sabado = models.BooleanField(default=True)
    Domingo = models.BooleanField(default=True)
