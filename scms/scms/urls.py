
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views.views import LOGIN



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LOGIN,name='login'),
    path('users/', include('users.urls')),
    # path('attendence/', include('attendence.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
