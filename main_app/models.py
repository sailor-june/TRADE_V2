from django.db import models
from django.contrib.auth.models import User

    

class Item(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    item_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile = Profile.objects.get(user=self.owner)
        profile.inventory.add(self)
        profile.save()
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inventory = models.ManyToManyField(Item)

    def get_inventory_items(self):
        return self.inventory.all()
    
class TradeOffer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_trade_offers')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_trade_offers')
    item_to_trade = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_requested = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='received_trade_offers')
    message = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
