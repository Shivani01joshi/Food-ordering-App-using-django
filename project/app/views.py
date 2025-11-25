from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login

from .models import Cart, CartItems, Pizza
from .forms import PizzaForm 
# Create your views here.
def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'home.html', {'pizzas': pizzas})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def add_cart(request,pizza_id):
    user=request.user

    pizza = Pizza.objects.get(id=pizza_id)
    cart, _=Cart.objects.get_or_create(user=user,is_paid=False)

    cart_items=CartItems.objects.create(
        cart=cart,
        Pizza=pizza
    )
    return redirect('/')

def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    print(cart,_)
    cart_items = cart.cart_items.all()
    total_amount = sum(item.Pizza.price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
    })

def remove_cart(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

def create_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PizzaForm()
    return render(request, 'pizza_form.html', {'form': form})