"""shop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import orders.views
import shop.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/',include('cart.urls',namespace='cart')),
    path('orders/',include('orders.urls',namespace='orders')),
    path('orderhistory/',orders.views.order_history, name='order_history'),
    path('cancel/<int:order_id>',orders.views.cancel_order, name='cancel_order'),
    path('search/', include('search_app.urls')),
    path('product/',shop.views.product_list, name='product_list'),
    path('account/signup/',shop.views.signupView, name='signup'),
    path('account/login/',shop.views.signinView, name='signin'),
    path('account/logout/',shop.views.signoutView, name='signout'),
    path('profile/', shop.views.view_profile, name='view_profile'),
    path('profile/edit', shop.views.edit_profile, name='edit_profile'),
    path('change_password', shop.views.change_password, name='change_password'),
    path('contact',shop.views.contact, name='contact'),
    path('success',shop.views.success, name='success'),
    path('', include('shop.urls', namespace='shop')),
    path('vouchers/', include('vouchers.urls', namespace='vouchers')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
