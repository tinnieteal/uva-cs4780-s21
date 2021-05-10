from django import template
from django.shortcuts import render
from django.template.defaultfilters import stringfilter
from django.template import Template
from django.utils.safestring import mark_safe
from re import IGNORECASE, compile, escape as rescape

register = template.Library()

@register.filter
def highlight_search(text, search):
    rgx = compile(rescape(search), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text text-danger">{}</b>'.format(m.group()),
            text
        )
    )