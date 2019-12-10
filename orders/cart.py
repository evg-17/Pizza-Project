from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # def add(self, product, quantity=1, update_quantity=False):
    #     """
    #     Add a product to the cart or update its quantity.
    #     """
    #     product_id = str(product.id)
    #     if product_id not in self.cart:
    #         self.cart[product_id] = {'quantity': 0,
    #                                   'price': str(product.price)}
    #     if update_quantity:
    #         self.cart[product_id]['quantity'] = quantity
    #     else:
    #         self.cart[product_id]['quantity'] += quantity
    #     self.save()

    def add(self, product, toppings=None):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        toppings = str(toppings)
        # cart_product = str(product.id) + str(toppings)


        # if product_id not in self.cart or (product_id in self.cart and self.cart[product_id]['toppings'] != toppings):
        #     self.cart[product_id] = {'quantity': 1,
        #                              'price': str(product.price),
        #                              'toppings': toppings}
        # else:
        #     self.cart[product_id]['quantity'] += 1


        # if product_id not in self.cart:
        #     self.cart[product_id] = {'quantity': 1,
        #                               'price': str(product.price),
        #                               'toppings': toppings}
        # else:
        #     if self.cart[product_id]['toppings'] == toppings:
        #         self.cart[product_id]['quantity'] += 1
        #     else:

        # if cart_product not in self.cart:
        #      self.cart[cart_product] = {'p_id': str(product.id),
        #                            'quantity': 1,
        #                            'price': str(product.price),
        #                            'toppings': toppings}
        # else:
        #      self.cart[cart_product]['quantity'] += 1

        if product_id not in self.cart:
            self.cart[product_id] = {toppings: {
                                   'quantity': 1,
                                   'price': str(product.price)}}
        else:
            if toppings in self.cart[product_id]:
                self.cart[product_id][toppings]['quantity'] += 1
            else:
                self.cart[product_id][toppings] = {'quantity': 1,
                                                   'price': str(product.price)}

        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()

        # product_ids_temp = self.cart.keys()
        # product_ids = []
        # for key in product_ids_temp:
        #     id = key.split('[')[0]
        #     if id not in product_ids:
        #         product_ids.append(id)

        #get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        # orig
        # for product in products:
        #     cart[str(product.id)]['product'] = product

        for prod in cart.values():
            for item in prod.values():
                for product in products:
                    if prod == str(product.id):
                        item['product'] = product

        for product in products:
            if str(product.id) in self.cart:


        for prod in cart.values():
            for item in prod.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

        # orig
        # for item in cart.values():
        #     item['price'] = Decimal(item['price'])
        #     item['total_price'] = item['price'] * item['quantity']
        #     yield item

    # def __len__(self):
    #     """
    #     Count all items in the cart.
    #     """
    #     return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # orig
        # return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        cart = self.cart.copy()
        for prod in cart.values():
            for item in prod.values():
                return sum(Decimal(item['price']) * item['quantity'] for item in prod.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()


# {% block header %}
#
#   <nav class="navbar navbar-expand">
#     <ul class="navbar-nav mr-auto p-2">
#       {#% for category in categories %}
#         <li class="nav-item">
#           <a class="nav-link" href="{{ category.get_absolute_url }}">{{ category.name }}</a>
#         </li>
#       {#% endfor %}
#     </ul>
#   </nav> -->
# {% endblock %}

# <div class="container-fluid d-flex flex-row">
# <div class="board d-flex justify-content-center">
#   <table id="menu-board">
#     {% if category %}
#       {% if category.sized == True %}
#         <tr>
#           <th></th>
#           <th>Small</th>
#           <th>Large</th>
#         </tr>
#         {% for dish in dishes %}
#         <tr>
#           <td>{{ dish.name }}</td>
#           {% for p in products_small %}
#             {% if dish.name == p.dish.name %}
#               <td>{{ p.price }}</td>
#               <td><a href="{% url 'orders:cart_add' category.slug p.id %}">+</a></td>
#             {% endif %}
#           {% endfor %}
#           {% for p in products_large %}
#             {% if dish.name == p.dish.name %}
#               <td>{{ p.price }}</td>
#               <td><a href="{% url 'orders:cart_add' category.slug p.id %}">+</a></td>
#             {% endif %}
#           {% endfor %}
#         </tr>
#         {% endfor %}
#       {% else %}
#         {% for p in products_unsized %}
#         <tr>
#           <td>{{ p.dish.name }}</td>
#           <td>{{ p.price }}</td>
#           <td><a href="{% url 'orders:cart_add' category.slug p.id %}">+</a></td>
#         </tr>
#         {% endfor %}
#       {% endif %}
#     {% endif %}
#   </table>
# </div>
# <div class="order d-flex justify-content-center">
#   {% if cart %}
#     {% for item in cart %}
#       {% with product=item.product %}
#         {{ product.dish.category.name }}
#         {{ product.dish.name }}
#         {{ product.size.name }}
#         {{ product.price }}
#       {% endwith %}
#     {% endfor %}
#   {% endif %}
# </div>


#<td><button><a href="{% url 'orders:cart_remove' category.slug product.id %}">-</a></button></td>
