from django.contrib import admin
from .models import (RequestProductImage, ProductRecord,
                     CustomerProductView, 
                     CustomerSearch,NewsLetterSubscriber,
                     DailyVisitors, TotalVisitors,
                     Bookmark, Wishlist, 
                     CustomerProductActivity)




admin.site.register(RequestProductImage)
admin.site.register(ProductRecord)
#admin.site.register(CustomerProductView)
# admin.site.register(CustomerSearch)
admin.site.register(NewsLetterSubscriber)
admin.site.register(DailyVisitors)
admin.site.register(TotalVisitors)
admin.site.register(Bookmark)
admin.site.register(Wishlist)
admin.site.register(CustomerProductActivity)
