from django.contrib import admin

from .models import Price, Tour, User, Reservation

# Register your models here.
admin.site.register(Price)
admin.site.register(Tour)
admin.site.register(User)
admin.site.register(Reservation)