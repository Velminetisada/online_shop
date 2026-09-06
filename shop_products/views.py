from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Product, Order


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'shop_products/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'shop_products/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    products = Product.objects.all()

    return render(
        request,
        'shop_products/home.html',
        {'products': products}
    )


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    product = Product.objects.get(id=product_id)

    current_quantity = cart.get(product_id, 0)

    if current_quantity < product.stock:
        cart[product_id] = current_quantity + 1

    request.session['cart'] = cart

    return redirect('home')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        product = Product.objects.get(id=product_id)

        if cart[product_id] < product.stock:
            cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

            total += subtotal

        except Product.DoesNotExist:
            pass

    return render(
        request,
        'shop_products/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


def checkout(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

            total += subtotal

        except Product.DoesNotExist:
            pass

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        Order.objects.create(
            customer_name=customer_name,
            email=email,
            address=address,
            total_amount=total,
        )

        for item in cart_items:
            product = item['product']
            product.stock -= item['quantity']
            product.save()

        request.session['cart'] = {}

        request.session['checkout_total'] = float(total)

        return redirect('payment')

    return render(
        request,
        'shop_products/checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'shop_products/register.html',
                {'error': 'Username already exists.'}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'shop_products/register.html')


def order_history(request):
    orders = Order.objects.all().order_by('-created_at')

    return render(
        request,
        'shop_products/order_history.html',
        {'orders': orders}
    )


def payment(request):
    total = request.session.get('checkout_total', 0)

    if request.method == 'POST':
        return render(
            request,
            'shop_products/payment_success.html',
            {'total': total}
        )

    return render(
        request,
        'shop_products/payment.html',
        {'total': total}
    )