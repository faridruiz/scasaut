from django.db import models
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, null=True)

# class CicloEscolar(models.Model):
#     descripcion = models.CharField(max_length=100)

# class Dia(models.Model):
#     nombre = models.CharField(max_length=10)
#     habil = models.BooleanField()
class Maestro(models.Model):
    nombre = models.CharField(max_length=20)    
    user = models.OneToOneField(User, unique=True, null = True)

class Horario(models.Model):
    idmaestro = models.ForeignKey(Maestro, null= True)

# class Grupo(models.Model):
#     nombre = models.CharField(max_length=32, null=True)
#     descripcion = models.CharField(max_length=100, null=True)
#     #idhorario = models.ForeignKey(Horario)


class Hora(models.Model):
    hora = models.IntegerField()
    idhorario = models.ForeignKey(Horario)
    idaula = models.ForeignKey(Aula)

class Usuario(models.Model):
    usuario = models.CharField(max_length=20)
    contrasena = models.IntegerField()    
    idmaestro = models.ForeignKey(Maestro)
    EsAdministrador = models.BooleanField(default = False)
