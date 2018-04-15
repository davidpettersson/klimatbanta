from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from klimatbanta import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'', include('zombie.urls'))
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)