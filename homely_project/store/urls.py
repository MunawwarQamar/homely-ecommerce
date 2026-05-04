from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('products/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),

    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('about/', views.about, name='about'),
    path('sales/', views.sales, name='sales'),
    path('all-products/', views.all_products, name='all_products'),
    path('new/', views.new_products, name='new_products'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_products, name='search_products'),

    path('api/products/', views.products_api, name='products_api'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/products/', views.admin_products, name='admin_products'),
    path('admin-dashboard/products/<int:product_id>/edit/', views.admin_edit_product, name='admin_edit_product'),
    path('admin-dashboard/products/<int:product_id>/archive/', views.admin_archive_product, name='admin_archive_product'),
    path('admin-dashboard/products/add/', views.admin_add_product, name='admin_add_product'),
    path('admin-dashboard/messages/', views.admin_messages, name='admin_messages'),
    path('admin-dashboard/messages/<int:message_id>/read/', views.admin_mark_message_read, name='admin_mark_message_read'),
]