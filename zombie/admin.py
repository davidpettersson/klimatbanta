from django.contrib import admin

from zombie.models import TravelEntry, FoodEntry

admin.site.register(TravelEntry)
admin.site.register(FoodEntry)