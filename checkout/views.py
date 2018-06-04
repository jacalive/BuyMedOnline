from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from BuyMed.models import Product
from .checkout import Checkout
from .forms import CheckoutAddProductForm

@require_POST

def checkout_remove(request, product_id):
    checkout = Checkout(request)
    product = get_object_or_404(Product, id=product_id)
    checkout.remove(product)
    return redirect('checkout:checkout_detail')


def checkout_detail(request):
    checkout = Checkout(request)
    for item in checkout:
        item['update_quantity_form'] = CheckoutAddProductForm(
                                            initial={'quantity': item['quantity'],
                                            'update': True})
    return render(request, 'checkout/detail.html', {'checkout': checkout})
