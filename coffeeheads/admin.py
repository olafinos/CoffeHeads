from django.contrib import admin
from .models import Coffee, UserCoffee, Opinion

# Register your models here.

admin.site.register(Coffee)
admin.site.register(UserCoffee)
admin.site.register(Opinion)
