from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    return form[field_name]

@register.filter
def get_field_value(form, field_name):
    return form[field_name].value()