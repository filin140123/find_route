from django.contrib import admin
from django.urls import path, include

from routes.views import home, find_routes
from travel.views import about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include(('cities.urls', 'cities'))),
    path('trains/', include(('trains.urls', 'trains'))),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('about/', about),
    path('find_routes/', find_routes, name='find_routes'),
]
