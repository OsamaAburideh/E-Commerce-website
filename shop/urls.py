from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
     path('', views.home, name='home'),
     path('product', views.product_list, name='product_list'),
     path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
     path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
     path('accounts/login/', views.signinView, name='signin'),
     path('accounts/create/', views.signupView, name='signup'),
     path('accounts/logout/', views.signoutView, name='signout'),
     path('profile/', views.view_profile, name='view_profile'),
     path('profile/edit', views.edit_profile, name='edit_profile'),
     path('success/', views.success, name='success'),
     path('contact/', views.contact, name='contact'),
     path('change_password/', views.change_password, name='change_password'),
]