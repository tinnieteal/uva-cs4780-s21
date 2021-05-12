import math
import nltk
nltk.downloader.download('vader_lexicon')
from .utils import *
from .models import *
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

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
            num_doc = indices.first().num_review  # Number of reveiw that contain this token

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

#without comment
def BM25_doc(query, item_obj): 
    # review_sc = bm25_review (query, item_obj)
    des_sc = bm25_des(query, item_obj)
    title_sc = bm25_title(query, item_obj)
    total_sc = des_sc + title_sc
    
    return total_sc

# def senti_BM_doc(query, item_obj):
#     score = 0
#     item_length = item_obj.desc_length + item_obj.title_length + item_obj.review_length
#     # Initialize the weights for each feature to 1
#     title_wt = 1
#     desc_wt = 1
#     review_wt = 1

#     for token in nltk_process(query):
#         indices = Index.objects.filter(word=token).all()
#         num_doc = 0
#         total_freq = 0

#         if len(indices) != 0:
#             num_doc = indices.first().items.count()  # Number of items that contain this token

#             mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
#             if len(mems) != 0:
#                 mem = mems.first()
#                 sia = SentimentIntensityAnalyzer()
#                 reviews = Review.objects.filter(item=mem.item).all()
#                 if len(reviews) != 0:
#                     # rel_reviews = []  # A list of the content of relevant reviews
#                     for r in reviews:
#                         # tokenized_review = nltk_process(r.content)
#                         # Find relevant reviews
#                     #     if token in tokenized_review:
#                     #         rel_reviews.append(r.content)
#                     # for content in rel_reviews:
#                         senti_scores = sia.polarity_scores(r.content)
#                         """ We use compound scores to decide whether the review is negative
#                         Compound score thresholds:
#                         positive: compound score>=0.05
#                         neutral: compound score between -0.05 and 0.05
#                         negative: compound score<=-0.05
#                         """
#                         if senti_scores["compound"] <= -0.05:
#                             # Reduce the weight for review if the relevant review is negative
#                             review_wt += -10
#                         elif senti_scores["compound"] >= 0.05:
#                             # Increase the weight for review if the relevant review is positive
#                             review_wt += 100

#                 total_freq = desc_wt*mem.des_df + title_wt*mem.title_df + review_wt*mem.review_df
#                 # if len(reviews) != 0:
#                 #     for review in reviews:
#                 #         if (review.rating > 3 and review.rating <= 5):
#                 #             review_wt = 5
#                 #         elif (review.rating <=3):
#                 #             review_wt = 2
#                 # review_wt = 1
#                 total_freq = desc_wt*mem.des_df + title_wt*mem.title_df + review_wt*mem.review_df

#         score += idf(num_doc) * (
#                     (total_freq * (k1 + 1)) / (total_freq + k1 * (1 - b + b * item_length / average_item_length)))

#     return score

def senti_BM_doc(query, item_obj):
    score = 0
    item_length = item_obj.review_length
    # Initialize the weights for each feature to 1
    title_wt = 1
    desc_wt = 1
    review_wt = 1

    #obtain score for title and description
    des_sc = desc_wt*bm25_des(query, item_obj)
    title_sc = title_wt*bm25_title(query, item_obj)

    #consider weight for review
    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0:
            num_doc = indices.first().num_review  # Number of reviews that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0:
                mem = mems.first()
                total_freq = mem.review_df
                sia = SentimentIntensityAnalyzer()
                reviews = Review.objects.filter(item=mem.item).all()
                if len(reviews) != 0:
                    senti_scores = []
                    rating_scores = []
                    total_score = []
                    for r in reviews:
                        senti_score = sia.polarity_scores(r.content)
                        rating = r.rating
                        senti_scores.append(senti_score["compound"])
                        rating_scores.append(rating)

                    senti_scores_norm = []
                    for s in senti_scores:
                        s = (s+1)/2
                        senti_scores_norm.append(s)
                    print ("senti score:" , senti_scores_norm)

                    rating_norm = np.linalg.norm(rating_scores)
                    rating_scores = rating_scores/rating_norm
                    print("rating score:" , rating_scores)

                    total_score = np.add(senti_scores, rating_scores)

                    negative_review_ct = 0
                    neutral_review_ct = 0
                    positive_review_ct = 0

                    for s in total_score:
                        if s <= 0.875:
                            negative_review_ct += 1
                        elif s > 0.875 and s < 1.125:
                            neutral_review_ct += 1
                        else:
                            positive_review_ct += 1
                    if negative_review_ct == 1: 
                        if positive_review_ct ==2:
                            review_wt = 1
                        elif positive_review_ct == 1:
                            review_wt = 0.75
                        else:
                            review_wt = 0.5
                    elif negative_review_ct == 2:
                        if positive_review_ct ==1:
                            review_wt = -0.25
                        else: 
                            review_wt = -0.5
                    elif negative_review_ct == 0:
                        if positive_review_ct == 1:
                            review_wt = 1.25
                        elif positive_review_ct == 2:
                            review_wt = 1.5
                        elif positive_review_ct == 3:
                            review_wt = 2
                        else:
                            review_wt = 1
                    else:
                        review_wt = -1

                    # for r in reviews:
                    #     senti_score = sia.polarity_scores(r.content)
                    #     if (senti_score <= -0.05):
                    #         senti_scores_negative.append(r.rating)
                    #     elif (senti_score > -0.05 and senti_score < 0.05):
                    #         senti_scores_neutral.append(r.rating)
                    #     else:
                    #         senti_scores_postive.append(r.rating)
                    """ We use compound scores to decide whether the review is negative
                    Compound score thresholds:
                    positive: compound score>=0.05
                    neutral: compound score between -0.05 and 0.05
                    negative: compound score<=-0.05
                    """
 
        review_sc += review_wt*(idf(num_doc) * (
                    (total_freq * (k1 + 1)) / (total_freq + k1 * (1 - b + b * item_length / average_item_length))))

    score = review_sc + des_sc + title_sc

    return score


