from django import template
from django.shortcuts import render
from django.template.defaultfilters import stringfilter
from django.template import Template
from django.utils.safestring import mark_safe
from re import IGNORECASE, compile, escape as rescape

import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

#nltk.download("punkt")
#nltk.download('averaged_perceptron_tagger')

register = template.Library()

@register.filter
def highlight_search(text, search):
    tokens = nltk.word_tokenize(search)
    i = 0
    for token in tokens:
        rgx = compile(rescape(token), IGNORECASE)
        text = rgx.sub(
                lambda m: '<mark>{}</mark>'.format(m.group()),
                text
            )
    return mark_safe(text)