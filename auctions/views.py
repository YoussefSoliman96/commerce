from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, Category, AuctionListing, Comment, Bid


def index(request):
    listings = AuctionListing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories        
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

def createListing(request):
    if request.method == "GET":
        # Get all categories and show forms
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {
           "categories": categories
        })
    else:
        # Submit all data of the new listing
        category = request.POST['category']
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']
        year = request.POST['year']
        image = request.POST['imageurl']
        time = datetime.datetime.now()
        
        # Select the user
        user = request.user
        categoryData = Category.objects.get(title=category)
        
        newBid = Bid(
            bid = price,
            user = user,
        )
        newBid.save()
        # Turn the new data an object
        newListing = AuctionListing(
            category = categoryData,
            title = title,
            price = newBid,
            description = description,
            year = year,
            imageUrl = image,
            owner = user,
            created_at = time,
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    
def categoryItems(request):
    categories = Category.objects.all()
    if request.method == "POST":
        try:
            categoryName = request.POST['category']
            category = Category.objects.get(title=categoryName)
        except:
            listings = AuctionListing.objects.all()
            return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories        
        })
            
        listings = AuctionListing.objects.filter(active=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories        
        })
        
def allCategoryItems(request):
    listings = AuctionListing.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/all.html", {
        "listings": listings,
        "categories": categories        
    })

def item(request, name, id):
    listing = AuctionListing.objects.get(title=name, pk=id)
    watchlistStatus = request.user in listing.watchlist.all()
    listingComments = Comment.objects.filter(item=listing) 
    owner = listing.owner
    currentUser = request.user
    if owner.username == currentUser.username:
        itemOwner = True
    else:
        itemOwner = False
    return render(request, "auctions/item.html", {
        "listing": listing,
        "watchlistStatus": watchlistStatus,
        "comments":listingComments,
        "itemOwner": itemOwner
    })
        
def watchlistRemoved(request, name, id):
    listing = AuctionListing.objects.get(title=name, pk=id)
    user = request.user
    listing.watchlist.remove(user)
    itemWatchlist = user.userWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": itemWatchlist,
        "watchListItemRemoved": f"{listing} removed from Watchlist"
    })
    
def watchlistAdded(request, name, id):
    listing = AuctionListing.objects.get(title=name, pk=id)
    user = request.user
    listing.watchlist.add(user) 
    return HttpResponseRedirect(reverse("item", args=(name, id, )))

def watchlist(request):
    user = request.user
    itemWatchlist = user.userWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": itemWatchlist,
    })
    
def comment(request, id, name):
    user= request.user
    listing = AuctionListing.objects.get(title=name, pk=id)
    listingComment = request.POST['comment']
    
    newComment = Comment(
        writer = user,
        item = listing,
        listingComment = listingComment,
    )   
    newComment.save()
    return HttpResponseRedirect(reverse("item", args=(name, id, )))

def bid(request, id, name):
    user= request.user
    listing = AuctionListing.objects.get(title=name, pk=id)
    watchlistStatus = request.user in listing.watchlist.all()
    listingComments = Comment.objects.filter(item=listing) 
    owner = listing.owner
    currentUser = request.user
    if owner.username == currentUser.username:
        itemOwner = True
    else:
        itemOwner = False
    listingBid = request.POST['bid']
    if float(listingBid) > listing.price.bid:
        newBid = Bid(
            bid = listingBid,
            user = user,
        )
        newBid.save()
        listing.price = newBid
        listing.save()
        return render(request, "auctions/item.html", {
            "listing":listing,
            "alert":"Bid submitted successfully",
            "status": "success",
            "watchlistStatus": watchlistStatus,
            "comments":listingComments,
            "itemOwner": itemOwner,
            
        })
    else:
        return render(request, "auctions/item.html", {
            "listing":listing,
            "alert":"Bidding failed",
            "status": "fail",
            "watchlistStatus": watchlistStatus,
            "comments":listingComments,
            "itemOwner": itemOwner,
            })
        
def closeAuction(request, id, name):
    listing = AuctionListing.objects.get(title=name, pk=id)
    watchlistStatus = request.user in listing.watchlist.all()
    listingComments = Comment.objects.filter(item=listing) 
    listing.active = False
    listing.save()
    owner = listing.owner
    currentUser = request.user
    if owner.username == currentUser.username:
        itemOwner = True
    else:
        itemOwner = False
    return render(request, "auctions/item.html", {
            "listing":listing,
            "status": "success",
            "watchlistStatus": watchlistStatus,
            "comments":listingComments,
            "itemOwner": itemOwner,
            "auctionClosedMessage": "Auction closed successfully!"           
            })
    
def repost(request, id, name):
    listing = AuctionListing.objects.get(title=name, pk=id)
    watchlistStatus = request.user in listing.watchlist.all()
    listingComments = Comment.objects.filter(item=listing) 
    listing.active = True
    listing.save()
    owner = listing.owner
    currentUser = request.user
    if owner.username == currentUser.username:
        itemOwner = True
    else:
        itemOwner = False
    return render(request, "auctions/item.html", {
            "listing":listing,
            "status": "success",
            "watchlistStatus": watchlistStatus,
            "comments":listingComments,
            "itemOwner": itemOwner,
            "auctionClosedMessage": "Auction reposted successfully!"           
            })
    
def allCategories(request):
    categories = Category.objects.all()
    if request.method == "POST":
        try:
            categoryName = request.POST['category']
            category = Category.objects.get(title=categoryName)
        except:
            listings = AuctionListing.objects.all()
            return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories        
        })
            
        listings = AuctionListing.objects.filter(active=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories        
        })
    else:
        return render(request, "auctions/allCategories.html", {
            "categories": categories   
            })