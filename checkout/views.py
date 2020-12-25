from django.shortcuts import render, get_object_or_404, reverse, HttpResponse, redirect
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import stripe
import json

from books.models import Book
from .models import Purchase

# Create your views here.


def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get("shopping_cart", {})
    line_items = []
    all_book_ids = []
    for book_id, book in cart.items():
        book_model = get_object_or_404(Book, pk=book_id)
        item = {
            "name": book_model.title,
            "amount": int(book_model.price),
            "quantity": book['qty'],
            "currency": "USD",
        }
        line_items.append(item)
        all_book_ids.append({
            'book_id': book_model.id,
            'qty': book['qty']
        })

    current_site = Site.objects.get_current()
    domain = current_site.domain

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        client_reference_id=request.user.id,
        metadata={
            "all_book_ids": json.dumps(all_book_ids)
        },
        mode="payment",
        success_url=domain+reverse("checkout_success"),
        cancel_url=domain+reverse("checkout_cancelled")
    )
    return render(request, "checkout/checkout.template.html", {
        "session_id": session.id,
        "public_key": settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
def payment_compeleted(request):
    payload = request.body
    endpoint_secret = settings.ENDPOINT_SECRET
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Invalid Payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid Signature")
        return HttpResponse(status=400)

    if event['type'] == 'checkout_session.completed':
        session = event['data']['object']
        handle_payment(session)
    return HttpResponse(status=200)


def checkout_success(request):
    request.session["shopping_cart"] = {}
    messages.success(request, "Payment Complete! Thank you for purchase!")
    return redirect(reverse("homepage"))


def checkout_cancelled(request):
    messages.error(request, "Payment Cannot be Completed !!! Kindly check card details !")
    return redirect(reverse("view_cart"))


def handle_payment(session):
    metadata = session['metadata']
    user = get_object_or_404(User, pk=session["client_reference_id"])
    all_book_ids = json.loads(metadata["all_book_ids"])
    for book_id in all_book_ids:
        book_model = get_object_or_404(Book, pk=book_id["book_id"])

        purchase = Purchase()
        purchase.book_id = book_model
        purchase.user_id = user
        purchase.qty = book_id['qty']
        purchase.price = book_model.price

        purchase.save()
