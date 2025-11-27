from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login

from .s3_upload import upload_to_s3

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
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def upload_view(request):
    print("UPLOAD VIEW HIT")

    if request.method == "POST":
        try:
            print("FILES:", request.FILES)
            file = request.FILES["file"]
            print("FILE RECEIVED:", file.name)
            url = upload_to_s3(file, file.name)

            print("UPLOAD SUCCESS:", url)
            return JsonResponse({"file_url": url})
        
        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "upload.html")

from django.shortcuts import render

# Create your views here.

import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UploadImage(APIView):
    def post(self, request):
        file = request.FILES.get("image")
        print(file)
        if not file:
            return Response({"error": "No file provided"}, status=400)

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        print("s3",s3)
        file_path = f"uploads/{file.name}"
        print("file path",file_path)
        try:
            s3.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_path,
                ExtraArgs={
                    "ContentType": file.content_type,
                    #"ACL": "public-read"
                }
            )

            url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_path}"
            print(url)
            return Response({"message": "Uploaded", "url": url}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

