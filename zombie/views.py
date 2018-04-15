import datetime
import random
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from zombie.forms import FoodForm
from zombie.models import AbstractEntry, FoodEntry, TravelEntry


def _parse_raw_point(rp):
    qs = rp.split()
    a, b = qs[0], qs[1]
    return b, a


def _prepare_google_map_url(lz):
    trimmed = lz[13:-1]
    raw_points = trimmed.split(',')
    points = map(_parse_raw_point, raw_points)
    pairs = map(lambda p: ','.join(p), list(points))
    concatenated = '|'.join(pairs)
    prefix = 'https://maps.googleapis.com/maps/api/staticmap?size=600x400&maptype=roadmap&path=color:0xff0000ff|weight:5|'
    return prefix + concatenated


def index(req):
    if req.user.is_authenticated:
        return HttpResponseRedirect(reverse('timeline'))
    else:
        return render(req, 'zombie/index.html')


def _make_card_from_entry(entry):
    # Basics
    card = {
        'created': entry.created,
        'co2_cost': entry.co2_cost,
        'user': entry.user,
        'likes': random.choice([0, 0, 0, 1, 1, 2, 3 ])
    }

    # Type
    if isinstance(entry, FoodEntry):
        card['type'] = 'F'
        card['food_type'] = entry.get_dish_type_display()
        card['image'] = entry.image
    elif isinstance(entry, TravelEntry):
        card['type'] = 'T'
        card['travel_type'] = entry.get_travel_type_display()
        card['google_map_url'] = _prepare_google_map_url(entry.geometry)
    else:
        card['type'] = 'BROKEN'

    return card


@login_required
def timeline(req):
    context = {
        'cards': map(_make_card_from_entry, AbstractEntry.objects.all().order_by('-created'))
    }

    return render(req, 'zombie/timeline.html', context)


@login_required
def my_timeline(req):
    context = {
        'cards': map(_make_card_from_entry, AbstractEntry.objects.all().filter(user=req.user).order_by('-created'))
    }

    return render(req, 'zombie/timeline.html', context)


@login_required
def add_select(req):
    return render(req, 'zombie/add_select.html')


FOOD_COST_LOOKUP = {
    FoodEntry.DISH_TYPE_FISH: 1.0,
    FoodEntry.DISH_TYPE_MEAT: 2.0,
    FoodEntry.DISH_TYPE_VEGETARIAN: 0.5
}


@login_required
def add_food(req):
    # if this is a POST request we need to process the form data
    if req.method == 'POST':
        form = FoodForm(req.POST, req.FILES)
        # check whether it's valid:
        if form.is_valid():
            print('VALID')
            f = FoodEntry()
            f.created = datetime.datetime.now()
            f.user = req.user
            f.dish_type = form.cleaned_data['food_type']
            f.co2_cost = FOOD_COST_LOOKUP[f.dish_type]
            f.image = req.FILES['image']
            f.save()
            return HttpResponseRedirect(reverse('timeline'))
        else:
            print('NOT VALID')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FoodForm()

    context = {'form': form}
    pprint(context)
    return render(req, 'zombie/add_food.html', context)


@login_required
def profile(req):
    context = {
        'user': req.user
    }
    return render(req, 'zombie/profile.html', context)


@login_required
def compare(req):
    david = User.objects.get(email='david@shebang.nu')
    britta = User.objects.get(email='britta.duve@gmail.com')
    context = {}
    # entries_dp = AbstractEntry.objects.filter(created__gte=datetime.datetime.now()-datetime.timedelta(days=14)).filter(user=david)
    # entries_bd = AbstractEntry.objects.filter(created__gte=datetime.datetime.now()-datetime.timedelta(days=14)).filter(user=britta)

    values = []
    n = 14

    for k in range(n):
        start = datetime.date.today() - datetime.timedelta(days=n - k + 1)
        stop = datetime.date.today() - datetime.timedelta(days=n - k)
        entries_dp = AbstractEntry.objects.filter(created__gte=start).filter(created__lt=stop).filter(user=david)
        entries_bd = AbstractEntry.objects.filter(created__gte=start).filter(created__lt=stop).filter(user=britta)
        sum_dp = sum(list(map(lambda e: e.co2_cost, entries_dp)))
        sum_bd = sum(list(map(lambda e: e.co2_cost, entries_bd)))
        pprint(k)
        pprint(start)
        pprint(stop)
        pprint(entries_dp)
        pprint(entries_bd)
        pprint(sum_dp)
        pprint(sum_bd)

    return render(req, 'zombie/compare.html', context)


@login_required
def import_data(req):
    import zombie.ourdata
    entries = zombie.ourdata.get_travel_britta()
    for entry in entries:
        te = TravelEntry()
        te.created = entry['created']
        te.travel_type = entry['travel_type']
        te.distance_meters = entry['distance']
        te.co2_cost = entry['co2_cost']
        te.geometry = entry['geometry']
        te.user = User.objects.get(email='britta.duve@gmail.com')
        te.save()
    return HttpResponse('OK')

@login_required
def yyyimport_data(req):
    import zombie.ourdata
    entries = zombie.ourdata.get_food_entries()
    for entry in entries:
        te = FoodEntry()
        te.created = entry['created']
        te.dish_type = entry['dish_type']
        te.co2_cost = FOOD_COST_LOOKUP[entry['dish_type']]
        te.user = User.objects.get(email='britta.duve@gmail.com')
        te.image = entry['image']
        te.save()
    return HttpResponse('OK')
