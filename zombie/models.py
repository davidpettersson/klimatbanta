from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel



class AbstractEntry(PolymorphicModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(
        verbose_name='created'
    )

    co2_cost = models.FloatField(
        verbose_name='carbondioxide cost'
    )


class TravelEntry(AbstractEntry):
    TRAVEL_TYPE_BUS = 'B'
    TRAVEL_TYPE_RAIL = 'R'
    TRAVEL_TYPE_CAR_PETROL = 'P'
    TRAVEL_TYPE_CYCLE = 'C'
    TRAVEL_TYPE_WALK = 'W'
    TRAVEL_TYPE_FLIGHT = 'F'

    TRAVEL_CHOICES = (
        (TRAVEL_TYPE_BUS, 'buss'),
        (TRAVEL_TYPE_RAIL, 'tåg'),
        (TRAVEL_TYPE_CAR_PETROL, 'bil (bensin)'),
        (TRAVEL_TYPE_CYCLE, 'cykel'),
        (TRAVEL_TYPE_WALK, 'gång'),
        (TRAVEL_TYPE_FLIGHT, 'flyg'),
    )

    distance_meters = models.FloatField(
        verbose_name='distance in meters'
    )

    travel_type = models.CharField(
        max_length=1,
        choices=TRAVEL_CHOICES,
        verbose_name='travel type'
    )

    geometry = models.TextField(
        verbose_name='geometry'
    )

    class Meta:
        verbose_name_plural = 'travel entries'


class FoodEntry(AbstractEntry):
    DISH_TYPE_MEAT = 'M'
    DISH_TYPE_FISH = 'F'
    DISH_TYPE_VEGETARIAN = 'V'

    DISH_CHOICES = ((DISH_TYPE_MEAT, 'kött'),
                    (DISH_TYPE_FISH, 'fisk'),
                    (DISH_TYPE_VEGETARIAN, 'vegetariskt'))

    dish_type = models.CharField(
        max_length=1,
        choices=DISH_CHOICES,
        verbose_name='dish type'
    )

    image = models.ImageField(
        upload_to='food_entries/',
        verbose_name='image'
    )

    class Meta:
        verbose_name_plural = 'food entries'
