from django.contrib.auth.models import User
from django.db.models import BooleanField, CASCADE, CharField, DateTimeField, DecimalField, \
    F, FloatField, ForeignKey, ImageField, \
    IntegerField, Model, OneToOneField, SET_NULL, TextField, ManyToOneRel


class Customer(Model):
    user = OneToOneField(User, null=True, blank=True, on_delete=CASCADE)
    name = CharField(max_length=70, null=True)
    email = CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


class Category(Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = CharField(max_length=30)
    image = ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        if self.image:
            url = self.image.url
        else:
            url = ''
        return url


MEASURE_TYPE = (
    (1, 'By Weight'),
    (2, 'By Quantity')
)

PACKAGE_SIZE = (
    (1, '100 gr'),
    (2, '250 gr'),
    (3, '500 gr'),
    (4, '1 kg'),
    (5, '1'),
    (6, '4'),
    (7, '6'),
    (8, '12'),
    (9, '24')
)


class MetaProduct(Model):
    class Meta:
        verbose_name = 'Meta Product'
        verbose_name_plural = 'Meta Products'

    name = CharField(max_length=70, unique=True)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)
    description = TextField(max_length=700, null=False, blank=False)
    availability = IntegerField(null=False, blank=False)
    digital = BooleanField(default=False, null=True, blank=True)
    image = ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        if self.image:
            url = self.image.url
        else:
            url = ''
        return url

    @property
    def favourite(self):
        pass
        #favourite =


class Product(Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    meta_product = ForeignKey(MetaProduct, on_delete=CASCADE)
    measure = IntegerField(verbose_name='Kind of measure', choices=MEASURE_TYPE)
    package = IntegerField(verbose_name='Package size', choices=PACKAGE_SIZE)
    price = DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.meta_product.name

    @property
    def name(self):
        name = self.meta_product.name
        return name

    @property
    def availability(self):
        availability = self.meta_product.availability / self.package
        return availability

    @property
    def imageURL(self):
        image = self.meta_product.image
        if image:
            url = self.meta_product.image.url
        else:
            url = ''
        return url


class Order(Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    date_ordered = DateTimeField(auto_now_add=True)
    complete = BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_order_no(self):
        order_no = self.id
        return order_no

    @property
    def get_orderitems(self):
        orderitems = self.orderitem_set.all()
        return orderitems

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital is False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True, blank=True)
    order = ForeignKey(Order, on_delete=SET_NULL, null=True, blank=True)
    quantity = IntegerField(default=0, null=True, blank=True)
    date_added = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_history_items(self):
        if self.order.complete is True:
            m_history_items = self.order.orderitems_set.all()
        return m_history_items

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(Model):
    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    order = ForeignKey(Order, on_delete=SET_NULL, null=True, blank=True)
    address = CharField(max_length=200, null=False)
    city = CharField(max_length=200, null=False)
    state = CharField(max_length=200, null=False)
    zipcode = CharField(max_length=200, null=False)
    date_added = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class OrderComment(Model):
    class Meta:
        verbose_name = 'Order Comment'
        verbose_name_plural = 'Orders Comments'

    order = OneToOneField(Order, on_delete=CASCADE, null=True, blank=True)
    comment = CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ProductOpinion(Model):
    product = ForeignKey(MetaProduct, on_delete=SET_NULL, null=True, blank=True)
    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    rating = IntegerField(null=True, blank=True)
    title = TextField(max_length=250, null=True, blank=True)
    opinion = TextField(max_length=1500, null=True, blank=True)
    date_created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FavouriteProduct(Model):
    class Meta:
        verbose_name = 'Favourite Product'
        verbose_name_plural = 'Favourite Products'

    meta_product = ForeignKey(MetaProduct, on_delete=CASCADE)
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True)
    favourite = BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.meta_product.name

    @property
    def name(self):
        name = self.meta_product.name
        return name
