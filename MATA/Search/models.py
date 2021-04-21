from django.db import models

# Create your models here.
class Item(models.Model):
    title=models.CharField(max_length=128)
    description=models.TextField()
    asin=models.CharField(max_length=10)
    image = models.TextField(max_length=500, default="")
 
    def __str__(self):
        return self.asin

class Review(models.Model):
    content = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return "review of "+self.item+ ": " + self.content[0]

class Index(models.Model):
    word = models.CharField(max_length=128, default="")
    items = models.ManyToManyField(Item, through='Membership')
    des_tf = models.IntegerField(default=0)
    title_tf = models.IntegerField(default=0)
    review_tf = models.IntegerField(default=0)

    def __str__(self):
        return self.word

class Membership(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    index = models.ForeignKey(Index, on_delete=models.CASCADE)
    des_df = models.IntegerField()
    title_df = models.IntegerField()
    review_df = models.IntegerField()









>>>>>>> database loaded and inverted index created

