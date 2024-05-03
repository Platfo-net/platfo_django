from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

base_urlpatterns = (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

urlpatterns = base_urlpatterns + [
    path('admin/', admin.site.urls),
]

# if settings.DEBUG:
#     urlpatterns += [path('__debug__/', include('debug_toolbar.urls')), ]
