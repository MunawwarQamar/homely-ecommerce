from django.http import JsonResponse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, User, Cart, CartItem

def calculate_cart_totals(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = Decimal('0.00')

    for item in cart_items:
        item.item_total = item.product.final_price * item.quantity
        subtotal += item.item_total

    tax = subtotal * Decimal('0.10')
    total = subtotal + tax

    return cart_items, subtotal, tax, total

def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You need to log in first.')
        return redirect('/login/')

    user = get_object_or_404(User, id=request.session['user_id'])
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=user)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)

    messages.success(request, 'Product added to cart successfully.')
    return redirect(f'/product/{product.id}/')

def remove_from_cart(request, item_id):
    if 'user_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'You need to log in first.'}, status=401)

    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()

    cart_items, subtotal, tax, total = calculate_cart_totals(cart)

    return JsonResponse({
        'success': True,
        'subtotal': str(subtotal),
        'tax': str(tax),
        'total': str(total),
    })


def update_cart_item(request, item_id, action):
    if 'user_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'You need to log in first.'}, status=401)

    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()

    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

    cart_items, subtotal, tax, total = calculate_cart_totals(cart)
    item_total = cart_item.product.final_price * cart_item.quantity

    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'item_total': str(item_total),
        'subtotal': str(subtotal),
        'tax': str(tax),
        'total': str(total),
    })


def home(request):
    return render(request, 'home.html')


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'product_details.html', context)



def cart(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You need to log in first.')
        return redirect('/login/')

    user = get_object_or_404(User, id=request.session['user_id'])
    cart = Cart.objects.filter(user=user).first()

    cart_items = []
    subtotal = Decimal('0.00')

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            item.item_total = item.product.price * item.quantity
            subtotal += item.item_total

    tax = subtotal * Decimal('0.10')
    total = subtotal + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }

    return render(request, 'cart.html', context)
def login_view(request):
    if 'user_id' in request.session:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('/login/')

        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('/')

        messages.error(request, 'Invalid email or password.')
        return redirect('/login/')

    return render(request, 'login.html')

def logout_view(request):
    request.session.clear()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/login/')

def register(request):
    if 'user_id' in request.session:
        return redirect('/')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not first_name or not last_name or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return redirect('/register/')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('/register/')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('/register/')

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        messages.success(request, 'Your account has been created successfully. Please log in.')
        return redirect('/login/')

    return render(request, 'register.html')
def about(request):
    return render(request, 'about.html')

def sales(request):
    products = Product.objects.filter(discount__gt=0).order_by('-discount')

    context = {
        'products': products,
    }

    return render(request, 'sales.html', context)
