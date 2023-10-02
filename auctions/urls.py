from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createListing, name="createlisting"),
    path("categoryitems", views.categoryItems, name="categoryitems"),
    path("item/<str:name>&<int:id>", views.item, name="item"),
    path("watchlistRemoved/<str:name>&<int:id>", views.watchlistRemoved, name="watchlistRemoved"),
    path("watchlistAdded/<str:name>&<int:id>", views.watchlistAdded, name="watchlistAdded"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<str:name>&<int:id>", views.comment, name="comment"),
    path("bid/<str:name>&<int:id>", views.bid, name="bid"),
    path("closeAuction/<str:name>&<int:id>", views.closeAuction, name="closeAuction"),
]   
