from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from accounts.decoraters import unthnticated_user

# create your views
from accounts.models import *
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter
from .decoraters import unthnticated_user,allowed_users,admin_only

@unthnticated_user
def Login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                    login(request,user)
                    return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')

        context = {}
        return render(request,'accounts/login.html',context) 


def Logout(request):
    logout(request)
    return redirect('login')    

@unthnticated_user
def Register(request):
    form = CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account was created for '+username)
            return redirect('login')

    context = {'form':form}
    return render(request,'accounts/register.html',context) 


@login_required(login_url='/login/')
@admin_only
def home(request):
    customer = Customer.objects.all()
    orders = Order.objects.all()
    total_customer = customer.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()


    context = {'customer':customer,'orders':orders,'delivered':delivered,'pending':pending,'total_order':total_order,'total_customer':total_customer}
    return render(request,'accounts/dashboard.html',context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def contact(request,pk_text,*args, **kwargs):
    contact = Customer.objects.get(id=pk_text)
    orders = contact.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'contact':contact,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk,*args,**kwargs):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    contact = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'contact':contact})
    formset = OrderFormSet(instance=contact)
    if request.method == 'POST':
        # print(request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=contact)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk,*args, **kwargs):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print(request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk,*args, **kwargs):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        # print(request.POST)
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context) 


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request, 'accounts/users.html', context)  

# @login_required(login_url='/login/')
# @allowed_users(allowed_roles=['customer'])
def accountsSetting(request):
    context = {}
    return render(request, 'accounts/accounts_settings.html', context)  