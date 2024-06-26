from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.core.exceptions import ValidationError
from .models import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from .model_annotate import annotate_with_model_name
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
# Create your views here.



def index(request):
    user = request.user
    recent_oils = annotate_with_model_name(Oil.objects.order_by('-id')[:2], 'oil')
    recent_crayfish = annotate_with_model_name(CrayFish.objects.order_by('-id')[:2], 'crayfish')
    recent_catfish = annotate_with_model_name(CatFish.objects.order_by('-id')[:2], 'catfish')
    recent_ponmo_by_kg = annotate_with_model_name(PonmoByKg.objects.order_by('-id')[:2], 'ponmobykg')
    recent_ponmo_by_piece = annotate_with_model_name(PonmoByPiece.objects.order_by('-id')[:2], 'ponmobyiece')
    


    context = {
        'recent_oils': recent_oils,
        'recent_crayfish': recent_crayfish,
        'recent_catfish': recent_catfish,
        'recent_ponmo_by_kg': recent_ponmo_by_kg,
        'recent_ponmo_by_piece': recent_ponmo_by_piece,
        'user': user,
        
    }
    return render(request, 'market/index.html', context)

def error(request):
    return render(request, 'market/error.html')

def annotat_with_model_name(queryset, model_name):
    return [{'model_name': model_name, 'object': item} for item in queryset]

def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        oil_results = annotat_with_model_name(Oil.objects.filter(title__icontains=query), 'oil')
        crayfish_results = annotat_with_model_name(CrayFish.objects.filter(title__icontains=query), 'crayfish')
        catfish_results = annotat_with_model_name(CatFish.objects.filter(title__icontains=query), 'catfish')
        ponmo_by_kg_results = annotat_with_model_name(PonmoByKg.objects.filter(title__icontains=query), 'ponmobykg')
        ponmo_by_piece_results = annotat_with_model_name(PonmoByPiece.objects.filter(title__icontains=query), 'ponmobypiece')

        results = oil_results + crayfish_results + catfish_results + ponmo_by_kg_results + ponmo_by_piece_results

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'market/search_results.html', context)

def set_in_cart_status(items, cart):
    cart_item_ids = set(cart.items.values_list('object_id', flat=True))
    content_type = ContentType.objects.get_for_model(items.first().__class__)
    cart_items = cart.items.filter(content_type=content_type).values_list('object_id', flat=True)
    item_ids_in_cart = set(cart_items)

    for item in items:
        item.in_cart = item.id in item_ids_in_cart

def market(request):
    user = request.user
    recent_oils = annotate_with_model_name(Oil.objects.order_by('-id')[:12], 'oil')
    recent_crayfish = annotate_with_model_name(CrayFish.objects.order_by('-id')[:12], 'crayfish')
    recent_catfish = annotate_with_model_name(CatFish.objects.order_by('-id')[:12], 'catfish')
    recent_ponmo_by_kg = annotate_with_model_name(PonmoByKg.objects.order_by('-id')[:12], 'ponmobykg')
    recent_ponmo_by_piece = annotate_with_model_name(PonmoByPiece.objects.order_by('-id')[:12], 'ponmobypiece')

    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            set_in_cart_status(recent_oils, cart)
            set_in_cart_status(recent_crayfish, cart)
            set_in_cart_status(recent_catfish, cart)
            set_in_cart_status(recent_ponmo_by_kg, cart)
            set_in_cart_status(recent_ponmo_by_piece, cart)

    context = {
        'recent_oils': recent_oils,
        'recent_crayfish': recent_crayfish,
        'recent_catfish': recent_catfish,
        'recent_ponmo_by_kg': recent_ponmo_by_kg,
        'recent_ponmo_by_piece': recent_ponmo_by_piece,
        'user': user
    }
    return render(request, 'market/market.html', context)

def oil_view(request):
    user = request.user 
    oil_data = annotate_with_model_name(Oil.objects.order_by('-id'), 'oil')

    # Paginate the oils queryset
    paginator = Paginator(oil_data, 50)  # Show 50 oils per page

    page_number = request.GET.get('page')
    oils = paginator.get_page(page_number)
    cart_item_ids = set()
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            cart_item_ids = set(cart.items.values_list('object_id', flat=True))
            for oil in oils:
                oil.in_cart = oil.id in cart_item_ids

    context = {
        'oils': oils,
        'user': user,
        'cart_item_ids': cart_item_ids
    }
    return render(request, 'market/oil.html', context)


def crayfish_view(request):
    user = request.user 
    crayfish_data = annotate_with_model_name(CrayFish.objects.order_by('-id'), 'crayfish')

    # Paginate the oils queryset
    paginator = Paginator(crayfish_data, 50)  # Show 50 oils per page

    page_number = request.GET.get('page')
    crayfish = paginator.get_page(page_number)

    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            cart_item_ids = set(cart.items.values_list('object_id', flat=True))
            for fish in crayfish:
                fish.in_cart = fish.id in cart_item_ids

    context = {
        'crayfish_data': crayfish,
        'user': user
    }
    return render(request, 'market/crayfish.html', context)

def update_cart(request, product_type, item_id, quantity):
    content_type = ContentType.objects.get(model=product_type)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, content_type=content_type, object_id=item_id)
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')

def checkout(request):
    return render(request, 'market/checkout.html')

def catfish_view(request):
    user = request.user 
    catfish_data = annotate_with_model_name(CatFish.objects.order_by('-id'), 'catfish')

    # Paginate the oils queryset
    paginator = Paginator(catfish_data, 50)  # Show 50 oils per page

    page_number = request.GET.get('page')
    catfish = paginator.get_page(page_number)
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            cart_item_ids = set(cart.items.values_list('object_id', flat=True))
            for fish in catfish:
                fish.in_cart = fish.id in cart_item_ids

    context = {
        'catfish_data': catfish,
        'user': user
    }
    return render(request, 'market/catfish.html', context)

def ponmo_by_kg_view(request):
    user = request.user
    ponmo_by_kg_data = annotate_with_model_name(PonmoByKg.objects.order_by('-id'), 'ponmobykg')

    # Paginate the oils queryset
    paginator = Paginator(ponmo_by_kg_data, 50)  # Show 50 oils per page

    page_number = request.GET.get('page')
    ponmo_by_kg = paginator.get_page(page_number)
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            cart_item_ids = set(cart.items.values_list('object_id', flat=True))
            for ponmo in ponmo_by_kg:
                ponmo.in_cart = ponmo.id in cart_item_ids

    context = {
        'ponmo_by_kg': ponmo_by_kg,
        'user': user
    }
    return render(request, 'market/ponmo-by-kg.html', context)

def ponmo_by_piece_view(request):
    user = request.user
    ponmo_by_piece_data = annotate_with_model_name(PonmoByPiece.objects.order_by('-id'), 'ponmobypiece')

    # Paginate the oils queryset
    paginator = Paginator(ponmo_by_piece_data, 50)  # Show 50 oils per page

    page_number = request.GET.get('page')
    ponmo_by_piece = paginator.get_page(page_number)
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            cart_item_ids = set(cart.items.values_list('object_id', flat=True))
            for ponmo in ponmo_by_piece:
                ponmo.in_cart = ponmo.id in cart_item_ids

    context = {
        'ponmo_by_piece': ponmo_by_piece,
        'user': user
    }
    return render(request, 'market/ponmo-by-piece.html', context)

def category_detail(request, slug):
    user = request.user
    category = get_object_or_404(MarketCategory, slug=slug)
    subcategories = Subcategory.objects.filter(category=category)

    def oil_pagination():
        oil_data = annotate_with_model_name(Oil.objects.filter(subcategory__in=subcategories), 'oil')

        # Paginate the oils queryset
        paginator = Paginator(oil_data, 50)  # Show 50 oils per page

        page_number = request.GET.get('page')
        oils = paginator.get_page(page_number)
        return oils
    
    def crayfish_pagination():
        crayfish_data =annotate_with_model_name(CrayFish.objects.filter(subcategory__in=subcategories), 'crayfish')
        # Paginate the oils queryset
        paginator = Paginator(crayfish_data, 50)  # Show 50 oils per page

        page_number = request.GET.get('page')
        crayfish = paginator.get_page(page_number)
        return crayfish
    
    def catfish_pagination():
        catfish_data = annotate_with_model_name(CatFish.objects.filter(subcategory__in=subcategories), 'catfish')

        # Paginate the oils queryset
        paginator = Paginator(catfish_data, 50)  # Show 50 oils per page

        page_number = request.GET.get('page')
        catfish = paginator.get_page(page_number)
        return catfish
    
    def ponmo_by_kg_pagination():
        ponmo_by_kg_data = annotate_with_model_name(PonmoByKg.objects.filter(subcategory__in=subcategories), 'ponmobykg')

        # Paginate the oils queryset
        paginator = Paginator(ponmo_by_kg_data, 50)  # Show 50 oils per page

        page_number = request.GET.get('page')
        ponmo_by_kg = paginator.get_page(page_number)
        return ponmo_by_kg
    
    def ponmo_by_piece_pagination():
        ponmo_by_piece_data = annotate_with_model_name(PonmoByPiece.objects.filter(subcategory__in=subcategories), 'ponmobypiece')

        # Paginate the oils queryset
        paginator = Paginator(ponmo_by_piece_data, 50)  # Show 50 oils per page

        page_number = request.GET.get('page')
        ponmo_by_piece = paginator.get_page(page_number)
        return ponmo_by_piece

    
    oils = oil_pagination()
    crayfish = crayfish_pagination()
    catfish = catfish_pagination()
    ponmo_by_kg = ponmo_by_kg_pagination()
    ponmo_by_piece = ponmo_by_piece_pagination()
    
    context = {
        'category': category,
        'oils': oils,
        'crayfish_data': crayfish,
        'catfish_data': catfish,
        'ponmo_by_kg': ponmo_by_kg,
        'ponmo_by_piece': ponmo_by_piece,
        'user': user
    }
    return render(request, 'market/category_detail.html', context)

def add_to_cart(request, product_type, product_id):
    if request.method == 'POST':
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        content_type = ContentType.objects.get(model=product_type)
        product = get_object_or_404(content_type.model_class(), id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, content_type=content_type, object_id=product.id)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def cart_remove_from_cart(request, product_type, item_id):
    if request.method == 'POST':
        content_type = ContentType.objects.get(model=product_type)
        item = get_object_or_404(CartItem, content_type=content_type, object_id=item_id, cart__user=request.user)
        item.delete()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def remove_from_cart(request, product_type, item_id):
    content_type = ContentType.objects.get(model=product_type)
    item = get_object_or_404(CartItem, content_type=content_type, object_id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_cost = sum(item.content_object.price * item.quantity for item in cart_items)
    context = {'cart': cart, 'cart_items': cart_items, 'total_cost': total_cost}
    return render(request, 'market/cart.html', context)


def place_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        return redirect('view_cart')

    total_cost = sum(item.content_object.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_cost)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            content_type=item.content_type,
            object_id=item.object_id,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('order_success')

@login_required
def order_success(request):
    user = request.user
    return render(request, 'market/order-success.html', {'user': user})
def upload(request):
    return render(request, "market/upload.html")

def register(request):
    return render(request, 'market/register.html')

def detail(request, model, id):
    model_class = apps.get_model('afri_food', model)
    product = get_object_or_404(model_class, id=id)
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(model_class), object_id=product.id)

    in_cart = False
    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(
            cart__user=request.user,
            content_type=ContentType.objects.get_for_model(model_class),
            object_id=product.id
        ).exists()

    return render(request, "market/detail.html", {
        "product": product,
        "comments": comments,
        "model_name": model,
        "in_cart": in_cart
    })

import json
def add_comment(request, model, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_message = data.get('comment')
            if not comment_message:
                return JsonResponse({'success': False, 'error': 'Comment message is required'}, status=400)

            model_class = apps.get_model('afri_food', model)
            product = get_object_or_404(model_class, id=id)

            comment = Comment.objects.create(
                content_object=product,
                author=request.user,
                message=comment_message,
            )
            return JsonResponse({'success': True, 'comment': comment.message})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"redirect_url": reverse('index')})
        else:
            return JsonResponse({"error": "Invalid username or password."})
    return render(request, "market/error.html")



def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        phone_number = request.POST["phone_number"]

        if password != confirmation:
            return JsonResponse({"message": "Passwords must match."}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()
        except IntegrityError:
            return JsonResponse({"message": "Username already taken."}, status=400)
        except ValidationError as e:
            return JsonResponse({"message": e.message}, status=400)

        login(request, user)
        return JsonResponse({"redirect": reverse("index")})
    else:
        return render(request, "market/error.html")
    

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('registration/password_reset_done')
    email_template_name = 'registration/password_reset_email.html'

    def form_valid(self, form):
        context = {'email': form.cleaned_data['email']}
        return render(self.request, self.template_name, context)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'market/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('registration/password_reset_complete')


class CustomPasswordResetCompleteView(TemplateView):
    template_name = 'registration/password_reset_complete.html'

