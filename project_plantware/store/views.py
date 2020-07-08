from django.shortcuts import render, redirect
from warehouse.models import *
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_user
from warehouse.forms import CustomerUpdateForm
import datetime



# Create your views here.

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def ProfilePage(request):
	orders = request.user.customer.order_set.all()
	print(orders.all())
	context = {'orders': orders}
	return render(request, 'store/profile.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def Profile_update(request):
	customer = request.user.customer
	form = CustomerUpdateForm(instance=customer)

	if request.method == 'POST':
		form = CustomerUpdateForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form': form}
	return render(request, 'store/profile_update.html', context)



def store(request):
	products = Product.objects.filter(available='True')
	context = {'products': products}
	return render(request, 'store/store.html', context)


def View_item(request, product_id):
	product = Product.objects.get(id=product_id)

	if request.method == 'POST':
		product = Product.objects.get(id=product_id)
		try:
			customer = request.user.customer

			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
			orderItem.quantity = int(request.POST['quantity'])
			orderItem.save()
		except:
			order = None

		return redirect('cart')

	context = {'product': product}
	return render(request, 'store/view_item.html', context)

def Remove_item(request, item_id):
	orderItem = OrderItem.objects.get(id=item_id)
	orderItem.delete()
	return redirect('cart')


def cart(request):

	try:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		if items.count() == 0:
			show = 'false'
		else:
			show = 'true'
	except:
		items = []
		order = None
		show = 'false'

	context = {'order': order, 'items': items, 'show': show}
	return render(request, 'store/cart.html', context)

def checkout(request):
	try:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		shipping = order.shippingaddress_set.all()
	except:
		items = []
		order = None
		shipping = []

	if request.method == 'POST':
		shipping = order.shippingaddress_set.all()
		shipping.delete()
		address = request.POST['address']
		city = request.POST['city']
		district = request.POST['district']
		zipcode = request.POST['zipcode']
		try:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			shipping, created = ShippingAddress.objects.get_or_create(customer=customer, order=order,
							address=address, city=city, district=district, zipcode=zipcode, complete=False)
			return redirect('payment_info')
		except:
			pass

	context = {'order': order, 'items': items, 'shipping': shipping}
	return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def PaymentInfo(request):
	try:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		shipping = order.shippingaddress_set.all()
		#print(shipping.get())
	except:
		items = []
		order = None
		shipping = []

	context = {'order': order, 'items': items, 'shipping': shipping}
	return render(request, 'store/payment_page.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	try:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		if order.complete != True:
			order.complete = True
			order.transaction_id = transaction_id
			#order.save()
			shipping, created = ShippingAddress.objects.get_or_create(customer=customer, order=order, complete=False)
			if shipping.complete != True:
				shipping.complete = True
				shipping.save()
				order.date_ordered = shipping.date_added
				order.save()
	except:
		pass
	return redirect('cus_profile')

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def cancelOrder(request):

	try:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		for item in items:
			item.delete()

		shipping, created = ShippingAddress.objects.get_or_create(customer=customer, order=order, complete=False)

		order.delete()
		shipping.delete()
	except:
		pass
	return redirect('store')



