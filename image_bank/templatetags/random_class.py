from django import template
import random

register = template.Library()
class_list = ['badge rounded-pill badge-primary', 'badge rounded-pill badge-dark',
              'badge rounded-pill badge-info', 'badge rounded-pill badge-secondary', 'badge rounded-pill badge-success']

@register.simple_tag
def random_class():
    selected_class = random.choice(class_list)
    return selected_class