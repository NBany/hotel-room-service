from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db.models import Q
from conf_app.models import ConferenceHall, Reservation
from conf_app.forms import HallForm, ReservationForm
from datetime import datetime


def show_halls(request):
    halls = ConferenceHall.objects.all()
    reservations = Reservation.objects.all()
    status = {}
    check_res = []
    for r in reservations:
        check_res.append(r.hall)
    for h in halls:
        if h not in check_res:
            status = 'Free'
        else:
            for r in reservations:
                if datetime.today().date() == r.date and h == r.hall:
                    status = 'Reserved'
                    break
                else:
                    status = 'Free'
            status[h.id] = status
    return render(request, 'show_halls.html', context={'halls': halls, 'status': status})


def show_halls_details(request):
    if 'message' in request.session:
        del request.session['message']
    halls = ConferenceHall.objects.all()
    reservations = Reservation.objects.filter(date__gte=datetime.today().date())
    if request.method == 'GET':
        if request.session.get('order_by'):
            if request.session.get('order_by') == 2:
                halls = ConferenceHall.objects.all().order_by('-capacity')
            elif request.session.get('order_by') == 1:
                halls = ConferenceHall.objects.all().order_by('capacity')
        return render(request, 'show_halls_details.html', context={'halls': halls, 'reservations': reservations })
    else:
        if request.POST.get('sort') == "2":
            halls = ConferenceHall.objects.all().order_by('-capacity')
            request.session['order_by'] = 2
        elif request.POST.get('sort') == "1":
            halls = ConferenceHall.objects.all().order_by('capacity')
            request.session['order_by'] = 1
        else:
            request.session['order_by'] = 0
        return render(request, 'show_halls_details.html', context={'halls': halls, 'reservations': reservations})


def hall_details(request, id):
    halls = ConferenceHall.objects.filter(Q(pk=int(id)))
    reservations = Reservation.objects.filter(Q(hall=ConferenceHall.objects.get(pk=id)))
    return render(request, 'show_halls_details.html', context={'halls': halls, 'reservations': reservations})


def add_hall(request):
    if 'message' in request.session:
        del request.session['message']
    form = HallForm()
    if request.method == 'GET':
        return render(request, 'add_hall.html', context={'form': form})
    else:
        form = HallForm(request.POST)
        name = request.POST.get('name')
        halls = ConferenceHall.objects.all()
        names = []
        for hall in halls:
            names.append(hall.name)
        if form.is_valid() and name not in names:
            form.save()
            request.session['message'] = f'{name} hall added'
            return redirect('halls')
        else:
            message = 'Something went wrong.'
            form = HallForm()
            return render(request, 'add_hall.html', context={'form': form, 'message': message})


