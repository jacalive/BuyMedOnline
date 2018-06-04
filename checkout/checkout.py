from decimal import Decimal
from django.conf import settings
from BuyMed.models import Product

class Checkout(object):
    def __init__(self, request):
        """
        Initialize the Checkout.
        """
        self.session = request.session
        checkout = self.session.get(settings.CHECKOUT_SESSION_ID)
        if not checkout:
            # save an empty checkout in the session
            checkout = self.session[settings.CHECKOUT_SESSION_ID] = {}
        self.checkout = checkout


    def __iter__(self):
        """
        Iterate over the items in the checkout and get the products
        from the database.
        """
        product_ids = self.checkout.keys()
        # get the product objects and add them to the checkout
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.checkout[str(product.id)]['product'] = product
            
        for item in self.checkout.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        """
        Count all items in the checkout.
        """
        return sum(item['quantity'] for item in self.checkout.values())


    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the checkout or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.checkout:
            self.checkout[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.checkout[product_id]['quantity'] = quantity
        else:
            self.checkout[product_id]['quantity'] += quantity
        self.save()
        
        
    def save(self):
        # update the session checkout
        self.session[settings.CHECKOUT_SESSION_ID] = self.checkout
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the checkout.
        """
        product_id = str(product.id)
        if product_id in self.checkout:
            del self.checkout[product_id]
            self.save()


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.checkout.values())


    def clear(self):
        # remove checkout from session
        del self.session[settings.CHECKOUT_SESSION_ID]
        self.session.modified = True
