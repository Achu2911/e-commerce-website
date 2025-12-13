from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Cart, CartItem, Order, OrderItem


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(featured=True, available=True)[:8]
    categories = Category.objects.all()[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, "shop/index.html", context)


def product_list(request):
    """List all products with filtering and pagination"""
    products = Product.objects.filter(available=True)
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'newest')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, "shop/product_list.html", context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]
    
    cart = get_or_create_cart(request)
    cart_item = None
    if cart:
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            pass

    context = {
        'product': product,
        'related_products': related_products,
        'cart_item': cart_item,
    }
    return render(request, "shop/product_detail.html", context)


def cart_view(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, "shop/cart.html", context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to cart!")
    return redirect('product_detail', slug=product.slug)


def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated!")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from cart!")
    
    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart')


def checkout(request):
    """Checkout page - allows guest checkout"""
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            country=request.POST.get('country', 'India'),
            total_amount=cart.total_price,
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.final_price,
            )
        
        # Clear cart
        cart_items.delete()
        cart.delete()
        
        messages.success(request, f"Order placed successfully! Order ID: #{order.id}")
        return redirect('order_success', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, "shop/checkout.html", context)


def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, "shop/order_success.html", context)


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, "shop/order_history.html", context)