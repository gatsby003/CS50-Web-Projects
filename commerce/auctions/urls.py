from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowatchlist/<int:listing_id>", views.add_to_watchlist, name="addtowatchlist"),
    path("removefromwatchlist/<int:listing_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("activelisting/<int:listing_id>", views.active_listing, name="activelisting"),
    path("placebid", views.place_bid, name="placebid"),
    path("closeauction/<int:listing_id>", views.close_auction, name="closeauction"),
    path("result/<int:listing_id>", views.showresult, name="resultpage"),
    path("categories", views.categories, name='category'),
    path("categories/<str:category_id>", views.showcategory, name="showcategory")
]
