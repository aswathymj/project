from django.urls import path, include
from django.contrib import admin
from myapp.views import user_login, register, index, admin_view, technician_view, user_view, logout_view, add_category, accessories, view_category, delete_category, add_subcategory, view_subcategory,edit_category,edit_subcategory,delete_subcategory,add_product,view_product,edit_product,delete_product,get_subcategories,product_detail,category_products,add_to_cart,view_cart,update_cart,remove_from_cart,buy_now,payment_detail,update_user_details,create_paypal_payment, execute_paypal_payment, payment_cancelled, create_payment,verify_payment
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('admin_view/', admin_view, name='admin_view'),
    path('user_view/', user_view, name='user_view'),
    path('technician_view/', technician_view, name='technician_view'),
    path('add_category/', add_category, name='add_category'),
    path('view_category/', view_category, name='view_category'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('add_subcategory/', add_subcategory, name='add_subcategory'),
    path('view_subcategory/', view_subcategory, name='view_subcategory'),
    path('add_product/', add_product, name='add_product'),
    path('view_product/', view_product, name='view_product'),
    path('accessories/', accessories, name='accessories'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('edit_category/<int:category_id>/', edit_category, name='edit_category'),
    path('edit-subcategory/<int:id>/', edit_subcategory, name='edit_subcategory'),
    path('delete-subcategory/<int:id>/', delete_subcategory, name='delete_subcategory'),
    path('products/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('get-subcategories/', get_subcategories, name='get_subcategories'),
       path('product/<int:product_id>/', product_detail, name='product_detail'),
      path('category/<int:category_id>/', category_products, name='category_products'),
       path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
        path('cart/', view_cart, name='view_cart'),
         path('cart/update/<int:item_id>/',update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
     path('buy_now/<int:cart_id>/', buy_now, name='buy_now'),
    path('payment_detail/<int:payment_id>/',payment_detail, name='payment_detail'),
     path('update_user_details/', update_user_details, name='update_user_details'),
     path('create_paypal_payment/', create_paypal_payment, name='create_paypal_payment'),
    path('paypal_execute/', execute_paypal_payment, name='paypal_execute'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),

    
    path('create-payment/', create_payment, name='create_payment'),
    path('verify-payment/', verify_payment, name='verify_payment'),
]
