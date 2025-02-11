from django.urls import path

from . import views
from .views import store, product_detail  # Ensure product_detail is imported


urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    
	path('update_item/', views.updateItem, name="update_item"),
    
	path('process_order/', views.processOrder, name="process_order"),
    path('product/<int:id>/', product_detail, name='product'),  # Product detail page

]