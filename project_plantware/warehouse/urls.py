from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),

    path('product_list/', views.productlist, name='product_list'),
    path('product_add/', views.createProduct, name='product_add'),
    path('product_update/<str:product_id>/', views.UpdateProduct, name='product_update'),
    path('product_delete/<str:product_id>/', views.DeleteProduct, name='product_delete'),

    path('customer/', views.customer, name='customer'),
    path('cus_details/<str:cus_id>/', views.customer_details, name='cus_details'),
    path('cus_order/<str:ord_id>/', views.cus_order, name='cus_order'),

    path('order_view/', views.order_view, name='order_view'),
    path('order_view_delivery/', views.order_delivery_view, name='order_view_delivery'),
    path('order_details/<str:shipping_id>/', views.order_details, name='order_details'),
    path('order_delivery/<str:order_id>/', views.OrderDelivery, name='order_delivery'),
    path('date_order/', views.dateOrder, name='date_order'),

    path('production_list/', views.productionPlan, name='production_list'),
    path('previous_plan/', views.ViewPreviousPlan, name='previous_plan'),
    path('production_new/', views.createProductionPlan, name='production_new'),
    path('production_delete/<str:plan_id>/', views.DeleteproductionPlan, name='production_delete'),
    path('production_done/<str:plan_id>/', views.Doneproductionplan, name='production_done'),

    path('category/', views.category, name='category'),
    path('category_delete/<str:category_id>/', views.delete_category, name='delete_category'),

]
