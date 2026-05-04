from django.http import JsonResponse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, User, Cart, CartItem, ContactMessage
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

def get_logged_in_user(request):
    if 'user_id' not in request.session:
        return None
    return User.objects.filter(id=request.session['user_id']).first()


def admin_required(request):
    user = get_logged_in_user(request)

    if not user:
        messages.error(request, 'Please login first.')
        return None, redirect('/login/')

    if not user.is_admin:
        messages.error(request, 'You are not allowed to access this page.')
        return None, redirect('/')

    return user, None


def calculate_cart_totals(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = Decimal('0.00')

    for item in cart_items:
        item.item_total = item.product.final_price * item.quantity
        subtotal += item.item_total

    tax = subtotal * Decimal('0.10')
    total = subtotal + tax

    return cart_items, subtotal, tax, total


def home(request):
    return render(request, 'home.html')


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_archived=False)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'products.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_archived=False)

    context = {
        'product': product,
    }

    return render(request, 'product_details.html', context)

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
            item.item_total = item.product.final_price * item.quantity
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

        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            request.session['user_is_admin'] = user.is_admin

            messages.success(request, f'Welcome back, {user.first_name}!')

            if user.is_admin:
                return redirect('/admin-dashboard/')

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
            password=make_password(password)
        )

        messages.success(request, 'Your account has been created successfully. Please log in.')
        return redirect('/login/')

    return render(request, 'register.html')


def about(request):
    return render(request, 'about.html')


def sales(request):
    products = Product.objects.filter(discount__gt=0, is_archived=False).order_by('-discount')

    context = {
        'products': products,
    }

    return render(request, 'sales.html', context)


def all_products(request):
    products = Product.objects.filter(is_archived=False).order_by('-created_at')

    context = {
        'products': products,
    }

    return render(request, 'all_products.html', context)

def new_products(request):
    products = Product.objects.filter(is_archived=False).order_by('-created_at')[:8]

    context = {
        'products': products,
    }

    return render(request, 'new_products.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all fields.')
            return redirect('/contact/')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        admin_subject = f'New Contact Message: {subject}'
        admin_message = f"""
You received a new message from Homely Contact Us page.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

        user_subject = 'We received your message - Homely'
        user_message = f"""
Hi {name},

Thank you for contacting Homely.

We received your message and our team will get back to you as soon as possible.

Best regards,
Homely Team
"""

        try:
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('/contact/')

        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, f'Something went wrong: {e}')
            return redirect('/contact/')

    return render(request, 'contact.html')

def search_products(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_archived=False
        ).order_by('-created_at')

    context = {
        'products': products,
        'query': query,
    }

    return render(request, 'search_results.html', context)


def products_api(request):
    products = Product.objects.filter(is_archived=False).order_by('-created_at')
    data = []

    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'category': product.category.name,
            'price': float(product.price),
            'discount': product.discount,
            'final_price': float(product.final_price),
            'stock_quantity': product.stock_quantity,
            'image': product.image,
        })

    return JsonResponse({
        'products': data
    })


def admin_dashboard(request):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    total_products = Product.objects.filter(is_archived=False).count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_categories = Category.objects.count()

    context = {
        'total_products': total_products,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'total_categories': total_categories,
    }

    return render(request, 'admin_dashboard.html', context)


def admin_products(request):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    products = Product.objects.filter(is_archived=False).order_by('-created_at')

    context = {
        'products': products,
    }

    return render(request, 'admin_products.html', context)



def admin_edit_product(request, product_id):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        image = request.FILES.get('image')
        discount = request.POST.get('discount')

        if not category_id or not name or not description or not price or not stock_quantity:
            messages.error(request, 'Please fill in all required fields.')
            return redirect(f'/admin-dashboard/products/{product.id}/edit/')

        product.category = get_object_or_404(Category, id=category_id)
        product.name = name
        product.description = description
        product.price = price
        product.stock_quantity = stock_quantity
        product.discount = discount or 0

        if image:
            product.image = image

        try:
            product.full_clean()
            product.save()

            messages.success(request, 'Product updated successfully.')
            return redirect('/admin-dashboard/products/')

        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect(f'/admin-dashboard/products/{product.id}/edit/')

    context = {
        'product': product,
        'categories': categories,
    }

    return render(request, 'admin_edit_product.html', context)


def admin_add_product(request):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        image = request.FILES.get('image')
        discount = request.POST.get('discount')

        if not category_id or not name or not description or not price or not stock_quantity:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('/admin-dashboard/products/add/')

        try:
            product = Product(
                category=get_object_or_404(Category, id=category_id),
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity,
                image=image,
                discount=discount or 0
            )

            product.full_clean()
            product.save()

            messages.success(request, 'Product added successfully.')
            return redirect('/admin-dashboard/products/')

        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('/admin-dashboard/products/add/')

    context = {
        'categories': categories,
    }

    return render(request, 'admin_add_product.html', context)

def admin_archive_product(request, product_id):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    product = get_object_or_404(Product, id=product_id)
    product.is_archived = True
    product.save()

    messages.success(request, 'Product archived successfully.')
    return redirect('/admin-dashboard/products/')


def admin_messages(request):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    contact_messages = ContactMessage.objects.all().order_by('-created_at')

    context = {
        'contact_messages': contact_messages,
    }

    return render(request, 'admin_messages.html', context)


def admin_mark_message_read(request, message_id):
    user, redirect_response = admin_required(request)
    if redirect_response:
        return redirect_response

    contact_message = get_object_or_404(ContactMessage, id=message_id)
    contact_message.is_read = True
    contact_message.save()

    messages.success(request, 'Message marked as read.')
    return redirect('/admin-dashboard/messages/')