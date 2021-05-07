from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import *
from .utils import *

def index(request):

    return render(request, 'search/index.html',)

def result(request):
    query = request.POST.get('query')

    results = []
    #loop through the tokenized & normalized token of the query
    for token in nltk_process(query):
        if len(indices) == 0: 
            continue
        for mem in Membership.objects.filter(index=indices.first()).all():
            results.append((mem.item, Review.objects.filter(item=mem.item)))
    return render(request, 'search/result.html',{'query': query, 'results': results})

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
