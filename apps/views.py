import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from apps.forms import RegisterForm, User, UpdateProfileForm, ShippingAddressForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.models import Product, Order, OrderItem, ShippingAddress


def index(request):
    # if request.user.is_authenticated:
    #     customer = request.user
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    products = Product.objects.all()
    context = {'obj': products}
    return render(request=request, template_name='apps/store.html', context=context)


def UpdateItem(request):
    """
    Update the quantity of the product in the cart
    :param request: request
    :return: json response

    """
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId : ', productId, 'action:', action)

    user = request.user
    product = Product.objects.get(id=productId)
    order, create = Order.objects.get_or_create(customer=user,complete=False)

    orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def Cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    context = {'items': items, 'order': order}
    return render(request=request, template_name='apps/cart.html', context=context)


def Checkout(request):
    form = ShippingAddressForm()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cars_items']

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        transaction_id = datetime.datetime.now().timestamp()
        if form.is_valid():
            if request.user.is_authenticated:
                customer = request.user
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                total = order.get_cart_total
                order.transaction_id = transaction_id
                order.complete = True
                order.save()


                ShippingAddress.objects.create(customer=customer,
                                               order=order,
                                               address=request.POST['address'],
                                               city=request.POST['city'],
                                               phone=request.POST['phone']
                                               )
                return redirect('main')

    # if request.method == 'GET':
    #     context = {'items': items, 'order': order, 'form': form}
    #     return render(request=request, template_name='apps/checkout.html', context=context)

    context = {'items': items, 'order': order, 'form': form}
    return render(request=request, template_name='apps/checkout.html', context=context)


# class checkout(ListView):
#     form_class = ShippingAddressForm
#     model = ShippingAddress
#     template_name = 'apps/checkout.html'
#
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['User_data'] = User.objects.all()
#         return context


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = 'apps/login.html'

    def get_success_url(self):
        return reverse_lazy('main')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid  login and password')
        return self.render_to_response(self.get_context_data(form=form))


class SingUpView(CreateView):
    form_class = RegisterForm
    template_name = 'apps/registration.html'

    def get_success_url(self):
        return reverse_lazy('login')


# @method_decorator(login_required, name="dispatch")
class PorfileView(ListView):
    model = User
    context_object_name = 'profile'
    template_name = 'apps/profile.html'

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return User.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['User_data'] = User.objects.all()
        return context


class UpdateProfileView(UpdateView):
    model = User
    form_class = UpdateProfileForm
    template_name = 'apps/editprofile.html'

    def get_success_url(self):
        return reverse_lazy('profile')


class Logout(LogoutView):
    template_name = "registration/logged_out.html"


def AboutPageView(request):
    return render(request=request, template_name='apps/aboutpage.html')

def redoc(request):
    return render(request=request, template_name='redoc/redoc.html')
