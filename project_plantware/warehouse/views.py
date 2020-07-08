from django.shortcuts import render, redirect
from .models import *
from .forms import ProductAddForm, ProductionPlanForm
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_user, loginpage_control
from django.contrib import messages



# Create your views here.
@login_required(login_url='login')
@loginpage_control
def home(request):
    total_products = Product.objects.all().count()
    shipping = ShippingAddress.objects.all()
    orders = shipping.filter(order__delivery='False').count()
    production = Production.objects.all()
    plans = production.filter(prepared='False').count()

    context = {'total_products': total_products, 'orders': orders, 'plans': plans}
    return render(request, 'warehouse/home.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def admin_profile(request):
    return render(request, 'warehouse/admin_profile.html')

#admin-products
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def productlist(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'warehouse/products.html', context)




@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createProduct(request):
    form = ProductAddForm()
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {'form': form}
    return render(request, 'warehouse/product_add.html', context)




@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def UpdateProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductAddForm(instance=product)
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {'form': form}
    return render(request, 'warehouse/product_add.html', context)




@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def DeleteProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_list')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        category = request.POST['category']
        Category.objects.create(name=category)
        return redirect('category')

    context = {'categories': categories}
    return render(request, 'warehouse/category_page.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('category')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'warehouse/customer.html', context)



@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer_details(request, cus_id):
    customer = Customer.objects.get(id=cus_id)
    shippings = customer.shippingaddress_set.all()
    context = {'customer': customer, 'shippings': shippings}
    return render(request, 'warehouse/cus_details.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def cus_order(request, ord_id):
    order = Order.objects.get(id=ord_id)
    orderlist = order.orderitem_set.all()

    address = order.shippingaddress_set.all()
    #print(address.get())
    context = {'orderlist': orderlist, 'order': order, 'address': address}
    return render(request, 'warehouse/cus_order_page.html', context)




@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def order_view(request):
    shippings = ShippingAddress.objects.filter(order__delivery='False')

    if request.method == 'POST':
        date = request.POST['date']
        DayOrder.objects.create(date=date)
        return redirect('date_order')
    else:
        pass

    context = {'shippings': shippings}
    return render(request, 'warehouse/order(emp).html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def dateOrder(request):
    selected_day = DayOrder.objects.last()
    date = selected_day.date
    #print(selected_day, selected_day.date, date)
    shippings = ShippingAddress.objects.filter(date_added__month=date.month, date_added__year=date.year, date_added__day=date.day)
    total_items = shippings.count()
    total = sum(shipping.order.get_cart_total for shipping in shippings)
    selected_day.delete()
    context = {'shippings': shippings, 'date': date, 'total_items': total_items, 'total': total}
    return render(request, 'warehouse/selected_orders.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def order_delivery_view(request):
    shippings = ShippingAddress.objects.filter(order__delivery='True')
    context = {'shippings': shippings}
    return render(request, 'warehouse/previous_order.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def order_details(request, shipping_id):
    shipping = ShippingAddress.objects.get(id=shipping_id)
    order = Order.objects.get(id=shipping.order.id)
    orderlist = order.orderitem_set.all()
    context = {'orderlist': orderlist, 'shipping': shipping}
    return render(request, 'warehouse/order_details.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def OrderDelivery(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.orderitem_set.all()
    sending = 'True'
    packet = []
    for item in items:
        product = Product.objects.get(id=item.product.id)
        if product.quantity > item.quantity:
            pass
        else:
            packet.append(product.name)
            sending = 'False'

    if sending == 'True':
        if order.delivery != True:
            for item in items:
                product = Product.objects.get(id=item.product.id)
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    product.save()

            order.delivery = True
            order.save()
    else:
        for i in packet:
            messages.info(request, i, extra_tags='order')
        messages.info(request, ' less then order amount.', extra_tags='order')
        messages.info(request, 'Delivery cannot possible', extra_tags='order')
        return redirect('production_new')

    return redirect('order_view_delivery')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def productionPlan(request):
    productions = Production.objects.filter(prepared='False')
    context = {'productions': productions}
    return render(request, 'warehouse/productionslist.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def ViewPreviousPlan(request):
    productions = Production.objects.filter(prepared='True')
    context = {'productions': productions}
    return render(request, 'warehouse/previous_plan.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createProductionPlan(request):
    form = ProductionPlanForm()
    if request.method == 'POST':
        form = ProductionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('production_list')

    context = {'form': form}
    return render(request, 'warehouse/new_production.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def DeleteproductionPlan(request, plan_id):
    plan = Production.objects.get(id=plan_id)
    plan.delete()
    return redirect('production_list')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def Doneproductionplan(request, plan_id):
    plan = Production.objects.get(id=plan_id)
    product = Product.objects.get(id=plan.product.id)

    if plan.prepared != True:
        product.quantity += plan.quantity
        plan.prepared = 'True'
        plan.save()
        if product.available != True:
            product.available = True

        product.save()
    return redirect('production_list')
