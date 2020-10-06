from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from shop.models import Product
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime, timezone
from django.contrib import messages

@login_required
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(email=email)        
        '''Pagination code '''
        paginator = Paginator(order_details, 3)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            orders = paginator.page(page)
        except(EmptyPage,InvalidPage):
            orders = paginator.page(paginator.num_pages)
        return render(request, 'orders/order_list.html', 
                                {'orders': orders, 'order_details': order_details})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.voucher:
                order.voucher = cart.voucher
                order.discount = cart.voucher.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            cart.clear()
            return render(request,
                        'orders/order/created.html',
                        {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                    'orders/order/create.html',
                    {'cart': cart,'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                    'admin/orders/order/detail.html',
                    {'order': order})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created
    current_date = datetime.now(timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60
    if minutes_diff < 30:
        order.delete()
        messages.add_message(request, messages.INFO,
                    'Order is now cancelled')
    else:
        messages.add_message(request, messages.INFO,
                            'Sorry, it is too late to cancel this order')
    return redirect('order_history')