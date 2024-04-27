from django.core.mail import send_mail
from django.db.models import Q, Subquery
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import ColdCoffee
import razorpay
from django.db import IntegrityError
from .forms import CoffeePaymentForm,ProductForm
from .models import SignUpData, Product, Owners, Contact,ForgotPassword,cart, Cartmultipe
from django.conf import settings
from django.db.models import F
from django.contrib import messages
# Create your views here.
def home(request):
    productlist = Product.objects.all()
    return render(request,'index.html',{"productlist":productlist})

def dogs(request):
    productlist = Product.objects.filter(category='Dog')
    return render(request, 'mainpages/dogs.html', {"productlist": productlist})


def cats(request):
    productlist = Product.objects.filter(category='Cat')
    return render(request, 'mainpages/cats.html', {"productlist": productlist})

def birds(request):
    productlist = Product.objects.filter(category='Bird')
    return render(request, 'mainpages/birds.html', {"productlist": productlist})

def fishes(request):
    productlist = Product.objects.filter(category='Fish')
    return render(request,'mainpages/fishes.html',{"productlist": productlist})

def rabbits(request):
    productlist = Product.objects.filter(category='Rabbit')
    return render(request,'mainpages/rabbits.html',{"productlist": productlist})

def gunniepigs(request):
    productlist = Product.objects.filter(category='Gunniepig')
    return render(request,'mainpages/gunniepigs.html',{"productlist": productlist})

def shelters(request):
    productlist = Product.objects.filter(category='Shelters')
    return render(request, 'mainpages/shelters.html',{"productlist": productlist})

def medicines(request):
    productlist = Product.objects.filter(category='Medicines')
    return render(request, 'mainpages/medicines.html',{"productlist": productlist})
def login(request):
    return render(request,'signup.html');

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        emailid = request.POST['email']
        pwd=request.POST['pass']
        flag = SignUpData.objects.filter(sign_email=emailid).first()
        if flag:
            message = "Email already exists!"
            return render(request, "signup.html", {'message': message})
        signobj = SignUpData(sign_name=name,sign_email=emailid,sign_password=pwd)
        SignUpData.save(signobj)
        message = "Successfully Signed up!"
        return render(request,"signup.html",{'message':message})
    return render(request,"signup.html")

def checkuserlogin(request):
    emailid=request.POST["logemail"]
    pwd=request.POST["logpass"]
    flag=SignUpData.objects.filter(Q(sign_email=emailid) & Q(sign_password=pwd))
    flag1 = Owners.objects.filter(Q(email=emailid) & Q(password=pwd))
    if flag1:
        admin = Owners.objects.get(email=emailid)
        usersdata = SignUpData.objects.all()
        userscount = SignUpData.objects.count()
        request.session["emailid"] = admin.email
        request.session["uname"] = admin.username
        return render(request, "owner.html",{"uname": admin.username,"users": usersdata,"count":userscount})
    else:
        if flag:
            user = SignUpData.objects.get(sign_email=emailid)
            request.session["uname"] = user.sign_name
            request.session["email"] = user.sign_email
            return render(request, "index.html", {"uname": user.sign_name,"user":user})
        else:
            message = 'Incorrect password (or) user not found! Signup'
            return render(request,"signup.html",{"message":message})

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = SignUpData.objects.filter(sign_email=email).first()
        if user:
            subject = "Request to change the password"
            reset_link = "http://127.0.0.1:8000/changepassword"
            message = f"Click the following link to reset your password: {reset_link}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            return HttpResponse("<h1 align=center>Mail sent Successfully</h1>")
        else:
            error_message = "User not found. Please enter a valid email address."
            return render(request, "forgotpassword.html", {"error_message": error_message})
    return render(request, "forgotpassword.html")

def logout(request):
    request.session.flush()
    return redirect('login')

def ownerpage(request):
    usersdata = SignUpData.objects.all()
    userscount = SignUpData.objects.count()
    return render(request, "owner.html", {"users": usersdata,"count":userscount})

def deleteuser(request,uid):
    SignUpData.objects.filter(id=uid).delete()
    return redirect("owner")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def rescue(request):
    return render(request,"rescue.html")
def addproduct(request):
    form = ProductForm()
    if request.method == "POST":
        formdata = ProductForm(request.POST,request.FILES)
        if formdata.is_valid():
            formdata.save()
            msg="Product Added Successfully"
            return render(request, "addproduct.html", {"productform": form,"msg":msg})
        else:
            msg = "Failed to Add Product"
            return render(request, "addproduct.html", {"productform": form, "msg": msg})
    return render(request,"addproduct.html",{"productform":form})

def temp(request):
    return render(request,"temp.html")

def viewproductsinowner(request):
    mail=request.session["emailid"]
    flag1 = Owners.objects.filter(Q(email=mail))
    p = Owners.objects.filter(email=mail)
    if flag1:
        key = p[0].secure_key
    # productlist = Product.objects.filter(secure_key=key)
    # count = Product.objects.filter(secure_key=key).count()
        productlist = Product.objects.all()
        count = Product.objects.count()
        return render(request,"viewproductsinowner.html",{"productlist":productlist,"count":count})
    else:
        message = 'Resered for owners!'
        return render(request, "signup.html", {"message": message})

def deleteproduct(request,uid):
    Product.objects.filter(id=uid).delete()
    return redirect("viewproductsinowner")

def userlogout(request):
    request.session.flush()
    return render(request,"index.html")

def changepassword(request):
    return render(request,"changepassword.html")

def contact(request):
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname = request.POST['lastname']
        comment = request.POST['comment']
        email = request.POST['email']
        subject=""
        comment1=comment+"This is my Suggestion. Kindly improve if possible"
        data=Contact(firstname=firstname,lastname=lastname,comment=comment,email=email)
        data.save()
        send_mail(
            subject,
            comment1,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        return HttpResponse("<h1 align=center>Mail sent Successfully</h1>")
    return render(request,"contact.html")

def getcategory(request,id):
    pro=Product.objects.filter(category=id)
    return render(request,"category.html",{"pro":pro})


from django.core.exceptions import ObjectDoesNotExist


def add_cart(request):
    try:
        user = request.session.get("email")  # Use get() method to avoid KeyError
        if not user:
            raise ValueError("User email is not found in the session")

        prid_str = request.POST.get("pid", "")  # Get pid from POST data
        if not prid_str.isdigit():
            raise ValueError("Invalid value for pid")

        prid = int(prid_str)
        print(prid)

        try:
            # Check if the product is already in the cart
            cart_item = Cartmultipe.objects.get(mail=user, pid=prid)
            # If the product is already in the cart, increment its quantity
            cart_item.quantity = F('quantity') + 1
            cart_item.save()
            message = "Quantity updated in the cart successfully"
        except ObjectDoesNotExist:
            # If the product is not in the cart, add it with quantity 1
            cart_obj = Cartmultipe(mail=user, pid=prid, quantity=1)
            cart_obj.save()
            message = "Product added to cart successfully"
    except (ValueError, ObjectDoesNotExist) as e:
        message = str(e)

    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER'))


def get_cart(request):
    user = request.session["email"]
    pro=Cartmultipe.objects.filter(mail=user)
    pcount = Cartmultipe.objects.filter(mail=user).count()
    products = Product.objects.filter(id__in=Subquery(pro.values('pid')))
    total = sum([Product.price for Product in products])
    return render(request, "cart.html", {"pro": products,"count":pcount,"price":total})

def update_cart(request):
    if request.method == 'POST':
        user = request.session["email"]
        prid = int(request.POST.get("pid"))
        quantity = int(request.POST.get("quantity"))
        cart_item = Cartmultipe.objects.filter(mail=user, pid=prid).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantity updated successfully")
        else:
            messages.error(request, "Product not found in the cart")
    return redirect(request.META.get('HTTP_REFERER'))  # Redirect to your cart page


def deletecartproduct(request,uid):
    Cartmultipe.objects.filter(pid=uid).delete()
    return redirect("getcart")
def clearcartafterpayment(request):
    user = request.session["email"]
    cart.objects.filter(mail=user).delete()
    return redirect("home")

def payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount'))*100
        client = razorpay.Client(auth=('rzp_test_2bjpZJK2gF38qx','bkv1WSfxBXki5HVNge6Ny7Wz'))
        response_payment=client.order.create(dict(
            amount=amount,
            currency='INR'
        ))
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == 'created':
            cold_coffee = ColdCoffee(name=name,amount=amount,order_id=order_id)
            cold_coffee.save()
            response_payment['name']=name
            form=CoffeePaymentForm(request.POST or None)
            return render(request,'payment.html',{'form':form,'payment':response_payment})

    form=CoffeePaymentForm()
    return render(request,'payment.html',{'form':form})

@csrf_exempt
def payment_status(request):
    response = request.POST
    dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    client=razorpay.Client(auth=('rzp_test_2bjpZJK2gF38qx','bkv1WSfxBXki5HVNge6Ny7Wz'))
    try:
        status=client.utility.verify_payment_signature(dict)
        cold_coffee=ColdCoffee.objects.get(order_id=response['razorpay_order_id'])
        cold_coffee.razorpay_payment_id=response['razorpay_payment_id']
        cold_coffee.paid=True
        cold_coffee.save()
        return render(request,"payment_status.html",{'status':True})
    except:
        return render(request,'payment_status.html',{'status':False})