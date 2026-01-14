from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Item, Order
from .services import create_checkout_session, create_order_checkout_session
from django.conf import settings


def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    session = create_checkout_session(item)
    return JsonResponse({"id": session.id})

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    public_key = settings.STRIPE_KEYS[item.currency]["public"]

    return render(request, "item.html", {
        "item": item,
        "stripe_public_key": public_key
    })

def buy_order(request, id):
    order = get_object_or_404(Order, id=id)
    session = create_order_checkout_session(order)
    return JsonResponse({"id": session.id})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.currency
    public_key = settings.STRIPE_KEYS[currency]["public"]

    return render(request, "order.html", {
        "order": order,
        "stripe_public_key": public_key
    })
