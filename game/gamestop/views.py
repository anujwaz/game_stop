from django.shortcuts import render, HttpResponse, redirect
from gamestop.models import Product, Cart, Orders, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
import random


# Create your views here.



def index(request):
    
    return render(request, 'index.html')

def create_product(request):
    
    if request.method == 'GET':
    
     return render(request, 'createproduct.html')
    
    else:
        name = request.POST['name']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']
        image = request.FILES['image']
        
        
        p = Product.objects.create(name = name, description = description, manufacturer = manufacturer, category = category,
                               quantity = quantity, price = price, image = image)
        
        p.save()
        
        return redirect('/read_product')
    

def read_product(request):
    
    p = Product.objects.all()    

    context = {}
    
    context['data'] = p
    
    return render(request, 'read_product.html', context)


def user_register(request):
    
    if request.method == "GET":
        return render(request, 'register.html')
    
    else:
        
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            
            u = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)
            
            u.set_password(password)
            
            u.save()
            
            return redirect("/login")
        
        
        else:
            
            context = {}
            
            context['error'] = "Password and confirm password does not match"
            
            return render(request, 'register.html', context)
        
        
def user_login(request):
    
    if request.method == "GET":
        return render(request, 'login.html')
    
    else:
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            
            login(request, user)
            
            return redirect('/')
        
        
        else:
            
            context = {}
            
            context['error'] = 'Username and password is incorrect'
            
            return render(request, 'login.html', context)
        
        
def user_logout(request):
    
    logout(request)
    
    return redirect("/")


@login_required(login_url='/login')
def create_cart(request, rid):
    
    prod = Product.objects.get(id = rid)
    
    cart = Cart.objects.filter(product = prod, user = request.user).exists()
    
    if cart:
        
        return redirect('/read_cart')
    
    else:
    
        user = User.objects.get(username = request.user)  
        
        total_price = prod.price 
        
        c = Cart.objects.create(product = prod, user = user, quantity = 1, total_price = total_price)  
        
        c.save()
        
        return redirect('/read_cart')
    
    
@login_required(login_url='/login')
def read_cart(request):
    
    cart = Cart.objects.filter(user = request.user)

    context = {}
    
    context['data'] = cart
    
    total_quantity = 0
    
    total_price = 0
    
    for x in cart:
        
        total_quantity += x.quantity
        total_price += x.total_price
        

    context['total_quantity'] = total_quantity
    context['total_price'] = total_price
    
    return render(request, 'readcart.html', context)


@login_required(login_url='/login')
def delete_cart(request, rid):
    
    cart = Cart.objects.filter(id = rid)        

    cart.delete()

    return redirect('/read_cart')

def update_cart(request, rid, q):
    
    cart = Cart.objects.filter(id = rid)
    
    c = Cart.objects.get(id = rid)
    
    
    price = int(c.product.price)*int(q)
    
    cart.update(quantity = q, total_price = price)
    
    return redirect('/read_cart')


def create_order(request, rid):
    
    cart = Cart.objects.get(id = rid)
    
    order = Orders.objects.create(product = cart.product, user = request.user,
                                  quantity = cart.quantity, price = cart.total_price)
    
    
    order.save()
    
    cart.delete()
    
    return redirect('/read_cart')    


def read_orders(request):
    
    order = Orders.objects.filter(user = request.user)
    
    context = {}
    
    context['data'] = order
    
    return render(request, 'readorder.html', context)

def create_review(request, rid):
    
   prod = Product.objects.get(id = rid)
   
   rev = Review.objects.filter(user = request.user, product = prod).exists()
   
   if rev:
       
       return HttpResponse("Review already added")
   
   else:
            if request.method == "GET":
        
             return render(request, 'create_review.html')
    
            else:
                
                title = request.POST['title']
                content = request.POST['content']
                rating = request.POST['rate']
                image = request.FILES['image']
                
                product = Product.objects.get(id = rid)
                
                review = Review.objects.create(product = product, user = request.user, title = title,
                                            content = content, rating = rating, image = image)
                
                review.save()
                
                return HttpResponse("/")
            
            
def read_product_detail(request, rid):
    
    prod = Product.objects.filter(id = rid)
    
    p = Product.objects.get(id = rid)
    
    n = Review.objects.filter(product = p).count()
    
    rev = Review.objects.filter(product = p)
    
    sum = 0
    
    for x in rev:
        
        sum += x.rating
        
        
    avg_r = sum/n
    avg = int(sum/n)
    
    context = {}
    
    context['data'] = prod
    
    context['avg_rating'] = avg
    context['avg'] = avg_r        
        
    
    return render(request, 'readproductdetails.html', context) 

def forgot_password(request):
    
    if request.method == "GET":
        
        return render(request, 'forgot_password.html')     
    else:
        
        email = request.POST['email']
        
        request.session['email'] = email
        
        user = User.objects.filter(email = email).exists()
        
        if user:
        
            otp = random.randint(1000, 9999)
            
            request.session['otp'] = otp
            
            with get_connection(
                
                
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS
            ) as connection :
                
                subject = "opt verification"
                email_from = settings.EMAIL_HOST_USER
                reciption_list = [ email ]
                message = f"otp is {otp}"
                
                EmailMessage(subject, message, email_from, reciption_list,
                            connection= connection).send()
            
            return redirect("/otp_verification")
        
        else:
            
            context = {}
            
            context['error'] = 'user does not exist'
            
            return render(request, 'forgot_password.html', context)
    
    
def opt_verification(request):
    
    if request.method == "GET":
        
        return render(request, 'otp.html')
    
    else:
        
        otp = int(request.POST['otp'])
        
        email_otp = int(request.session['otp'])
        
        if otp == email_otp:
            
            return redirect("/new_password")
        else:
            
            return HttpResponse("not ok")
        
def new_password(request):
    
    if request.method == "GET":
        
        return render(request, 'newpassword.html')
    
    else:
        
        email = request.session['email']
    
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = User.objects.get(email = email)
        
        if password == confirm_password:
            
            user.set_password(password)
            
            user.save()
            
            return redirect("/login")
        
        else:
            
            context = {}
            
            context['error'] = "Password and confirm password does not match"
            
            return render(request, 'newpassword.html', context)
            
                    
                

    
    

        

    
    


