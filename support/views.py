from django.shortcuts import render
from django.http import JsonResponse
import  json
import time
from django.shortcuts import get_object_or_404
from orders.models import Order

from support.agent import run_support_agent
from support.models import Conversations, Message
# Create your views here.

def chat(request,order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message") 
        
        if not user_message:
            return JsonResponse({"error":"empty data"},status=400)
        

        order = get_object_or_404(Order,user=request.user,id = order_id)
        conversation, created = Conversations.objects.get_or_create(user=request.user,order=order)
        
        Message.objects.create(conversations=conversation,role="user",content=user_message)
        
        #agent message
        reply = run_support_agent(user_message,conversation.id)
        #store llm reply
        Message.objects.create(conversations=conversation,role="assistant",content=reply)

        
        
        return JsonResponse({"reply":reply},status=200)
    