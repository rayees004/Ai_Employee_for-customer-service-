from django.db import models
from django.contrib.auth.models import User
from orders.models import Order
# Create your models here.

class Conversations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="conversations")
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Conversation #{self.id} - {self.user.username} / order #{self.order.id}"

class Message(models.Model):
    ROLE_CHOICES = [
        ('user',"User"),
        ('agent', "Agent")
    ]
    conversations = models.ForeignKey(Conversations,on_delete=models.CASCADE,related_name="messages")
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.role} :{self.content[:50]}"

class AgentLog(models.Model):
    EVENT_CHOICES = [
        ('support',"Support Agent"),
        ('tool_call',"Tool Call"),
        ("tool_result","Tool Result"),
        ("manager","Manger Agent"),
        ("rist","Risk Agent"),
        ("final", "Final Reply")
    ]
    conversations = models.ForeignKey(Conversations,on_delete=models.CASCADE, related_name="agentlogs")
    event_type = models.CharField(max_length=20,choices=EVENT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"[{self.event_type}] - {self.message[:40]}"


