from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    # categories
    CLOTHING = 'CL'
    ELECTRONICS = 'EL'
    BOOKS = 'BK'
    GROCERIES = 'GR'
    FOOTWEAR = 'FT'
    PLANTS = 'PL'
    STATIONARY = 'ST'
    OTHER = 'OT'
    category_choices = [
        (CLOTHING, 'Clothing'),
        (ELECTRONICS, 'Electronics'),
        (BOOKS, 'Books'),
        (GROCERIES, 'Groceries'),
        (FOOTWEAR, 'Footwear'),
        (PLANTS, 'Plants'),
        (STATIONARY, 'Stationary'),
        (OTHER, 'Other')
    ]
    category = models.CharField(
        max_length = 2,
        choices = category_choices,
        default = OTHER,
        editable = True
    )

    name = models.CharField(max_length=120)
    price = models.IntegerField()
    image = models.URLField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator_lister")
    status = models.BooleanField(default=True, editable=True)
    winner = models.PositiveIntegerField(default=0, editable=True)




class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listed_itm")
    comment = models.CharField(max_length=240)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")

class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listed_bid')
    bid = models.PositiveIntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_maker')

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_creator')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist_item')


def default_user():
    return User()
