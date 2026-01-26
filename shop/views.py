from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import redirect


from .models import Category, SubCategory, Product, Cart, CartItem, Order, OrderItem


# 🏠 Home page
# 🏠 Home page
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    return render(request, 'shop/index.html', {
        'categories': categories,
        'products': products,
    })

# 📦 Product list
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)

    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'current_category': category_filter,
    })


# 📄 Product detail
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})


# 🛒 Helper: get cart
def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
    return cart


# ➕ Add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('shop:cart_detail')


# 🛒 Cart detail
def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


# 🔄 Update cart
def update_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.GET.get('action')
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('shop:cart_detail')

    item.save()
    return redirect('shop:cart_detail')


# ❌ Remove from cart
def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('shop:cart_detail')


# ✅ Checkout
@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        return redirect('shop:cart_detail')

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_amount=sum(
                item.product.price * item.quantity
                for item in cart.items.all()
            ),
            status="Pending"
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()  # clear cart
        return render(request, "shop/order_success.html", {"order": order})

    return render(request, "shop/checkout.html")

# 💳 Payment
@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'pending':
        return redirect('shop:my_orders')

    if request.method == "POST":
        order.status = 'processing'
        order.save()
        return redirect('shop:payment_success', order_id=order.id)

    return render(request, 'shop/payment.html', {'order': order})

# 🎉 Payment success
@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/payment_success.html', {'order': order})


# 📦 My orders
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'pending':
        messages.error(request, "You cannot cancel this order.")
        return redirect('shop:my_orders')

    order.status = 'cancelled'
    order.save()

    messages.success(request, "Order cancelled successfully.")
    return redirect('shop:my_orders')

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(50, y, f"ShopKart Invoice - Order #{order.id}")
    y -= 40

    p.drawString(50, y, f"Name: {order.first_name} {order.last_name}")
    y -= 20
    p.drawString(50, y, f"Email: {order.email}")
    y -= 20
    p.drawString(50, y, f"Status: {order.status}")
    y -= 30

    p.drawString(50, y, "Items:")
    y -= 20

    for item in order.items.all():
        p.drawString(60, y, f"{item.product.name} x {item.quantity} - ₹{item.subtotal}")
        y -= 20

    y -= 20
    p.drawString(50, y, f"Total Amount: ₹{order.total_amount}")

    p.showPage()
    p.save()
    return response


