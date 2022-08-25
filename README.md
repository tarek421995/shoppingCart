# shoppingCart

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/tarek421995/shoppingCart.git
$ cd shoppingCart
```

Create a virtual environment to install dependencies in and activate it:

## for linux user
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

## for windows uesrs :
```sh
$ python3 -m venv venv
$ ./venv/Scripts/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd shoppingCart
(venv)$ python manage.py createsuperuser 
(venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/cart/`.

you just have to add items manually to cart from django admin panel 

### The WorkFlow 
1 : add new items from the admin panel. <br />
2 : create new CartItem for those Items. <br />
3 : create New user with django base auth system and then login. <br />
4 : create user session to store The Cart item , so the user can resume his work in case of logging out or losing internet connection. <br />
5 : navigate to /cart/ to see the items listed. <br />
6 : play around with JavaScript Features like : realtime validation , auto item quantity adjust,
    if the item is no longer exist or you have orderd more then the store have,
    message for clearfication to know whats going on in the shoppong cart. <br />
7 : complete you order with buy button to see you cart confirmation detail and checkout button to confirm the purcheses with nice thank you page. <br />
8 : reset cart item session on every click on checkout button in finalize page. <br />
    
    
    

