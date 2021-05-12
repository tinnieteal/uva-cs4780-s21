from .models import *
from .ranking_utils import *

import math

def search_BM25_doc(query ):
    results = []
    # reviews = []
    # loop through the tokenized & normalized token of the query
    asin_set = set()

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        if len(indices) == 0:
            continue
        for mem in Membership.objects.filter(index=indices.first()).all():
            item_obj = mem.item
            if item_obj.asin in asin_set:
                continue
            asin_set.add(item_obj.asin)

            reviews = Review.objects.filter(item=mem.item)

            ranking_score = BM25_doc(query, item_obj)
            results.append((ranking_score, item_obj, reviews))
    results.sort(key=lambda element: element[0], reverse=True)

    return results

def search_BM25_fields(query ):
    results = []
    # reviews = []
    # loop through the tokenized & normalized token of the query
    asin_set = set() 
    
    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        if len(indices) == 0:
            continue
        for mem in Membership.objects.filter(index=indices.first()).all():
            item_obj = mem.item
            if item_obj.asin in asin_set:
                continue
            asin_set.add(item_obj.asin)

            reviews = Review.objects.filter(item=mem.item)

            ranking_score = BM25_fields(query, item_obj)
            results.append((ranking_score, item_obj, reviews))
    results.sort(key=lambda element: element[0], reverse=True)
    return results

def search_senti_BM25_doc(query):
    results = []
    # reviews = []
    # loop through the tokenized & normalized token of the query
    asin_set = set()

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        if len(indices) == 0:
            continue
        for mem in Membership.objects.filter(index=indices.first()).all():
            item_obj = mem.item
            if item_obj.asin in asin_set:
                continue
            asin_set.add(item_obj.asin)

            reviews = Review.objects.filter(item=mem.item)

            ranking_score = senti_BM_doc(query, item_obj)
            results.append((ranking_score, item_obj, reviews))
    results.sort(key=lambda element: element[0], reverse=True)
    return results

def search_none(query):
    results = []
    # reviews = []
    # loop through the tokenized & normalized token of the query
    asin_set = set()

    ranking_score = "no ranking"
    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        if len(indices) == 0:
            continue
        for mem in Membership.objects.filter(index=indices.first()).all():
            results.append((ranking_score, mem.item, Review.objects.filter(item=mem.item)))
    return results