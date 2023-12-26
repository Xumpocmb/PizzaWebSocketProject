from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderForm, UserLoginForm, UserRegistrationForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def is_chef(user):
    return user.userprofile.role == 'chef'


@login_required
def orders_list(request):
    context = {
        'room_name': 'orders',
    }
    if request.user.userprofile.role == 'chef':
        orders = Order.objects.filter(is_completed=False)
        context['orders'] = orders
    else:
        orders = Order.objects.all()
        context['orders'] = orders
    return render(request, 'orders/list.html', context)


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'orders/detail.html', {'order': order})

# в файле views.py вашего приложения


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Отправка уведомления в WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'orders',
                {
                    'type': 'orders_update',
                    'order_id': order.id,
                }
            )
            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})


@login_required
@user_passes_test(is_chef)
def process_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        order.is_completed = True
        order.save()

        # Отправка уведомления в WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'orders',
            {
                'type': 'orders_update',
                'order_id': order.id
            }
        )
        return redirect('orders_list')

    return render(request, 'orders/process_order.html', {'order': order})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('profile')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'orders/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            print('registered')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'orders/register.html', context)


@login_required
def profile(request):
    user = request.user
    return render(request, 'orders/profile.html', {'user': user})


def logout(request):
    auth.logout(request)
    return redirect('login')


def index(request):
    return render(request, 'orders/index.html')