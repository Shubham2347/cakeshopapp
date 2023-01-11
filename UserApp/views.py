from django.shortcuts import render,redirect
from AdminApp.models import Category,Product,UserInfo,PaymentMaster
from UserApp.models import MyCart,OrderMaster
from datetime import datetime

# Create your views here.
def homepage(request):
    #Fetch all records from Category table
    cats = Category.objects.all()
    cakes = Product.objects.all()
    
    return render(request,"homepage.html",{"cats":cats,"cakes":cakes})

def login(request):
    if(request.method == "GET"):
        return render(request,"login.html",{})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        try:
            user = UserInfo.objects.get(uname=uname,password=password)
           

        except:
            
            return redirect(login)
        else:
            #Create the session
            request.session["uname"]=uname
            return redirect(homepage)

def signout(request):
    request.session.clear()
    return redirect(homepage)

def signup(request):
    if(request.method == "GET"):
        return render(request,"signup.html",{})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = UserInfo(uname,password,email)
        user.save()
        return redirect(homepage)


def ShowCakes(request,id):    
    #get method returns single object
    id = Category.objects.get(id=id) 
    #filter method returns multiple objects   
    cakes = Product.objects.filter(cat = id)
    cats = Category.objects.all()    
    return render(request,"homepage.html",{"cats":cats,"cakes":cakes})


def ViewDetails(request,id):
    cake = Product.objects.get(id=id)
    return render(request,"ViewDetails.html",{"cake":cake})

def addToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            #Add to cart
            #User and Product
            cakeid = request.POST["cakeid"]
            user = request.session["uname"]
            qty = request.POST["qty"]
            cake = Product.objects.get(id=cakeid)
            user = UserInfo.objects.get(uname = user)
            #check for duplicate entry
            try:
                cart = MyCart.objects.get(cake=cake,user=user)
            except:
                cart = MyCart()
                cart.user = user
                cart.cake = cake
                cart.qty = qty
                cart.save()
            else:
                pass
            return redirect(homepage)
        else:
            return redirect(login)

def ShowAllCartItems(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    if(request.method == "GET"):       
        cartitems = MyCart.objects.filter(user=user)
        total = 0
        for item in cartitems:
            total+= item.qty*item.cake.price
        request.session["total"] = total
        return render(request,"ShowAllCartItems.html",{"items":cartitems})
    else:
        
        id = request.POST["cakeid"]
        cake = Product.objects.get(id=id)
        item = MyCart.objects.get(user=user,cake=cake)            
        qty = request.POST["qty"]
        item.qty = qty
        item.save() #Update
        return redirect(ShowAllCartItems)

def removeItem(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    id = request.POST["cakeid"]
    cake = Product.objects.get(id=id)
    item = MyCart.objects.get(user=user,cake=cake) 
    item.delete()
    return redirect(ShowAllCartItems)

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = PaymentMaster.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            #Its a match
            owner = PaymentMaster.objects.get(cardno='111',cvv='111',expiry='12/2025')
            owner.balance += request.session["total"]
            buyer.balance -=request.session["total"]
            owner.save()
            buyer.save()
            #Delete all items from cart
            uname = request.session["uname"]
            user = UserInfo.objects.get(uname = uname)


            order=OrderMaster()
            order.user=user
            order.amount=request.session['total']
            #order.dateOfOrder=datetime.now()
            # fetchall cart item
            details=""
            items=MyCart.objects.filter(user=user)
            for item in items:
                details+=(item.cake.pname)+","
                item.delete()
            order.details=details
            order.save()
                
            return redirect(homepage)

