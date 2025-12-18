from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "ShopKart Administration"
admin.site.site_title = "ShopKart Admin"
admin.site.index_title = "Welcome to ShopKart Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
