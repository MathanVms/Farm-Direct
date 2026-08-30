from django.urls import path

from . import views


urlpatterns = [

    path("", views.home, name="home"),

    path("products/", views.product_list, name="product_list"),

    path(
        "products/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    path("login/", views.login, name="login"),

    path("register/", views.register, name="register"),

    path("cart/", views.cart, name="cart"),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
    "cart/increase/<int:product_id>/",
    views.increase_cart_quantity,
    name="increase_cart_quantity"
),

path(
    "cart/decrease/<int:product_id>/",
    views.decrease_cart_quantity,
    name="decrease_cart_quantity"
),

    path("checkout/", views.checkout, name="checkout"),

    path("about/", views.about, name="about"),

    path("logout/", views.logout, name="logout"),

    path(
    "order-success/",
    views.order_success,
    name="order_success"
),

    
]