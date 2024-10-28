
from django import template

register = template.Library()

@register.filter
def get_color(colors, index):
    color_list = colors.split(',')
    return color_list[index % len(color_list)]
