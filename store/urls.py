

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # <-- home page
    path('add/<int:id>/', views.add_to_cart, name='add'),
    path('cart/', views.cart_view, name='cart'),
    path('signup/', views.signup, name='signup'),
    path('increase/<int:id>/', views.increase_qty, name='increase'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]


