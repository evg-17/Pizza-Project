from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("auth", views.auth, name="auth"),
    path("logout", views.logout_view, name="logout"),
    path("<slug:category_slug>/", views.index, name="menu_order"),
    path("<slug:category_slug>/<int:product_id>/cart_add", views.cart_add, name="cart_add"),
    path("<slug:category_slug>/<int:product_id>/<toppings>/cart_add", views.cart_add, name="cart_add"),
    # path("<slug:category_slug>/<int:product_id>/cart_remove", views.cart_remove, name="cart_remove"),
    path("<user_id>/order_create", views.order_create, name="order_create"),
    path("<slug:category_slug>/order_confirm", views.order_confirm, name="order_confirm")
]
