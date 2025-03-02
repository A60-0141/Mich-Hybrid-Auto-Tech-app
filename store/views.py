from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime


from .models import *
from . utils import cookieCart, cartData, guestOrder

# Create your views here.


def store(request):
	
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	# Get or create customer if user is authenticated

    # Pass all necessary data to the template
	context = {'products':products, 'cartItems':cartItems,}
	return render(request, 'store/store.html', context)

def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
		#Create empty cart for now for non-logged in user
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)




from django.shortcuts import render
from .models import Customer

def store(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
    else:
        customer = None  # If the user is not logged in

    context = {'customer': customer}
    return render(request, 'store/store.html', context)





def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    # Fetch products from the database
    products = Product.objects.all()

    # Debugging: Check if products exist
    if not products:
        print("⚠️ No products found in the database!")
    else:
        print(f"✅ Found {products.count()} products:")
        for product in products:
            print(f"- {product.name}, Image: {product.imageURL}")

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)





from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

