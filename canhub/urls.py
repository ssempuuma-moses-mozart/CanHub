from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include('public.urls')),
	path('cancer/', include('cancer.urls')),
    path('admin/', admin.site.urls),
	path("", include("network.urls")),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)