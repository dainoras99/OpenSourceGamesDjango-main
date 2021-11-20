from django import template
register = template.Library()

@register.simple_tag
def define_action(val=None):
  return val