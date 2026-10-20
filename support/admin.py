from django.contrib import admin

# Register your models here.

from .models import Conversations,Message,AgentLog

admin.site.register(Conversations,)
admin.site.register(Message,)
admin.site.register(AgentLog)