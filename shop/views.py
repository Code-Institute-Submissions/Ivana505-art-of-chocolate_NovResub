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
import sendgrid
from sendgrid.helpers.mail import Mail


class home(TemplateView):
    template_name = 'home.html'


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
                order['get_basket_total'] += chocolate.price*basket[item]['quantity']
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
    context = {'items': items, 'order': order, 'basketItems': basketItems, "user": request.user, "show": len(items) > 0}
    return render(request, 'shop/basket.html', context)


def checkout(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponse('Available for other users')
        buyer = request.user.buyer
        email = request.GET["email"]
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        items = order.orderitem_set.all()
        basketItems = order.get_basket_items
        context = {
            'items': items,
            'order': order,
            'basketItems': basketItems,
            'email': email
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
                order['get_basket_total'] += chocolate.price*basket[item]['quantity']
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

        context = {'items': items, 'order': order, 'basketItems': basketItems, 'total': order['get_basket_total'], 'email': email}
    return render(request, 'shop/checkout.html', context)


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


class DeleteProductView(DeleteView):
    model = Chocolate
    template_name = 'delete_chocolate.html'
    success_url = reverse_lazy('shop')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponse('You do not have access')
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_product(request):
    # add the request.FILES
    chocolate_form = ChocolateForm(request.POST, request.FILES)
    user = get_object_or_404(User, username=request.user.username)
    if not request.user.is_superuser:
        return HttpResponse('You do not have access')
    if request.method == "POST":
        if chocolate_form.is_valid():
            # save the form but do not commit
            form = chocolate_form.save(commit=False)
            # attach the arthur after
            form.author = request.user
            # save the form
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


@login_required
def edit_product(request, pk):
    # add the request.FILES
    chocolate = get_object_or_404(Chocolate, id=pk)
    chocolate_form = ChocolateForm(request.POST, request.FILES)
    user = get_object_or_404(User, username=request.user.username)
    if not request.user.is_superuser:
        return HttpResponse('You do not have access')
    if request.method == "POST":
        if chocolate_form.is_valid():
            # save the form but do not commit
            form = ChocolateForm(
                request.POST, request.FILES, instance=chocolate)
            # attach the arthur after
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


# This is your test secret API key.
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
                #   success_url='https://8000-ivana505-artofchocolate-grr6ik0bz9k.ws-eu73.gitpod.io/payment-success/',
                #   cancel_url='https://8000-ivana505-artofchocolate-grr6ik0bz9k.ws-eu73.gitpod.io/payment-cancel/',
            )
        else:
            order_total = self.request.POST.get('order_total')
            email = self.request.POST.get("email")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'unit_amount': int(100 * float(order_total)),
                            'product_data': {
                                'name': 'Your order will be generated when purchased',
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
                #   success_url='https://8000-ivana505-artofchocolate-grr6ik0bz9k.ws-eu73.gitpod.io/payment-success/',
                #   cancel_url='https://8000-ivana505-artofchocolate-grr6ik0bz9k.ws-eu7..gitpod.io/payment-cancel/',
            )
        return redirect(checkout_session.url, code=303)


def paymentSuccess(request):
    if request.user.is_authenticated:
        order = request.user.buyer.order_set.get(complete=False)
        order.complete = True
        order.save()
        order_id = order.id
    else:
        order_id = "anonymous"
    email = stripe.checkout.Session.list(limit=1)["data"][0]["customer_details"]["email"]
    name = stripe.checkout.Session.list(limit=1)["data"][0]["customer_details"]["name"]
    print(email, name)
    SENDGRID_API_KEY = ''
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    message = Mail(
        from_email='',
        to_emails=email,
        subject="Order Confirmation",
        html_content=f"Hey thank you for shopping with us! Your order is {order_id}"
    )
    response = sg.send(message)
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
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == "paid":
            line_item = session.list_line_items(session.id, limit=1).data[0]
            order_id = line_item['description']
            fulfill_order(order_id)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(order_id):
    order = Order.objects.get(id=order_id)
    order.ordered = Trueorder.orderDate = datetime.datetime.now()
    order.save()

    for item in order.items.all():
        product_var = ProductVariation.objects.get(id=item.product.id)
        product_var.stock -= item.quantity
        product_var.save()


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
             'name': form.cleaned_data['name'],
             'email_address': form.cleaned_data['email_address'],
             'phone': form.cleaned_data['phone'],
             'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(
                    subject, message, 'admin@test.com', ['admin@test.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect("home")

    form = ContactForm()
    return render(request, "contact.html", {'form': form})
