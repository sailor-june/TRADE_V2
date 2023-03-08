from django.contrib import admin
from .models import Profile, Item, TradeOffer

# Register your models here.
admin.site.register(Profile)
admin.site.register(TradeOffer)


from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'owner')

admin.site.register(Item, ItemAdmin)