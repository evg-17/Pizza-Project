from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Category, Product, Dish, Order, OrderItem, Topping
from .cart import Cart

# Create your views here.
def index(request, category_slug=None):
    # category = None
    # some_var = request.POST.getlist('check-top')
    cart = Cart(request)
    print(cart)
    context = {
        "categories": Category.objects.all()
    }
    if category_slug:
        context = {
            "categories": Category.objects.all(),
            "category": get_object_or_404(Category, slug=category_slug),
            "dishes": Dish.objects.filter(category__slug=category_slug),
            "products_small": Product.objects.select_related("dish").filter(dish__category__slug=category_slug, size__name="small"),
            "products_large": Product.objects.select_related("dish").filter(dish__category__slug=category_slug, size__name="large"),
            "products_unsized": Product.objects.select_related("dish").filter(dish__category__slug=category_slug, size__name=""),
            "toppings": Topping.objects.all(),
            "cart": cart
        }
        # category = get_object_or_404(Category, slug=category_slug)

    return render(request, "orders/index.html", context)

def login_view(request):
    return render(request, "orders/login.html")

def auth(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("orders:index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("orders:index"))

#@require_POST
def cart_add(request, category_slug, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    toppings = []
    if request.POST.getlist("check-top"):
        for topping in request.POST.getlist("check-top"):
            toppings.append(topping)
    print(toppings)
    cart.add(product, toppings)

    return redirect("orders:menu_order", category_slug=category_slug)

# def cart_remove(request, category_slug, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect("orders:menu_order", category_slug=category_slug)

def order_confirm(request, category_slug):
    cart = Cart(request)
    return render(request, "orders/confirmation.html", {"cart": cart})

def order_create(request, user_id):
    cart = Cart(request)
    user = User.objects.get(id=user_id)
    order = Order.objects.create(user=user, completed=False)
    for item in cart:
        OrderItem.objects.create(order=order,
                                 product=item["product"],
                                 price=item["price"],
                                 quantity=item["quantity"])
    # clear the cart
    cart.clear()
    return redirect("orders:index")
