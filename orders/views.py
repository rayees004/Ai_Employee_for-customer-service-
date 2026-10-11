from django.shortcuts import render

from orders.models import Order

# Create your views here.

def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders':orders
    }
    return render(request,'orders_list.html',context)

