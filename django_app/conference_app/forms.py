from django import forms
from django.forms import ModelForm
from conf_app.models import ConferenceHall, Reservation

class HallForm(ModelForm):
    class Meta:
        model = ConferenceHall
        fields = ["name", "capacity", "projector"]

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ["date", "hall", "description"]