from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Category, Cart, CartItem, OrderItem, Order
from .forms import ProductForm, LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import (login_required,permission_required)
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db import transaction

def home(request):
    print("delete_product",request.user.has_perm("shop.delete_product"))
    print("user:",request.user)
    print("auth:",request.user.is_authenticated)
    print("staff:",request.user.is_staff)
    print("superuser:",request.user.is_superuser)
    return render(request,"shop/home.html")
def menu_page(request):
    products=Product.objects.all()
    categories=Category.objects.all()
    search=request.GET.get("search")
    category_id=request.GET.get("category")
    sort=request.GET.get("sort")
    paginator=Paginator(products,3)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    if search:
        products=products.filter(name__icontains=search)

    if category_id:
        products=products.filter(category_id=category_id)
    # print(products.query)
    if sort == "price":
        products=products.order_by("price")
    elif sort == "-price":
        products=products.order_by("-price")
    context={
        "products":page_obj,
        "search":search,
        "categories":categories,
        "selected_category":category_id,
        "sort":sort
    }
    return render(request,"shop/menu.html",context)
def about(request):
    return render(request,"shop/about.html")
def contacts(request):
    return render(request,"shop/contacts.html")
def map(request):
    return render(request,"shop/map.html")
def job_application(request):
    return render(request,"shop/job_application.html")
def product_detail(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    context={
        "product":product
    }
    return render(request,"shop/product_detail.html",context)
@login_required
@permission_required("shop.add_product",raise_exception=True)
def add_product(request):

    # if request.method=="POST":
    #     name=request.POST["name"]
    #     price=int(request.POST["price"])
    #     category=request.POST["category"]
    #     rate=float(request.POST["rate"])
    #     available=request.POST.get("category")=="on"
    #     description = request.POST["description"]
    #     stock = int(request.POST["stock"])
    #     Product.objects.create(
    #         name=name,price=price,category=category,rate=rate,available=available, description=description, stock=stock
    #     )
    #     return redirect("menu")
    # return render(request,"shop/add_product.html")
    # if not request.user.has_perm("shop.add_product"):
    #     return HttpResponseForbidden("У вас немає доступу")
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("menu") 
    else:
        form=ProductForm()
    context={"form":form}
    return render(request,"shop/add_product.html",context)
@login_required
@permission_required("shop.change_product",raise_exception=True)
def edit_product(request,product_id):
    # if not request.user.has_perm("shop.change_product"):
    #     return HttpResponseForbidden("У вас немає доступу")
    product=get_object_or_404(Product,id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect ("product_detail", product_id=product.id)
    else:
        form = ProductForm(instance=product)
    context = { "form": form, "product": product }
    return render(request, "shop/edit_product.html", context)
@login_required
@permission_required("shop.delete_product",raise_exception=True)
def delete_product(request,product_id):
    # if not request.user.has_perm("shop.delete_product"):
    #     return HttpResponseForbidden("У вас немає доступу")
    product=get_object_or_404(Product,id=product_id)
    if request.method=="POST":
        product.delete()
        return redirect("menu")
    context={
        "product":product
    }
    return render(request,"shop/delete_product.html",context)
def login_view(request):
    error=None
    next_url=(request.POST.get("next") or request.GET.get("next"))
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None:
                # print("Користувача знайдено",user)
                login(request,user)
                if next_url:
                    return redirect(next_url)
                return redirect("home")
            else:
                error="Неправильний логін або пароль"
    else:
        form=LoginForm()
    context={
        "form":form,
        "error":error,
        "next":next_url
    }
    return render(request,"shop/login.html",context)
def logout_view(request):
    logout(request)
    return redirect("home")
@login_required
def add_to_cart(request,product_id):
    if request.method != "POST":
        return redirect("product_detail",product_id=product_id)        
    product=get_object_or_404(Product,id=product_id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_item,created=CartItem.objects.get_or_create(cart=cart, product=product) 
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    return redirect("product_detail",product_id=product_id)
@login_required
def cart_page(request):
    cart, created=Cart.objects.get_or_create(user=request.user)
    items=cart.items.all()
    total=sum(item.total_price for item in items)
    context={
        "cart":cart,
        "items":items,
        "total":total
    }
    return render(request,"shop/cart.html",context)
@login_required
@require_POST
def increase_cart_item(request,item_id):
    cart=get_object_or_404(Cart,user=request.user)
    cart_item=get_object_or_404(CartItem,id=item_id,cart=cart)
    cart_item.quantity+=1
    cart_item.save()
    return redirect("cart")
@login_required
@require_POST
def decrease_cart_item(request,item_id):
    cart=get_object_or_404(Cart,user=request.user)
    cart_item=get_object_or_404(CartItem,id=item_id,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")
@login_required
@require_POST
def remove_cart_item(request,item_id):
    cart=get_object_or_404(Cart,user=request.user)
    cart_item=get_object_or_404(CartItem,id=item_id,cart=cart)
    cart_item.delete()
    return redirect("cart")
@login_required
@require_POST
def checkout(request):
    cart=get_object_or_404(Cart,user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return redirect("cart")
    with transaction.atomic():
        order=Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
        cart_items.delete()
    return redirect("order_success",order_id=order.id)
@login_required
def order_success(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    return render(request,"shop/order_success.html",{"order":order})
@login_required
def my_orders(request):
    orders=(Order.objects.filter(user=request.user).order_by("-created_at").prefetch_related("items"))
    return render(request,"shop/my_orders.html",{"orders":orders})   
@login_required
def order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id,user=request.user)
    return render(request,"shop/order_detail.html",{"order":order})
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("home")
    else:
        form=UserCreationForm(request.POST)
    return render(request,"shop/register.html",{"form":form})