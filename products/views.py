from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Product, Category, CartItem , Order
from .models import Product


def home(request):
    return render(request, "products/home.html")


def product_list(request):
    products = Product.objects.all()

    search_query = request.GET.get("search", "")
    selected_category = request.GET.get("category", "")

    if search_query:
        products = products.filter(
            name__icontains=search_query
        )

    if selected_category:
        products = products.filter(
            category_id=selected_category
        )

    categories = Category.objects.all()

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "search_query": search_query,
            "selected_category": selected_category,
        }
    )

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(
        request,
        "products/product_detail.html",
        {"product": product}
    )


def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            return redirect("home")

        return render(
            request,
            "products/login.html",
            {"error": "Invalid email or password."}
        )

    return render(request, "products/login.html")


def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(
                request,
                "products/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=email).exists():

            return render(
                request,
                "products/register.html",
                {"error": "An account with this email already exists."}
            )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        return redirect("login")

    return render(request, "products/register.html")


def cart(request):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    subtotal = 0

    for item in cart_items:
        item.item_total = item.product.price * item.quantity
        subtotal += item.item_total

    return render(
        request,
        "products/cart.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "total": subtotal,
        }
    )


def checkout(request):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    subtotal = 0

    for item in cart_items:
        item.item_total = item.product.price * item.quantity
        subtotal += item.item_total

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")

        Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            payment_method="Cash on Delivery",
            total_amount=subtotal
        )

        cart_items.delete()

        return redirect("order_success")

    return render(
        request,
        "products/checkout.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "total": subtotal,
        }
    )


def about(request):
    return render(request, "products/about.html")

def logout(request):
    auth_logout(request)

    return redirect("home")

def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

def increase_cart_quantity(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        user=request.user,
        product_id=product_id
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


def decrease_cart_quantity(request, product_id):

    if not request.user.is_authenticated:
        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        user=request.user,
        product_id=product_id
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")

def order_success(request):
    return render(
        request,
        "products/order_success.html"
    )