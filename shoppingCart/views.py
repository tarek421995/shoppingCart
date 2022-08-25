from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from carts.models import Item, Cart

def home(request):
    context = {}
    # in_cart = []
    cart_obj, _ = Cart.objects.new_or_get(request)
    in_cart = list(cart_obj.items.all())
    items = Item.objects.all()
    cart_item = []
    for cartitem in in_cart:
        cart_item.append(cartitem.item)  
    context['cart'] = cart_item
    context['items'] = items
    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })
