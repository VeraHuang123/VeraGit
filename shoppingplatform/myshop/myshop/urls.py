"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from user.views import UsersView,UsersDetailView,Login,CustomersView,CustomersDetailView
from product.views import product_router
from cart.views import CartsView,CartsAddView,CartsDetailView,CartsDeleteView
from order.views import OrdersAddView,OrdersDetailView,OrdersView,BCOrdersView,BCOrdersDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/users',UsersView.as_view()),
    path('api/v1/users/<int:user_id>',UsersDetailView.as_view()),
    path('api/v1/login',Login.as_view()),
    path("api/v1/",include(product_router.urls)),
    path("api/v1/cart",CartsView.as_view()),
    path("api/v1/cart/<int:user_id>/<int:product_id>",CartsAddView.as_view()),
    path("api/v1/cart/<int:user_id>",CartsDetailView.as_view()),
    path("api/v1/cart/delete/<int:cart_id>",CartsDeleteView.as_view()),
    path("api/v1/order",OrdersView.as_view()),
    path("api/v1/order/<int:cart_id>",OrdersAddView.as_view()),
    path("api/v1/order/<int:order_id>/", OrdersDetailView.as_view()),

    path("customers/",CustomersView.as_view()),
    path("customers/<int:customer_id>",CustomersDetailView.as_view()),
    path("bcorders/",BCOrdersView.as_view()),
    path("bcorders/<int:order_id>",BCOrdersDetailView.as_view())

]
