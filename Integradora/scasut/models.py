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
    dia = models.CharField(default=True, max_length=100);

class Usuario(models.Model):
    usuario = models.CharField(max_length=20)
    contrasena = models.IntegerField()    
    idmaestro = models.ForeignKey(Maestro, null = True)
    EsAdministrador = models.BooleanField(default = False)
