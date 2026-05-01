from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart'),

]