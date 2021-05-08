import math
from .utils import *
from .models import *

num_items = 1000
average_item_length = 110.297
k1 = 1.5 ## [1.2, 2.0]
b = 0.75 

def bm25(query, item_obj): 
    score = 0
    item_length = item_obj.desc_length + item_obj.title_length + item_obj.review_length

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0: 
            num_doc = indices.first().items.count()

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0: 
                mem = mems.first()
                total_freq = mem.des_df + mem.title_df + mem.review_df

        score += idf(num_doc) * ((total_freq * (k1+1)) / (total_freq + k1 * (1-b+b * item_length /average_item_length)))

    return score

def idf(num_doc):
    return math.log( (num_items - num_doc + 0.5) / (num_doc + 0.5) + 1 )
