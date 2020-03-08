from decimal import Decimal
from django.conf import settings
from shop.models import Product
from vouchers.models import Voucher

class Cart(object):
    def __init__(self, request): #init the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        self.voucher_id = self.session.get('voucher_id')

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} #saving an empty cart in a session
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price']  = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
         return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum (Decimal(item['price']) * item['quantity'] for item in 
        self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    @property
    def voucher(self):
        if self.voucher_id:
            return Voucher.objects.get(id=self.voucher_id)
        return None
    
    def get_discount(self):
        if self.voucher:
            return(self.voucher.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
        