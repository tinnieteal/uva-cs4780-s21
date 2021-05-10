import math
from .utils import *
from .models import *
from nltk.sentiment import SentimentIntensityAnalyzer

num_items = 1000  # Total number of items
average_item_length = 143.77
k1 = 1.5  ## [1.2, 2.0]
b = 0.75 

def idf(num_doc):
    return math.log( (num_items - num_doc + 0.5) / (num_doc + 0.5) + 1 )

def bm25_without_comment(query, item_obj): 
    score = 0
    item_length = item_obj.desc_length + item_obj.title_length

    for token in nltk_process(query):
        indices = Index.objects.filter(word=token).all()
        num_doc = 0
        total_freq = 0

        if len(indices) != 0: 
            num_doc = indices.first().items.count()  # Number of items that contain this token

            mems = Membership.objects.filter(index=indices.first(), item=item_obj).all()
            if len(mems) != 0: 
                mem = mems.first()
                total_freq = mem.des_df + mem.title_df

        score += idf(num_doc) * ((total_freq * (k1+1)) / (total_freq + k1 * (1-b+b * item_length / average_item_length)))
    return score


def bm25(query, item_obj): 
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

def senti_BM(query, item_obj):
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
                reviews = Review.object.filter(item=item_obj)
                if len(reviews) != 0:
                    rel_reviews = []  # A list of the content of relevant reviews
                    for r in reviews:
                        tokenized_review = nltk_process(r.content)
                        # Find relevant reviews
                        if token in tokenized_review:
                            rel_reviews.append(r.content)
                    for content in rel_reviews:
                        senti_scores = sia.polarity_scores(content)
                        """ We use compound scores to decide whether the review is negative
                        Compound score thresholds:
                        positive: compound score>=0.05
                        neutral: compound score between -0.05 and 0.05
                        negative: compound score<=-0.05
                        """
                        if senti_scores["compound"] <= -0.05:
                            # Reduce the weight for review if the relevant review is negative
                            review_wt = 0.5
                        elif senti_scores["compound"] >= 0.05:
                            # Increase the weight for review if the relevant review is positive
                            review_wt = 1.5
                total_freq = desc_wt*mem.des_df + title_wt*mem.title_df + review_wt*mem.review_df

        score += idf(num_doc) * (
                    (total_freq * (k1 + 1)) / (total_freq + k1 * (1 - b + b * item_length / average_item_length)))

    return score