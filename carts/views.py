from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Item
from django.http import JsonResponse
from django.shortcuts import render
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def cart_home(request):
    cart_obj, _ = Cart.objects.new_or_get(request)
    context = {
       "cart": cart_obj
    }
    return render(request, "carts/cart_home.html", context)


def cart_update(request):
    item_id = request.POST.get('item_id')
    cart_obj, _= Cart.objects.new_or_get(request)
    if item_id is not None:
        try:
            item_obj = Item.objects.get(id=item_id)
            cart_item,_ = CartItem.objects.get_or_create(item=item_obj, cart_id=cart_obj.id)
            print(cart_item)
        except Item.DoesNotExist:
            return redirect("cart:home")
        if cart_item in cart_obj.items.all():
            cart_obj.items.remove(cart_item)   
            added = False
        else:
            cart_obj.items.add(cart_item)
            cart_obj.save() 
            added = True
        if is_ajax(request): # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.items.count()
            }
            return JsonResponse(json_data, status=200) # HttpResponse
            # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("cart:home")



def cart_update_session(request ,list):
    cart_obj, _ = Cart.objects.new_or_get(request)
    subtotal = 0
    cart_obj.total= 0
    msg = ''
    for data in list:
         if type(data) is list:
               data = data[0]
         slug = data.split('/')[0]
         quantity = data.split('/')[1]
         item = Item.objects.filter(slug=slug).first()
         cart_item,_ = CartItem.objects.get_or_create(item=item,cart_id=cart_obj.id)
         if item.quant_in == 0:
            msg = f'I’m sorry but weare out of stock for {item.title}'
            quantity_item = 0
            cart_item.quantity = quantity_item
            cart_item.total_price = 0
         elif int(quantity) > item.quant_in:
            msg = f'I’m sorry but we only have {item.quant_in}kg of item {item.title} left'
            quantity_item = item.quant_in
            cart_item.quantity =quantity_item
            cart_item.total_price = Decimal(item.price) * Decimal(quantity_item)
         else:
            msg = 'The Cart Updated'
            quantity_item =  quantity
            cart_item.quantity = quantity
            cart_item.total_price = Decimal(item.price) * Decimal(quantity)
         print(cart_item.total_price)
         cart_item.save()
         subtotal += cart_item.total_price
    cart_obj.total = subtotal
    cart_obj.save() 
    return msg ,quantity_item 


def quantity_update(request):
   if is_ajax(request) and request.method =='POST':
      item_data = request.POST.getlist('item_data[]')
      if len(item_data)>1:
         request.session['items'] = item_data
         _, _ = cart_update_session(request,item_data)
         return JsonResponse({"message": "updated",'data':item_data}, status=200)
      else:
         if not 'items' in request.session or not request.session['items']:
               request.session['items'] = item_data
         else:
               saved_list = request.session['items']
               size = len(item_data[0])
               strings_with_substring = [string for string in saved_list if item_data[0][:size - 3] in string]
               if strings_with_substring:
                  saved_list.remove(strings_with_substring[0])  
               saved_list.append(item_data[0])
               request.session['item'] = saved_list 
         msg, quantity_item = cart_update_session(request,request.session['items'])
         data = request.session['items']
         return JsonResponse({"msg": msg,'data':quantity_item}, status=200)
   else:
      return JsonResponse({"message": 'try again'}, status=500)


def cart_checkout(request):
   context = {}
   cart_obj,_ = Cart.objects.new_or_get(request)
   item_data = request.POST.get('finalize')
   if item_data == 'final':
      context['msg'] = 'thanks'
      cart_obj.active = False
      cart_obj.save()
      del request.session['cart_id']
      del request.session['items']
   else:
      context['cart'] = cart_obj
      message  = 'Confirm Your Order Please.'
      messages.success(request, message)
   return render(request, "carts/confirm.html", context)
