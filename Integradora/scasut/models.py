from django.db import models
from django import forms
from django.contrib.auth import authenticate

class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, null=True)


class CicloEscolar(models.Model):
    descripcion = models.CharField(max_length=100)


class Dia(models.Model):
    nombre = models.CharField(max_length=10)
    habil = models.BooleanField()


class Horario(models.Model):
    idcicloescolar = models.ForeignKey(CicloEscolar)


class Grupo(models.Model):
    idhorario = models.ForeignKey(Horario)


class Maestro(models.Model):
    nombre = models.CharField(max_length=20)


class Hora(models.Model):
    hora = models.CharField(max_length=10)
    idhorario = models.ForeignKey(Horario)
    iddia = models.ForeignKey(Dia)
    idmaestro = models.ForeignKey(Maestro)
    idaula = models.ForeignKey(Aula)


class Usuario(models.Model):
    usuario = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=10)
    huelladigitalbase64 = models.BinaryField()
    idmaestro = models.ForeignKey(Maestro)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('contrasena')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Lo sentimos su usuario no se encontro")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('usuario')
        user = authenticate(username=username, password=password)
        return user

    def obtencionValores(self, request):
        username = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('contrasena')
        ms = self.cleaned_data.get('maestro')
        msss = Maestro.objects.filter(id=1)
        usuario = Usuario(usuario='aaa', contrasena = 'asdas', idmaestro= msss.id)
        usuario.save()
        return True