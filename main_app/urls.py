from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path("inventory/",views.inventory_view, name='inventory'),
    path("add_item/",views.add_item,name="add_item"),
    path('trade/<int:item_id>/', views.send_trade_offer, name='send_offer'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('trade/confirm/<int:item_id>', views.trade_confirmation, name='confirm_trade_offer'),
    path('tradeoffer/<int:trade_offer_id>/', views.view_trade_offer, name='view_trade_offer'),
    path('incoming-trade-offers/', views.incoming_trade_offers, name='incoming_trade_offers'),

]