"""django_app URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from conf_app import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('halls/', v.show_halls, name='halls'),
    path('room/new', v.add_hall, name='add_hall'),
    path('room/<int:id>', v.hall_details, name='hall_details'),
    path('halls_details/', v.show_halls_details, name='halls_details'),
    path('room/reserve/<int:id>', v.add_reservation, name='new_reservation'),
    path('reserve/', v.new_reservation, name='new_reservation'),
    path('room/delete/<int:id>', v.delete_hall, name='delete_hall'),
    path('room/modify/<int:id>', v.edit_hall, name='edit_hall'),
    path('reservations/', v.show_reservations, name='show_reservations'),
    path('search', v.search_halls, name='search_halls'),
    re_path(r'^search/(?P<hall_id>(\d+))/(?P<capacity>(\d+))/(?P<projector>(\d))$', v.find_halls, name='find_halls'),
    path('res/modify/<int:id>', v.edit_reservation, name='edit_reservation'),
    path('res/delete/<int:id>', v.delete_reservation, name='delete_reservation'),
    re_path(r'^search_res/(?P<date>\d{4}-\d{2}-\d{2})/(?P<hall_id>(\d+))/(?P<word>(\w+))$', v.find_res, name='find_res'),
    path('search_res', v.search_res, name='search_res'),
]