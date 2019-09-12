from django.shortcuts import render,HttpResponseRedirect
from django.db.models import Q
from django.contrib import auth
from django.contrib.messages import success,error
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.db import models

#from Eshop.paytm import checksum
from MainApp.models import *
from MainApp.forms import *
from Eshop import settings


def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = ' it  means a lot to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )

def Home(request):
    if(request.method=='POST'):
        sr=request.POST.get('search')
        data=Product.objects.filter(Q(name__icontains=sr))
    else:
        data=Product.objects.all()
    return render(request,"index.html",{"Data":data})

def dispatch_email(request,data):

    subject = 'Order Dispached'
    message = 'Dear '+data.order_address.chname+',\n       Your Product is being dispatched for our side and will reached soon.\nAt address: \n'+data.order_address.address+"\n"+data.order_address.pin
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

def Shop(request,cn):

    if(cn=="sample"):
        data=Product.objects.all()
    else:
        data=Product.objects.filter(cat__cname=cn)
    return render(request,"shop.html",{"Data":data})


def ProductDetails(request,num):
    data=Product.objects.get(id=num)
    if (request.method == 'POST'):
        form = CartForm(request.POST)
        q = request.POST['count']
        if (form.is_valid()):
            f = form.save(commit=False)
            f.cart_user = request.user
            f.cart_product = data
            f.count = q
            f.total = int(data.price) * float(q)
            f.save()
            return HttpResponseRedirect('/cart/')
    else:
        form = CartForm()
    return render(request, 'product-details.html', {
        "Data": data,
        "Form": form
    })
@login_required(login_url='/login/')
def CartDelete(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.delete()
    data=Cart.objects.filter(cart_user=request.user)
    t = 0
    for i in data:
        t = t + i.cart_product.price * i.count
    return render(request, "cart.html", {"Data": data,"Total":t})


@login_required(login_url='/login/')
def CartDetails(request):
    data=Cart.objects.filter(cart_user=request.user)
    t=0
    for i in data:
        t=t+i.cart_product.price*i.count
    return render(request,"cart.html",{"Data":data,"Total":t})

def Checkout(request):
    return render(request,"checkout.html")

def Login(request):
    if(request.method=='POST'):
        uname=request.POST.get('uname')
        pward=request.POST.get('pward')
        user=auth.authenticate(username=uname,password=pward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/adminpage/')
            else:
                return HttpResponseRedirect('/shop/sample/')
        else:
            error(request,"Invalid User")
    return render(request,"login.html")

def SignUp(request):
    if(request.method=='POST'):
        uname=request.POST.get('uname')
        try:
            match=User.objects.get(username=uname)
            if(match):
                error(request,"UserName Already Exist")
        except:
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            email = request.POST.get('email')
            pward = request.POST.get('pward')
            cpward = request.POST.get('cpward')
            if(pward==cpward):
                User.objects.create_user(username=uname,
                                     first_name=fname,
                                     last_name=lname,
                                     email=email,
                                     password=pward
                                     )
                success(request,"Account is created")
                email_send(request,email,uname)
                #client=nexmo.Client(key='e73bdaec',secret='m1pF0Yg5cNGxWmQh')
                #client.send_message({
                #    'from':'Nexmo',
                #    'to':'+919873848046',
                #    'text':'hello',
                #})
                return HttpResponseRedirect('/login/')
            else:
                error(request,"Password and Confirm Password not Matched")
    return render(request,"signup.html")

@login_required(login_url='/login/')
def AddProduct(request):

    if(request.method=='POST'):
        try:
            data=Product()
            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')

            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = int(bp - (bp * d / 100))
            data.color = request.POST.get('color')
            data.img1 = request.FILES.get('img1')
            data.img2 = request.FILES.get('img2')
            data.img3 = request.FILES.get('img3')
            data.img4 = request.FILES.get('img4')
            data.save()
            success(request, 'Product Inserted')
            return HttpResponseRedirect('/addproduct/')
        except:
            error(request, "Invalid Record")
        return render(request, "addproduct.html")


@login_required(login_url='/login/')
def AdminPage(request):
    data=Product.objects.all()
    return render(request,"admin.html",{"Data":data})

def logout(request):
    auth.logout(request)
    return render(request,'index.html')

def DeleteProduct(request,num):
    data=Product.objects.get(id=num)
    data.delete()
    data = Product.objects.filter(size__sname='all')
    return render(request,"admins.html",{"Data":data})

@login_required(login_url='/login/')
def OrderPlaced(request):
    data=Order.objects.filter(order_user=request.user)
    return render(request,"orderplace.html",{"Data":data})
@login_required(login_url='/login/')
def editProduct(request,num):
    data=Product.objects.get(id=num)
    if (request.method == 'POST'):
        try:

            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')
            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = bp - bp * d / 100
            data.color = request.POST.get('color')
            data.save()
            success(request, 'Product Edited')
            data = Product.objects.get(id=num)
        except:
            error(request, "Invalid Record")
    return render(request,"edit.html",{"Data":data})




MERCHANT_KEY='sample'
@login_required(login_url='/login/')
def CheckoutForm(request):
    data = Cart.objects.filter(cart_user=request.user)
    t = 0
    for i in data:
        t = t + i.cart_product.price * i.count
    if(request.method=='POST'):
        check = Checkout()
        check.chname = request.POST.get('name')
        check.mobile = request.POST.get('mobile')
        check.email = request.POST.get('email')
        check.state = request.POST.get('state')
        check.city = request.POST.get('city')
        check.address = request.POST.get('address')
        check.pin = request.POST.get('pin')
        choice = request.POST.get('choice')
        if(choice=='COD'):
            check.save()
            return HttpResponseRedirect('/orderplace/')
    return render(request,"checkout.html",{"Total":t})


















@login_required(login_url='/login/')
def OrderAdmin(request):
    data=Order.objects.all()
    return render(request,'adminorder.html',{"Data":data})
@login_required(login_url='/register/')
def PastOrders(request):
    data=Order.objects.filter(order_user=request.user)
    return render(request,"pastorders.html",{"Data":data})

@login_required(login_url='/register/')
def PastOrders2(request):
    data=PreviousOrder.objects.filter(order_user=request.user)
    return render(request,"pastorders.html",{"Data":data})

def OrderPlaced(request):
     return render(request,"orderplaced.html")
@login_required(login_url='/login/')
def DispatchedOrder(request,num):

    data = Order.objects.get(ordernumber=num)
    p = PreviousOrder()
    p.ordernumber = data.ordernumber
    p.order_user = data.order_user
    p.order_product = data.order_product
    p.count=data.count
    p.order_address = data.order_address
    print(p.count)
    p.save()
    dispatch_email(request,data)
    data.delete()
    data=Order.objects.all()
    return render(request,'orderadmin.html',{"Data":data})

