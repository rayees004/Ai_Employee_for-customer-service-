from django.shortcuts import render,get_object_or_404

from orders.models import Order,RefundRequest
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders':orders
    }
    return render(request,'orders_list.html',context)

def order_detail(request,order_id):
    order = get_object_or_404(Order,id=order_id,user= request.user)
    refund = RefundRequest.objects.filter(order=order)

    context = {
        "order":order,
        'refunds':refund
    }
    return render(request,'order_detail.html',context)