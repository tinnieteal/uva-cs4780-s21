from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import *
from .utils import *
from .ranking_utils import *

import math

def index(request):

    return render(request, 'search/index.html',)


def result(request):
    query = request.POST.get('query')
    if request.POST:
        if 'none' in request.POST:
            choice = request.POST.get('none')
        elif 'bm25_title' in request.POST:
            choice = request.POST.get('bm25_title')
        elif 'bm25_combine_later' in request.POST:
            choice = request.POST.get('bm25_combine_later')
        elif 'senti_BM25' in request.POST:
            choice = request.POST.get('senti_BM25')
        else:
            choice = "none"

    results = []
    # reviews = []
    # loop through the tokenized & normalized token of the query
    asin_set = set()

    if choice == "bm25_title":
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

                ranking_score = bm25_title(query, item_obj)
                results.append((ranking_score, item_obj, reviews))
        results.sort(key=lambda element: element[0], reverse=True)

    elif choice == "bm25_combine_later":
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

                ranking_score = bm25_combine_later(query, item_obj)
                results.append((ranking_score, item_obj, reviews))
        results.sort(key=lambda element: element[0], reverse=True)

    elif choice == "senti_BM25":
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

                ranking_score = senti_BM(query, item_obj)
                results.append((ranking_score, item_obj, reviews))
        results.sort(key=lambda element: element[0], reverse=True)

    elif choice == "none":
        ranking_score = "no ranking"
        for token in nltk_process(query):
            indices = Index.objects.filter(word=token).all()
            if len(indices) == 0:
                continue
            for mem in Membership.objects.filter(index=indices.first()).all():
                results.append((ranking_score, mem.item, Review.objects.filter(item=mem.item)))

    return render(request, 'search/result.html',{'query': query, 'results': results, 'choice':choice})

def detail(request, asin):
    query = request.POST.get('query')
    items = Item.objects.filter(asin = asin).all()
    if len(items) != 0:
        reviews = Review.objects.filter(item=items.first())
        return render(request, 'search/detail.html',{'item': items.first(), 'reviews': reviews, 'query':query})

    return None
    # # loop through the tokenized & normalized token of the query
    # for token in nltk_process(query):
    #     indices = Index.objects.filter(word=token).all()
    #     if len(indices) == 0:
    #         continue
    #     for mem in Membership.objects.filter(index=indices.first()).all():
    #         results.append(mem.item)
    #
    # return render(request, 'search/result.html', {'query': query, 'allItem': results})


    # if query:
    #     posts = item.objects.filter(title__icontains=q)
    # else:
    #     posts = item.objects.all()
    # params = {'allposts': posts}
    # paginator = Paginator(posts, 2)
    # page_number = request.GET.get('page')
    # posts_obj = paginator.get_page(page_number)

    #return render(request, 'Search/result.html',params)
    #return HttpResponse('this is search')

    # list_doc = {}
    # for q in query:
    #     try:
    #         for doc in indexFile[q]:
    #             if doc['url'] in list_doc:
    #                 list_doc[doc['url']]['score'] += doc['score']
    #             else:
    #                 list_doc[doc['url']] = doc
    #     except:
    #         continue
    #
    # # convert to list
    # list_data = []
    # for data in list_doc:
    #     list_data.append(list_doc[data])
    #
    # # sorting list descending
    # count = 1;
    # for data in sorted(list_data, key=lambda k: k['score'], reverse=True):
    #     y = json.dumps(data)
    #     print(y)
    #     if (count == n):
    #         break
    #     count += 1
