import sys, os, json
import django

# sys.path.append('your_project_directory')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MATA.settings'
django.setup()

from Search.models import * 
from Search.utils import *


def process(img_url):
	return img_url.replace("._SS40_.jpg", ".jpg")

#load dataset
with open('all_beauty.json', 'r') as f:
		data = json.load(f)


index = {}

num_item = 0 
item_length_all = 0
item_length_desc = 0 
item_length_review = 0 
item_length_title = 0 

#loop through all items in dataset, assign fields correspondingly
for item in data:
	asin = item["asin"]
	description = item["description"]
	title = item["title"] 
	rank = item['rank']
	img =  process(item["image"][0])
	if img == None:
		print( item["image"][0] )

	#update doc frequency for item's title
	freq_table = {}
	tokenized_title = nltk_process(title)
	title_wordcount = len(tokenized_title)
	for word in tokenized_title:
		if word not in freq_table:
			freq_table[word] = {
			"des_freq":0,
			"title_freq":0,
			"review_freq":0,
			}
		freq_table[word]["title_freq"] += 1

	tokenized_description = nltk_process(description)
	desc_wordcount = len(tokenized_description)
	#update doc frequency for item's description
	for word in tokenized_description:
		if word not in freq_table:
			freq_table[word] = {
			"des_freq":0,
			"title_freq":0,
			"review_freq":0,
			}
		freq_table[word]["des_freq"] += 1

	total_review_wordcount = 0
	#loop thorugh all the reviews for this item

	review_wordcounts = []

	for review in item["reviewText"]:
		#if no reviews are found, print "found empty review"
		if review == None:
			print("found empty review")
			continue
		#update review wordcount
		tokenized_review = nltk_process(review)
		review_wordcount = len(tokenized_review)

		review_wordcounts.append(review_wordcount)

		#update total review wordcount
		total_review_wordcount += len(tokenized_review)

		for word in tokenized_review:
			if word not in freq_table:
				freq_table[word] = {
				"des_freq":0,
				"title_freq":0,
				"review_freq":0,
				}
			freq_table[word]["review_freq"] += 1	

	# save all item info, except for review
	item_obj = Item.objects.create(title=title, description=description, asin=asin, image=img,
								   title_length=title_wordcount, desc_length=desc_wordcount, review_length=total_review_wordcount)
	item_obj.save()

	num_item += 1
	item_length_desc += desc_wordcount
	item_length_review += total_review_wordcount
	item_length_title += title_wordcount
	item_length_all += (title_wordcount +  desc_wordcount + total_review_wordcount)


	for review, review_wordcount,review_rating in zip(item["reviewText"], review_wordcounts, item["overall"] ):
		review_obj = Review.objects.create(content=review, item=item_obj,length=review_wordcount, rating=review_rating)
		#save review objects
		review_obj.save()


	#loop through each item and its corresponding doc freq in the freq table
	for word, freq_map in freq_table.items():

		#create the word if not in index{} 
		if word not in index:
			index_obj = Index.objects.create(word=word)
			index[word] = index_obj

		#otherwise, create a membership object, and update all relevant fields
		mem_obj = Membership.objects.create(item=item_obj,
			index=index[word], 
			des_df=freq_map["des_freq"], 
			title_df=freq_map["title_freq"], 
			review_df=freq_map["review_freq"])

		mem_obj.save()
		

#update term frequency (tf) for each item
for index_obj in Index.objects.all():

	#tf initialziation description, title, and review 
	des_tf = 0
	title_tf = 0
	review_tf = 0
	items = []

	#loop through all membership objects, accumulate term freq
	for mem_obj in Membership.objects.filter(index=index_obj).all():
		des_tf += mem_obj.des_df
		title_tf += mem_obj.title_df	
		review_tf += mem_obj.review_df
		index_obj.items.add(mem_obj.item.pk)
	# print( des_tf, title_tf, review_tf )

	Index.objects.filter(pk=index_obj.pk).update(
		des_tf = des_tf,
		title_tf = title_tf,
		review_tf = review_tf
		)


print( "num_item: {} ".format(  num_item ) )
"----dividing line-----"
print( "totol description length: {} ".format(  item_length_desc ) )
print( "totol title length: {} ".format(  item_length_title ) )
print( "totol review length: {} ".format(  item_length_review ) )
print( "total item document length: {} ".format(  item_length_all ) )
"----dividing line-----"
print( "average description length: {} ".format(  item_length_desc / num_item ) )
print( "average title length: {} ".format(  item_length_title / num_item ) )
print( "average review length: {} ".format(  item_length_review / num_item ) )
print( "item length averge: {} ".format(  item_length_all / num_item ) )

# print( len(Item.objects.all()) )
# print( len(Review.objects.all()) )
# print( len(Membership.objects.all()) )
# print( len(Index.objects.all()) )