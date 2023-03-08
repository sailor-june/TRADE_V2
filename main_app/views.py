from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import InventoryForm, TradeOfferForm
from .models import Profile, Item, TradeOffer, User


def home(request):
    return render(request, "home.html")


@login_required
def view_profile(request, username):
    other_user = get_object_or_404(User, username=username)
    other_profile = get_object_or_404(Profile, user=other_user)
    other_items = Item.objects.filter(owner=other_user)
    trade_offers = TradeOffer.objects.filter(sender=request.user, receiver=other_user)

    if request.method == "POST":
        form = TradeOfferForm(request.POST, user=request.user)
        if form.is_valid():
            trade_offer = form.save(commit=False)
            trade_offer.sender = request.user
            trade_offer.receiver = other_user
            if "item_requested" in request.POST:
                trade_offer.item_requested = Item.objects.get(
                    pk=request.POST["item_requested"]
                )
            trade_offer.save()
            messages.success(request, "Trade offer sent!")
            return redirect("view_profile", username=username)
    context = {
        "user": other_user,
        "profile": other_profile,
        "trade_offers": trade_offers,
    }
    return render(request, "view_profile.html", context)


@login_required
def remove_item(request, item_id):
    profile = Profile.objects.get(user=request.user)
    inventory = profile.inventory

    for i, item in enumerate(inventory):
        if item["id"] == item_id:
            inventory.pop(i)
            profile.save()
            break

    return redirect("inventory")


@login_required
def inventory(request):
    profile = Profile.objects.get(user=request.user)
    inventory = profile.inventory

    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data["item_id"]
            item_name = form.cleaned_data["item_name"]
            inventory.append({"id": item_id, "name": item_name})
            profile.save()
            return redirect("inventory")
    else:
        form = InventoryForm()

    return render(request, "inventory.html", {"inventory": inventory, "form": form})


@login_required
def inventory_view(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, "inventory.html", {"items": items})


@login_required
def add_item(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            item_name = form.cleaned_data["item_name"]
            item = Item.objects.create(name=item_name, owner=request.user)
            messages.success(request, "Item added to inventory!")
            return redirect("inventory")
    else:
        form = InventoryForm()
    return render(request, "add_item.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)
            return redirect("profile")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {"profile": profile})


def send_trade_offer(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    user_inventory = Item.objects.filter(owner=request.user)
    return render(request, 'confirm_trade_offer.html', {'item': item, 'inventory':user_inventory})

# @login_required
# def trade_confirmation(request, item_id):
#     item = get_object_or_404(Item, item_id=item_id)
#     if request.method == 'POST':
#         # create and save TradeOffer object
#         trade_offer = TradeOffer(
#             sender=request.user,
#             receiver=item.owner,
#             item_to_trade=item,
#             item_requested=item_requested,
#             message=request.POST.get('message')
#         )
#         trade_offer.save()

#         # update trade offer with selected item to trade
#         item_to_trade_id = request.POST.get('item_to_trade')
#         item_to_trade = get_object_or_404(Item, item_id=item_to_trade_id)
#         trade_offer.item_to_trade = item_to_trade
#         trade_offer.save()

#         # confirm trade
#         messages.success(request, 'Trade offer sent!')
#         return redirect('home')
#     else:
#         return render(request, 'confirm_trade_offer.html', {'item': item, 'inventory': request.user.profile.get_inventory_items()})
def trade_confirmation(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    inventory = Item.objects.filter(owner=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        item_to_trade = get_object_or_404(Item, item_id=request.POST.get('item_to_trade'))  
        item_requested = item
    
        trade_offer = TradeOffer.objects.create(
            sender=request.user,
            receiver=item.owner,
            item_to_trade=item_to_trade,
            item_requested=item_requested,
            message=message
        )
        messages.success(request, 'Trade offer sent!')
        return redirect('home')
    else:
        form = TradeOfferForm()
    return render(request, 'confirm_trade_offer.html', {'form': form, 'inventory': inventory, 'item': item})
