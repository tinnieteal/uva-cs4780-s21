from django.contrib import admin
from .models import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title','description','image','rank')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'length', 'rating')

class IndexAdmin(admin.ModelAdmin):
    list_display = ('word', 'des_tf', 'title_tf', 'review_tf', 'get_items', 'num_title', 'num_des','num_review')

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('index', 'item', 'des_df', 'title_df', 'review_df')

admin.site.register(Item,ItemAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Index,IndexAdmin)
admin.site.register(Membership,MembershipAdmin)