# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:pizza_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:item_id>/', views.remove_cart, name='remove_cart_item'),
    path('create-pizza/', views.create_pizza, name='create_pizza'),
     path("upload/", views.upload_view, name="upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
