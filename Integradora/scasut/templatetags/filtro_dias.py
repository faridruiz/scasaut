from django.template.defaultfilters import stringfilter
from django import template
from scasut.models import Maestro

register = template.Library()

@register.filter
def in_category(dia, horadef):
	return dia.filter(hora=horadef).values()

@register.filter
def filtro_hora(dia, horadef):
	return dia.filter(fecha_hora=horadef).values()