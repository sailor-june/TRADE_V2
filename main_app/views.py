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
    profiles = Profile.objects.exclude(user=request.user)
    context = {'profiles': profiles}
    return render(request, 'home.html', context)


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



def view_trade_offer(request, trade_offer_id):
    trade_offer = get_object_or_404(TradeOffer, id=trade_offer_id)
    
    if request.user != trade_offer.receiver:
        return render(request, 'error.html')
    if request.method == 'POST':
        if 'accept' in request.POST:
            # switch items between users
            sender = Profile.objects.get(user=trade_offer.sender)
            sender_inventory = sender.inventory


            receiver = Profile.objects.get(user=trade_offer.receiver)
            receiver_inventory = receiver.inventory
            
            trade_offer.item_to_trade.owner = receiver.user
            trade_offer.item_requested.owner = sender.user
            
            trade_offer.item_to_trade.save()
            trade_offer.item_requested.save()

            receiver_inventory.add(trade_offer.item_to_trade)
            receiver_inventory.remove(trade_offer.item_requested)
            sender_inventory.add(trade_offer.item_requested)
            sender_inventory.remove(trade_offer.item_to_trade)



            # mark trade offer as completed
            trade_offer.accepted = True
            trade_offer.save()

            return redirect('home')
        elif 'decline' in request.POST:
            trade_offer.delete()
            return redirect('home')

    context = {
        'trade_offer': trade_offer
    }
    
    return render(request, 'view_trade_offer.html', context)



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

@login_required
def incoming_trade_offers(request):
    trade_offers = TradeOffer.objects.filter(receiver=request.user, accepted=False)
    context = {'trade_offers': trade_offers}
    return render(request, 'incoming_trade_offers.html', context)