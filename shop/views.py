import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from .models import *
from shop.forms import ChocolateForm
from django.conf import settings
from django.views import generic
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from mailjet_rest import Client


class home(TemplateView):
    template_name = 'home.html'


# Function to handle chop categories and search bar function
def shop(request):
    chocolates = Chocolate.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            chocolates = chocolates.filter(
                category__chocolate_type__in=categories)
            categories = Category.objects.filter(chocolate_type__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Chocolate does not exist!")
                return redirect(reverse('shop'))
            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            chocolates = chocolates.filter(queries)

    context = {
        'chocolates': chocolates,
        'search_term': query,
        'current_categories': categories,
    }
    return render(request, 'shop/shop.html', context)


# Function to handle basket
def basket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponse('Available for other users')
        buyer, created = Buyer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        items = order.orderitem_set.all()
        basketItems = order.get_basket_items
    else:
        try:
            basket = json.loads(request.COOKIES['basket'])
        except Exception:
            basket = {}
            print('Basket:', basket)
        items = []
        order = {
            'get_basket_total': 0,
            'get_basket_items': 0,
            'shipping': False,
        }
        for item in basket:
            try:
                chocolate = Chocolate.objects.get(id=item)
                order['get_basket_total'] += chocolate.price*basket[
                    item]['quantity']
                order['get_basket_items'] += basket[item]['quantity']
                item = {
                    "chocolate": {
                        "id": chocolate.id,
                        "name": chocolate.name,
                        "price": chocolate.price,
                        "imageURL": chocolate.imageURL,
                    },
                    "quantity": basket[item]["quantity"],
                    "get_total": chocolate.price*basket[item]['quantity']
                }
                items.append(item)
            except Exception:
                pass
        basketItems = order['get_basket_items']
        print(items)
    context = {
        'items': items,
        'order': order,
        'basketItems': basketItems,
        "user": request.user, "show": len(items) > 0}
    return render(request, 'shop/basket.html', context)


# Function that stores shipping Information and order
def checkout(request):
    address = request.GET['address']
    city = request.GET['city']
    state = request.GET['state']
    zipcode = request.GET['zipcode']
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponse('Available for other users')
        buyer = request.user.buyer
        email = request.GET["email"]
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        items = order.orderitem_set.all()
        sending_address = SendingAddress(
            user=request.user,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            date_added=datetime.datetime.now()

        )
        sending_address.order = order
        sending_address.save()
        basketItems = order.get_basket_items
        context = {
            'items': items,
            'order': order,
            'basketItems': basketItems,
            'email': email,
            'order_id': order.id
        }
    else:
        items = []
        order = {
            'get_basket_total': 0,
            'get_basket_items': 0,
            'shipping': False,
        }
        email = request.GET["email"]
        basketItems = order['get_basket_items']
        try:
            basket = json.loads(request.COOKIES['basket'])
        except Exception:
            basket = {}

        for item in basket:
            try:
                chocolate = Chocolate.objects.get(id=item)
                order['get_basket_total'] += chocolate.price*basket[
                    item]['quantity']
                order['get_basket_items'] += basket[item]['quantity']
                item = {
                    "chocolate": {
                        "id": chocolate.id,
                        "name": chocolate.name,
                        "price": chocolate.price,
                        "imageURL": chocolate.imageURL,
                    },
                    "quantity": basket[item]["quantity"],
                    "get_total": chocolate.price*basket[item]['quantity']
                }
                items.append(item)
            except Exception:
                pass
        order_object = Order.objects.create(buyer=None, complete=False)
        for item in items:
            chocolate_object = Chocolate.objects.get(
                id=item['chocolate']['id'])
            order_item = OrderItem.objects.create(
                chocolate=chocolate_object,
                order=order_object,
                quantity=item['quantity']
            )
            order_item.save()

        sending_address = SendingAddress(
            user=None,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            date_added=datetime.datetime.now()

        )
        basketItems = order_object.get_basket_items
        sending_address.order = order_object
        sending_address.save()

        context = {
            'items': items,
            'order': order,
            'basketItems': basketItems,
            'total': order['get_basket_total'],
            'email': email,
            'order_id': order_object.id}
    return render(request, 'shop/checkout.html', context)


# Function to add and remove products from the basket
def updateItem(request):
    if request.user.is_superuser:
        return HttpResponse('Available for other users')
    data = json.loads(request.body)
    chocolateId = data['chocolateId']
    action = data['action']

    print('Action', action)
    print('chocolateId', chocolateId)

    buyer = request.user.buyer
    chocolate = Chocolate.objects.get(id=chocolateId)
    order, created = Order.objects.get_or_create(buyer=buyer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, chocolate=chocolate)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    if request.user.is_superuser:
        return HttpResponse('Available for other users')
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_basket_total:
            order.complete = True
        order.save()

        if order.shipping:
            SendingAddress.objects.create(
                buyer=buyer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],

            )

    else:
        print('You are not logged in.')
    return JsonResponse('You paid !', safe=False)


def chocolate_page(request, id):
    chocolate = Chocolate.objects.filter(id=id).first()

    context = {
        'chocolate': chocolate,
    }

    return render(request, 'shop/chocolate_page.html', context)


# Superuser - access to delete chocolate
class DeleteProductView(DeleteView):
    model = Chocolate
    template_name = 'delete_chocolate.html'
    success_url = reverse_lazy('shop')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponse('You do not have access to delete product!')
        return super().dispatch(request, *args, **kwargs)


# Superuser - access to add chocolate
@login_required
def add_product(request):
    chocolate_form = ChocolateForm(request.POST, request.FILES)
    user = get_object_or_404(User, username=request.user.username)
    if not request.user.is_superuser:
        return HttpResponse('You do not have access to add new product!')
    if request.method == "POST":
        if chocolate_form.is_valid():
            form = chocolate_form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, "chocolate added")
            return redirect("shop")
        else:
            print(chocolate_form.errors)
    template = 'add_chocolate.html'
    context = {
            'chocolate_form': chocolate_form,
        }
    return render(request, template, context)


# Superuser - access to edit chocolate
@login_required
def edit_product(request, pk):
    chocolate = get_object_or_404(Chocolate, id=pk)
    chocolate_form = ChocolateForm(request.POST, request.FILES)
    user = get_object_or_404(User, username=request.user.username)
    if not request.user.is_superuser:
        return HttpResponse('You do not have access to edit product!')
    if request.method == "POST":
        if chocolate_form.is_valid():
            form = ChocolateForm(
                request.POST, request.FILES, instance=chocolate)
            if form.is_valid():
                form.save()
                messages.success(request, "edited")
                return redirect(reverse('chocolate_page', args=[chocolate.id]))
    else:
        form = ChocolateForm(instance=chocolate)
        messages.error(request, f'youre updating {chocolate.name}')

    template = 'edit_chocolate.html'
    context = {
            'form': form,
            'chocolate': chocolate,
        }
    return render(request, template, context)


# Stripe settings
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateCheckoutSessionView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return HttpResponse('You do not have access')
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        host = self.request.get_host()
        if self.request.user.is_authenticated:
            order_id = self.request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            email = self.request.POST.get("email")

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'unit_amount': int(100 * order.get_basket_total),
                            'product_data': {
                                'name': order.id,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_email=email,
                success_url="http://{}{}".format(
                    host, reverse('payment-success')),
                cancel_url="http://{}{}".format(
                    host, reverse('payment-cancel')),

            )
        else:
            order_id = self.request.POST.get('order_id')
            order_total = self.request.POST.get('order_total')
            email = self.request.POST.get("email")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'unit_amount': int(100 * float(order_total)),
                            'product_data': {
                                'name': order_id,

                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_email=email,
                success_url="http://{}{}".format(
                    host, reverse('payment-success')),
                cancel_url="http://{}{}".format(
                    host, reverse('payment-cancel')),

            )
        return redirect(checkout_session.url, code=303)


def paymentSuccess(request):
    if request.user.is_authenticated:
        order = request.user.buyer.order_set.get(complete=False)
        order.complete = True
        order.save()
        order_id = order.id
    else:
        order = Order.objects.filter(buyer=None, complete=False).last()
        order.complete = True
        order.save()
        order_id = order.id
    email = stripe.checkout.Session.list(
        limit=1)["data"][0]["customer_details"]["email"]
    name = stripe.checkout.Session.list(
        limit=1)["data"][0]["customer_details"]["name"]
    print(email, name)
    API_KEY = settings.API_KEY
    API_SECRET = settings.API_SECRET
    mailjet = Client(auth=(API_KEY, API_SECRET))
    data = {
        "FromEmail": settings.EMAIL,
        "FromName": "Art Of Chocolate Shop",
        "Subject": "Order Confirmation",
        "Text-part":
        f"Dear {name}, your order number {order_id} has been confirmed.",
        "Recipients": [
            {
                "Email": email
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    context = {
        'payment_status': 'success',
        'order_id': order_id,
        'email': email
    }
    return render(request, 'shop/confirmation.html', context)


def paymentCancel(request):
    context = {
        'payment_status': 'cancel'
    }
    return render(request, 'shop/confirmation.html', context)


# Stripe Webhooks
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == "paid":
            line_item = session.list_line_items(session.id, limit=1).data[0]
            order_id = line_item['description']
            fulfill_order(order_id)

    return HttpResponse(status=200)


def fulfill_order(order_id):
    order = Order.objects.get(id=order_id)
    order.ordered = Trueorder.orderDate = datetime.datetime.now()
    order.save()

    for item in order.items.all():
        product_var = ProductVariation.objects.get(id=item.product.id)
        product_var.stock -= item.quantity
        product_var.save()
