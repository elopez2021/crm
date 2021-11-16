from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory
#It's basically a way for us to create multiple forms within one form

from django.contrib import messages

from django.contrib.auth.decorators import login_required
#this is gonna restrict the user from seeing some page if he isn't logged in, and you set the decorator above the view

from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
#import the form you gonna use here
from .filters import OrderFilter

from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
           
            
            
            messages.success(request, "Account was created for " + username)
            #this shows a message when you're succesfully logged in, and it shows up in the login page
            return redirect('login')

            
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')#these are the input name

        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')#it shows up in the login page
        
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only #it's gonna check if it is a customer or a admin
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    #customers and orders are reffering from the first code
    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending }
    #we are using more values because in the homepage there are 2 tables 

    return render(request, 'accounts/dashboard.html', context)
    #and then we put it after the request

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])#this home page is going to be allowed only for admin users
def userPage(request):
    orders = request.user.customer.order_set.all()#grab all the orders from the customer

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])#this home page is going to be allowed only for admin users
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])#this home page is going to be allowed only for admin users
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})
    #whatever we call in "" is gonna be used in the templates

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])#this home page is going to be allowed only for admin users
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])#this home page is going to be allowed only for admin users
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
    #extra is the fields that are going to be added
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])#this home page is going to be allowed only for admin users
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    #instanc=order is from order above it
    #you use the form as creating because you're only updating the data, it has the same fields

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
            #it is going to be redirected to the homepage

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])#this home page is going to be allowed only for admin users
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)