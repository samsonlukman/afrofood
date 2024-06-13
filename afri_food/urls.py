from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("market/", views.market, name='market'),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("upload", views.upload, name="upload"),
    path("register", views.register, name="register"),
    path('product/<str:model>/<int:id>/', views.detail, name='product_detail'), 
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('cart/', views.view_cart, name='cart_view'),
    path('cart/add/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:product_type>/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('update_cart/<str:product_type>/<int:item_id>/<int:quantity>/', views.update_cart, name='update_cart'),
    path('oils/', views.oil_view, name='oils'),
    path('checkout/', views.checkout, name='checkout'),
    path('crayfish/', views.crayfish_view, name='crayfish'),
    path('catfish/', views.catfish_view, name='catfish'),
    path('ponmo_by_kg/', views.ponmo_by_kg_view, name='ponmo_by_kg'),
    path('ponmo_by_piece/', views.ponmo_by_piece_view, name='ponmo_by_piece'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
]
