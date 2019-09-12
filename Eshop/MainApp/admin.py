from django.contrib import admin
from MainApp.models import *

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(PreviousOrder)
admin.site.register(Order)
admin.site.register(Checkout)