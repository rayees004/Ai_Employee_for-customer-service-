from django.contrib import admin

# Register your models here.
from .models import Product,Order,RefundRequest

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category','in_stock']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','product_name','amount','status','carrier','tracking_number']

class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ['order','user','reason','status','created_at']
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(RefundRequest,RefundRequestAdmin)



