from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, "product_id": product_id, 'weight': product.weight}
        else:
            if product.inventory >= self.cart[product_id]['quantity']:
                self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_post_price(self):
        weight = sum(item['weight']*item['quantity'] for item in self.cart.values())
        if weight < 500:
            return 0
        elif 500 <= weight < 1000:
            return 20000
        elif 1000 <= weight < 2000:
            return 30000
        else:
            return 50000

    def get_total_price(self):
        product_ids = []
        price = []
        for item in self.cart.values():
            product_ids.append(item["product_id"])
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            product_id = str(product.id)
            price.append(product.discount_price * self.cart[product_id]["quantity"])
        return sum(price)
        # return sum(item['price']*item['quantity'] for item in self.cart.values())

    def get_final_price(self):
        price = self.get_total_price() + self.get_post_price()
        return price

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
            self.cart[str(product.id)]["price"] = product.discount_price
        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def save(self):
        self.session.modified = True
