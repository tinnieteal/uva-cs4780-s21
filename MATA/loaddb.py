import sys, os, json
import django

# sys.path.append('your_project_directory')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MATA.settings'
django.setup()

from Search.models import * 
from Search.utils import *

#load dataset
with open('all_beauty.json', 'r') as f:
		data = json.load(f)


index = {}

#process 
for item in data:
	asin = item["asin"] 
	description = item["description"][0] if len(item["description"]) != 0 else ""
	title = item["title"] 
	img = item["image"][0]

	freq_table = {}
	for word in tokenize(title):
		if word not in freq_table:
			freq_table[word] = {
			"des_freq":0,
			"title_freq":0,
			"review_freq":0,
			}
		freq_table[word]["title_freq"] += 1

	for word in tokenize(description):
		if word not in freq_table:
			freq_table[word] = {
			"des_freq":0,
			"title_freq":0,
			"review_freq":0,
			}
		freq_table[word]["des_freq"] += 1
	

	item_obj = Item.objects.create(title=title, description=description, asin=asin, image=img)
	item_obj.save()

	for review in item["reviewText"]:
		if review == None:
			print("found empty review")
			continue
		review_obj = Review.objects.create(content=review, item=item_obj)

		for word in tokenize(review):
			if word not in freq_table:
				freq_table[word] = {
				"des_freq":0,
				"title_freq":0,
				"review_freq":0,
				}
			freq_table[word]["review_freq"] += 1	

		review_obj.save()

	for word, freq_map in freq_table.items():
		if word not in index:
			index_obj = Index.objects.create( word=word)
			index[word] = index_obj

		mem_obj = Membership.objects.create(item=item_obj,
			index=index[word], 
			des_df=freq_map["des_freq"], 
			title_df=freq_map["title_freq"], 
			review_df=freq_map["review_freq"])

		mem_obj.save()
		


# for word, index_obj in index.items():
for index_obj in Index.objects.all():
	des_tf = 0
	title_tf = 0
	review_tf = 0
	items = []
	for mem_obj in Membership.objects.filter(index=index_obj).all():
		des_tf += mem_obj.des_df
		title_tf += mem_obj.title_df
		review_tf += mem_obj.review_df
		index_obj.items.add(mem_obj.item.pk)

	Index.objects.filter(pk=index_obj.pk).update(
		des_tf = des_tf,
		title_tf = title_tf,
		review_tf = review_tf
		)
	# index = Index.objects.create( word=word, items=index_item[word])
	# index.save()



# print( len(Item.objects.all()) )
# print( len(Review.objects.all()) )
# print( len(Membership.objects.all()) )
# print( len(Index.objects.all()) )