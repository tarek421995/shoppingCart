from django.db import models
from shoppingCart.hash import HashableModel
from django.contrib.auth.models import User
from shoppingCart.utils import unique_slug_generator
from django.db.models.signals import pre_save
# Create your models here.

class Item(HashableModel):
    title       = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    price       = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    quant_in    = models.SmallIntegerField(default=1)
    slug        = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'description','price','quant_in','slug']),     
        ]

def item_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug :
        instance.slug = unique_slug_generator(instance)
        slug = instance.slug
        print(slug)
        
pre_save.connect(item_pre_save_receiver, sender=Item)

class CartItem(HashableModel):
    item        = models.ForeignKey(Item ,on_delete=models.CASCADE, blank=True)
    cart_id     = models.CharField(max_length=60, blank=True)
    quantity    = models.SmallIntegerField(default=1)
    total_price = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['item','quantity', 'total_price','cart_id']),
            
        ]
    def __str__(self):
        return str(self.item)


class CartManager(models.Manager):
    def new_or_get(self, request):
        user=request.user
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if user.is_authenticated and cart_obj.user is None:
                cart_obj.user = user
                cart_obj.save()    
        else:
            cart_obj = Cart.objects.new(user=user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(HashableModel):
    user        = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    items       = models.ManyToManyField(CartItem, blank=True)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    class Meta:
        indexes = [
            models.Index(fields=['user','total', 'updated', 'timestamp']),
        ]
    def __str__(self):
        return str(f'By {self.user}, Total: {self.total}')




