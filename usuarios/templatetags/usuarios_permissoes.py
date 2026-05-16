from django import template

from usuarios.utils import usuario_eh_administrador

register = template.Library()


@register.filter
def eh_administrador(user):
    return usuario_eh_administrador(user)
