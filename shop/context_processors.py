from .models import Cart


def cart_context(request):
    """Make cart available in all templates"""
    cart = None
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.items.count()
        except Cart.DoesNotExist:
            pass
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key, user=None)
                cart_count = cart.items.count()
            except Cart.DoesNotExist:
                pass
    
    return {
        'cart': cart,
        'cart_count': cart_count,
    }

