from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, Category, AuctionListing


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
        # Turn the new data an object
        newListing = AuctionListing(
            category = categoryData,
            title = title,
            price = price,
            description = description,
            year = year,
            imageUrl = image,
            owner = user,
            created_at = time,
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    
def categoryItems(request):
    if request.method == "POST":
        categoryName = request.POST['category']
        category = Category.objects.get(title=categoryName)
        listings = AuctionListing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories        
        })
        
def item(request, name, id):
    if request.method == "GET":
        listing = AuctionListing.objects.get(title=name, pk=id)
        return render(request, "auctions/item.html", {
            "listing": listing
        })
    