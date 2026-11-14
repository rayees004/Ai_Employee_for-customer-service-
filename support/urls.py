from django.urls import path
from support import views

urlpatterns = [
    path("chat/<int:order_id>/",views.chat,name="support_chat")
]
