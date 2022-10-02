from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db.models import Q
from conf_app.models import ConferenceHall, Reservation
from conf_app.forms import HallForm, ReservationForm
from datetime import datetime