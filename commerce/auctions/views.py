from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .auction_forms import *

from .models import *


def index(request):
    """ displays active listings on the home page
    """
    listings = Listing.objects.all()
    open_listings = [listing for listing in listings if listing.status]
    closed_listings = [listing for listing in listings if not listing.status]
    return render(request, "auctions/index.html",{
        "open_listings" : open_listings,
        "closed_listings" : closed_listings
    })

@login_required
def createlisting(request):
    """ creates listing object and saves to db,
        also displays new form if request is GET
    """
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            object = Listing()
            object.name = form.cleaned_data["name"]
            object.price = form.cleaned_data["price"]
            object.image = form.cleaned_data["image"]
            object.creator = request.user
            object.status = True
            object.category = form.cleaned_data["category"]
            object.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "error" : "Insert proper image link"
            })
    else:
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            "form" : form,
        })

def active_listing(request, listing_id, newContext={}):
    """ Displays the individual listing page
    """
    form = BidsForm()
    user = User.objects.get(username=request.user.username)
    try:
        listed = Listing.objects.get(id=listing_id)
    except Lising.DoesNotExist:
        listed = None
    past_bids = Bids.objects.all().filter(listing=listed)
    # validating pastbids
    if len(past_bids) == 0:
        past_bids = None
    try:
        complete_watchlist = Watchlist.objects.all().filter(user=user)
    except Watchlist.DoesNotExist:
        complete_watchlist = False
    context = {
        "form": form,
        "listing": listed,
        "watchlist": complete_watchlist,
        "pastbids": past_bids,
        "error": None
        }
    context.update(newContext)
    return render(request, "auctions/listings.html", context=context)

def place_bid(request):
    """ places the bids
    """
    if request.method == "POST":
        form = BidsForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(id=request.POST["listing_id"])
            past_bids = Bids.objects.all().filter(listing=listing)
            bid = form.cleaned_data["bid"]
            if bid_validator(past_bids, bid, listing.price):
                object = Bids()
                object.bid = bid
                object.bidder = request.user
                object.listing = listing
                object.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                context = {
                    "error" : "Invalid Bid, Either bid already exists or you bidded lower than asked price."
                }
                return active_listing(request,listing.id,context)
    else:
        return render(request, "auctions/create_listing.html", {
            "error" : "Insert proper image link"
        })

def bid_validator(past_bids, bid, price):
    all_bids = [bid.bid for bid in past_bids]
    if not all_bids:
        if price > bid:
            return False
        return True
    if int(max(all_bids)) > int(bid) and int(bid) < int(price):
        return False
    else:
        return True

def watchlist(request):
    """ renders the users watchlist
    """
    user = User.objects.get(username=request.user.username)
    try:
        complete_watchlist = Watchlist.objects.all().filter(user=user)
    except Watchlist.DoesNotExist:
        watchlist = None
    return render(request, "auctions/watchlist.html",{
        "watchlist" : complete_watchlist
    })

def add_to_watchlist(request, listing_id):
    """ adds item to watchlist
    """
    user = User.objects.get(username=request.user.username)
    try:
        watchlist = Watchlist.objects.get(listing=listing_id, user=user.id)
    except Watchlist.DoesNotExist:
        watchlist = Watchlist()
        watchlist.listing = Listing.objects.get(id=listing_id)
        watchlist.user = User.objects.get(id=user.id)
        watchlist.save()
    complete_watchlist = Watchlist.objects.all().filter(user=user)
    return render(request, "auctions/watchlist.html",{
        "watchlist": complete_watchlist
    })

def removefromwatchlist(request, listing_id):
    """ removes item from playlist """
    user = User.objects.get(username=request.user.username)
    listing = Listing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.get(user=user, listing=listing)
    watchlist.delete()
    return active_listing(request, listing_id)

def close_auction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bids = Bids.objects.all().filter(listing=listing)
    bids_objects_list = [bid for bid in bids]
    bids_list = [bid.bid for bid in bids]
    value = bids_list.index(max(bids_list))
    winner = bids_objects_list[value].bidder.id
    print(winner)
    listing.status = False
    listing.winner = winner
    listing.save()
    return index(request)

def showresult(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    winner_id = listing.winner
    listing.save()
    winner = User.objects.get(id=winner_id)
    return render(request, "auctions/result.html", {
        "winner" : winner
    })

def categories(request):
    listings = Listing.objects.all()
    categories = [listing.category for listing in listings]
    print(categories)
    return render(request, "auctions/category.html",{
        "categories": set(categories)
    })

def showcategory(request, category_id):
    listings = Listing.objects.all().filter(category=category_id)
    return render(request, "auctions/showcategory.html",{
        "listings" : listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
