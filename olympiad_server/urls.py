from django.contrib import admin
from django.urls import include, path
from reviews.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reviews.urls')),
    path('auth/', include('authentication.urls')),
]
