from django.urls import path

from orders import views

urlpatterns = [
    path('',views.orders_list,name='orders')
]