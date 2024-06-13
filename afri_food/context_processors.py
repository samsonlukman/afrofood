from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        cart_item_count = 0
    return {
        'cart_item_count': cart_item_count
    }
