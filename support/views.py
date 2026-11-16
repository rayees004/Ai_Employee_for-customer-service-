from django.shortcuts import render
from django.http import JsonResponse
import  json
import time
from django.shortcuts import get_object_or_404
from orders.models import Order
# Create your views here.

def chat(request,order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message") 
        
        if not user_message:
            return JsonResponse({"error":"empty data"},status=400)
        time.sleep(4)

        # order = get_object_or_404(Order,user=request.user,id = order_id)
        # conversation, created = Conversations.get_or_create()
        return JsonResponse({"reply":"here is reply message"},status=200)
    