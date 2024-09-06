from django.urls import path, include
from django.contrib import admin
from myapp.views import  chatbot_view,create_order,razorpay_webhook, get_expected_rate, manage_terms_and_conditions, submit_terms, terms_and_conditions, service_request_success, create_service_request, get_subcategory, get_models, get_complaints, user_login, register, index, admin_view, technician_view, user_view, logout_view, add_category, accessories, view_category, delete_category, add_subcategory, view_subcategory,edit_category,edit_subcategory,delete_subcategory,add_product,view_product,edit_product,delete_product,get_subcategories,product_detail,category_products,add_to_cart,view_cart,update_cart,remove_from_cart,buy_now,payment_detail,update_user_details,create_paypal_payment, execute_paypal_payment, payment_cancelled, create_payment,verify_payment,update_payment_status,paid_users,technician_dashboard,manage_technicians,approve_technician,reject_technician,add_phcategory,phone_category_list,edit_phcategory,delete_phcategory,add_phsubcategory,list_phsubcategories,edit_phsubcategory,delete_phsubcategory,add_phone_model,view_phone_models,delete_phone_model,edit_phone_model,add_complaint,complaint_list,delete_complaint,edit_complaint,forgot_password,reset_password,download_qualification,repair_view,repair_status,phone_category_view,get_service_request_data,update_service_request,service_requests
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

    path('update-payment-status/', update_payment_status, name='update_payment_status'),
    path('create-payment/', create_payment, name='create_payment'),
    path('verify-payment/', verify_payment, name='verify_payment'),
    path('paid_users/',paid_users, name='paid_users'),
    
     path('technician/dashboard/', technician_dashboard, name='technician_dashboard'),
     path('manage-technicians/', manage_technicians, name='manage_technicians'),
    path('approve-technician/<int:user_id>/', approve_technician, name='approve_technician'),
    path('reject-technician/<int:user_id>/', reject_technician, name='reject_technician'),
     path('add_phcategory/', add_phcategory, name='add_phcategory'),
     path('categories/', phone_category_list, name='phone_category_list'),
      path('categories/<int:category_id>/edit/', edit_phcategory, name='edit_phcategory'),
      path('categories/<int:category_id>/delete/', delete_phcategory, name='delete_phcategory'),
       path('add-phsubcategory/', add_phsubcategory, name='add_phsubcategory'),
         path('phsubcategories/', list_phsubcategories, name='list_phsubcategories'),
         path('edit_phsubcategory/<int:subcategory_id>/', edit_phsubcategory, name='edit_phsubcategory'),
          path('delete_phsubcategory/<int:subcategory_id>/', delete_phsubcategory, name='delete_phsubcategory'),
            path('add/', add_phone_model, name='add_phone_model'),
            path('view/', view_phone_models, name='view_phone_models'),
               path('delete_phone_model/<int:model_id>/', delete_phone_model, name='delete_phone_model'),
                  path('edit_phone_model/<int:model_id>/', edit_phone_model, name='edit_phone_model'),
                      path('complaints/add/', add_complaint, name='add_complaint'),
                      path('complaints/',complaint_list, name='complaint_list'),
                       path('complaints/delete/<int:complaint_id>/',delete_complaint, name='delete_complaint'),
                        path('complaints/edit/<int:complaint_id>/',edit_complaint, name='edit_complaint'),
                      path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/',reset_password, name='reset_password'),
     path('download-qualification/<int:user_id>/', download_qualification, name='download_qualification'),
      path('repair/',repair_view, name='repair'),
    path('repair_status/',repair_status , name='repair_status'),
     path('repair/', phone_category_view, name='phone_category_view'),
      path('get_subcategory/', get_subcategory, name='get_subcategory'),
    path('get_models/', get_models, name='get_models'),
    path('get_complaints/', get_complaints, name='get_complaints'),
    path('create-service-request/', create_service_request, name='create_service_request'),
    path('service-request-success/', service_request_success, name='service_request_success'),  # This should be created
     path('get_service_request_data/<int:service_request_id>/', get_service_request_data, name='get_service_request_data'),
    path('update_service_request/', update_service_request, name='update_service_request'),
    path('service-requests/', service_requests, name='service_requests'),
    path('terms-and-conditions/', terms_and_conditions, name='terms_and_conditions'),
     path('submit-terms/', submit_terms, name='submit-terms'),
    path('manage-terms-and-conditions/', manage_terms_and_conditions, name='manage_terms_and_conditions'),
     path('get_expected_rate/', get_expected_rate, name='get_expected_rate'),
     path('webhook/', razorpay_webhook, name='razorpay_webhook'),
     path('create-order/<int:id>/', create_order, name='create_order'),
      path('chatbot/', chatbot_view, name='chatbot'),
     
     

]


