from django.urls import path
from . import views

urlpatterns = [

    path('', views.store, name='store'),
    path('view_item/<str:product_id>/', views.View_item, name='view_item'),
    path('cart/', views.cart, name='cart'),
    path('remove_item/<str:item_id>/', views.Remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),

    path('payment_info/', views.PaymentInfo, name='payment_info'),
    path('process_order/', views.processOrder, name='process_order'),
    path('cancel_order/', views.cancelOrder, name='cancel_order'),


    #profile
    path('cus_profile/', views.ProfilePage, name='cus_profile'),
    path('cus_profile_update/', views.Profile_update, name='profile_update'),

]