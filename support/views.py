from django.shortcuts import render
from django.http import JsonResponse
import  json
# Create your views here.

def chat(request,order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message") 
        
        if not user_message:
            return JsonResponse({"error":"empty data"},status=400)
        return JsonResponse({"reply":"here is reply message"},status=200)
    