from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(City)
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(ScreenSeat)
admin.site.register(Movie)
admin.site.register(MovieCast)
admin.site.register(Screening)
admin.site.register(Booking)
admin.site.register(ShowSeat)
admin.site.register(Payment)
