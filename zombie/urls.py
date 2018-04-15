from django.conf.urls import url, include
from zombie import views

urlpatterns = [
    url(r'^timeline', views.timeline, name='timeline'),
    url(r'^my-timeline', views.my_timeline, name='my-timeline'),
    url(r'^compare', views.compare, name='compare'),
    url(r'^import-data', views.import_data, name='import-data'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^add/select', views.add_select, name='add-select'),
    url(r'^add/food', views.add_food, name='add-food'),
    url(r'^$', views.index, name='index'),
]
