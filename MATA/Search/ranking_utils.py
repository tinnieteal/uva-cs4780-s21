import math
import nltk
nltk.downloader.download('vader_lexicon')
from .utils import *
from .models import *
from nltk.sentiment import SentimentIntensityAnalyzer

import nltk
nltk.download('vader_lexicon')

num_items = 4048  # Total number of items
average_desc_length = 64.38117588932806
average_title_length = 12.563735177865613
average_review_length = 70.05681818181819
average_item_length = 147.00172924901185
k1 = 1.5  ## [1.2, 2.0]
b = 0.75 

def idf(num_doc):
    return math.log( (num_items - num_doc + 0.5) / (num_doc + 0.5) + 1 )

def bm25_title(query, item_obj): 
    score = 0
    item_length = item_obj.title_length

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0: 
            num_doc = indices.first().num_title  # Number of titles that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0: 
                mem = mems.first()
                total_freq = mem.title_df

        score += idf(num_doc) * ((total_freq * (k1+1)) / (total_freq + k1 * (1-b+b * item_length / average_title_length)))
    

    return score

def bm25_des(query, item_obj): 
    score = 0
    item_length = item_obj.desc_length

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0: 
            num_doc = indices.first().num_des  # Number of titles that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0: 
                mem = mems.first()
                total_freq = mem.des_df

        score += idf(num_doc) * ((total_freq * (k1+1)) / (total_freq + k1 * (1-b+b * item_length / average_review_length)))

    return score

def bm25_review (query, item_obj):
    score = 0
    item_length = item_obj.review_length

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0: 
            num_doc = indices.first().num_review  # Number of titles that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0: 
                mem = mems.first()
                total_freq = mem.review_df

        score += idf(num_doc) * ((total_freq * (k1+1)) / (total_freq + k1 * (1-b+b * item_length / average_item_length)))

    return score

def BM25_fields (query, item_obj):
    review_sc = bm25_review (query, item_obj)
    des_sc = bm25_des(query, item_obj)
    title_sc = bm25_title(query, item_obj)
    total_sc = review_sc + des_sc + title_sc
    
    return total_sc

def BM25_doc(query, item_obj): 
    score = 0
    item_length = item_obj.desc_length + item_obj.title_length + item_obj.review_length

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0: 
            num_doc = indices.first().items.count()  # Number of items that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0: 
                mem = mems.first()
                total_freq = mem.des_df + mem.title_df + mem.review_df

        score += idf(num_doc) * ((total_freq * (k1+1)) / (total_freq + k1 * (1-b+b * item_length / average_item_length)))

    return score

def senti_BM_doc(query, item_obj):
    score = 0
    item_length = item_obj.desc_length + item_obj.title_length + item_obj.review_length
    # Initialize the weights for each feature to 1
    title_wt = 1
    desc_wt = 1
    review_wt = 1

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0:
            num_doc = indices.first().items.count()  # Number of items that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0:
                mem = mems.first()
                sia = SentimentIntensityAnalyzer()
                reviews = Review.objects.filter(item=mem.item).all()
                if len(reviews) != 0:
                    # rel_reviews = []  # A list of the content of relevant reviews
                    for r in reviews:
                        # tokenized_review = nltk_process(r.content)
                        # Find relevant reviews
                    #     if token in tokenized_review:
                    #         rel_reviews.append(r.content)
                    # for content in rel_reviews:
                        senti_scores = sia.polarity_scores(r.content)
                        """ We use compound scores to decide whether the review is negative
                        Compound score thresholds:
                        positive: compound score>=0.05
                        neutral: compound score between -0.05 and 0.05
                        negative: compound score<=-0.05
                        """
                        if senti_scores["compound"] <= -0.05:
                            # Reduce the weight for review if the relevant review is negative
                            review_wt += -10
                        elif senti_scores["compound"] >= 0.05:
                            # Increase the weight for review if the relevant review is positive
                            review_wt += 100

                total_freq = desc_wt*mem.des_df + title_wt*mem.title_df + review_wt*mem.review_df
                # if len(reviews) != 0:
                #     for review in reviews:
                #         if (review.rating > 3 and review.rating <= 5):
                #             review_wt = 5
                #         elif (review.rating <=3):
                #             review_wt = 2
                # review_wt = 1
                total_freq = desc_wt*mem.des_df + title_wt*mem.title_df + review_wt*mem.review_df

        score += idf(num_doc) * (
                    (total_freq * (k1 + 1)) / (total_freq + k1 * (1 - b + b * item_length / average_item_length)))

    return score