from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db.models import Q
from models import ConferenceHall, Reservation
from forms import HallForm, ReservationForm
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


def delete_hall(request, id):
    if 'message' in request.session:
        del request.session['message']
    hall = ConferenceHall.objects.get(pk=id)
    hall.delete()
    request.session['message'] = f"{hall.name} hall has been deleted."
    return redirect('halls')


def edit_hall(request, id):
    if 'message' in request.session:
        del request.session['message']
    hall = ConferenceHall.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'edit_hall.html', context={'hall': hall})
    else:
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        halls = ConferenceHall.objects.all()
        names = []
        for h in halls:
            if h.name != name:
                names.append(h.name)
        if name and int(capacity) > 0 and name not in names:
            hall.name = name
            hall.capacity = int(capacity)
            hall.projector = False if projector == None else True
            hall.save()
            request.session['message'] = f'{name} was edited'
            return redirect('halls')
        else:
            message = 'Something went wrong. Hall was not added.'
            return render(request, 'edit_halls.html', context={'hall': hall, 'message': message})


def show_reservations(request):
    if 'message' in request.session:
        del request.session['message']
    reservations = Reservation.objects.all().order_by('id')
    if request.method == 'GET':
        if request.session.get('order_by_res'):
            if request.session.get('order_by_res') == 2:
                reservations = Reservation.objects.all().order_by('-date')
            elif request.session.get('order_by_res') == 1:
                reservations = Reservation.objects.all().order_by('date')
        return render(request, 'show_reservations.html', context={'reservations': reservations})
    else:
        if request.POST.get('sort') == "2":
            reservations = Reservation.objects.all().order_by('-date')
            request.session['order_by'] = 2
        elif request.POST.get('sort') == "1":
            reservations = Reservation.objects.all().order_by('date')
            request.session['order_by'] = 1
        else:
            request.session['order_by'] = 0
        return render(request, 'show_reservations', context={'reservations': reservations})


def add_reservation(request, id):
    if 'message' in request.session:
        del request.session['message']
    hall = ConferenceHall.objects.get(pk=id)
    reservations = Reservation.objects.filter(date__gte=datetime.today().date())
    hall_res = []
    for r in reservations:
        if r.hall == hall:
            hall_res.append(f'{r.date}: {r.description}')
    form = ReservationForm()
    if request.method == 'GET':
        return render(request, 'add_reservation.html', context={'form': form, 'hall': hall, 'hall_res': hall_res})
    else:
        description = request.POST.get('description')
        date = datetime.strftime(request.POST.get('date'), '%Y-%m-%d')
        if date.date() >= datetime.today().date():
            if len(reservations) != 0:
                for r in reservations:
                    if r.hall == hall and r.date == date.date():
                        message = 'This hall is reserved for this date'
                        return render(request, 'add_reservation.html', context={'form': form, 'message': message, 'hall': hall})
            reservation = Reservation.objects.create(date=date, hall=hall, description=description)
            request.session['message'] = f'{reservation} added to database'
            return redirect('halls')
        else:
            message = 'The date is wrong. Try again.'
            return render(request, 'add_reservation.html', context={'form': form, 'message': message, 'hall': hall})


def new_reservation(request):
    if 'message' in request.session:
        del request.session['message']
    form = ReservationForm()
    halls = ConferenceHall.objects.all()
    if request.method == 'GET':
        return render(request, 'new_reservation.html', context={'form': form, 'halls': halls})
    else:
        hall = ConferenceHall.objects.get(pk=request.POST.get('hall'))
        description = request.POST.get('description')
        date = datetime.strftime(request.POST.get('date'), '%Y-%m-%d')
        if date >= datetime.today():
            reservations = Reservation.objects.filter(date__gte=datetime.today().date())
            if len(reservations) != 0:
                for r in reservations:
                    if r.hall == hall and r.date == date.date():
                        message = 'This hall is already reserved.'
                        return render(request, 'new_reservation.html', context={'form': form, 'message': message, 'hall': hall})
            reservation = Reservation.objects.create(date=date, hall=hall, description=description)
            request.session['message'] = f'{reservation} added'
            return redirect('halls')
        else:
            message = 'Something went wrong.'
            return render(request, 'new_reservation.html', context={'form': form, 'message': message, 'hall': hall})


def edit_reservation(request, id):
    if 'message' in request.session:
        del request.session['message']
    res = Reservation.objects.get(pk=id)
    reservations = Reservation.objects.all()
    halls = ConferenceHall.objects.exclude(pk=res.get_hall_id())
    if request.method == 'GET':
        return render(request, 'edit_reservation.html', context={'res': res, 'halls': halls, 'reservations': reservations})
    else:
        hall = ConferenceHall.objects.get(pk=request.POST.get('hall'))
        description = request.POST.get('description')
        date = datetime.strftime(request.POST.get('date'), '%Y-%m-%d')
        if date.date() >= datetime.today().date():
            if len(reservations) != 0:
                for r in reservations:
                    if r.hall == hall and r.date == date.date():
                        message = 'This hall is already reserved.'
                        return render(request, 'edit_reservation.html',
                                      context={'reservations': reservations, 'message': message, 'halls': halls})
                    elif r.hall == res.hall and res.date != date.date():
                        if res.hall == r.hall and r.date == date.date():
                            message = 'This hall is reserved'
                            return render(request, 'edit_res.html', context={'res': res, 'halls': halls, 'message': message})
            res.hall = hall
            res.date = date
            res.description = description
            res.save()
            request.session['message'] = f'{reservations} added'
            return redirect('halls')
        else:
            message = 'Something went wrong.'
            return render(request, 'edit_reservation.html', context={'res': res, 'message': message, 'halls': halls})


def delete_reservation(request, id):
    if 'message' in request.session:
        del request.session['message']
    res = Reservation.objects.get(pk=id)
    res.delete()
    request.session['message'] = f"Reservation number {id} for {res.hall} has been deleted."
    return redirect('halls')


def search_halls(request):
    url = 'search/'
    if request.method == 'GET':
        return render(request, 'search_halls.html')
    else:
        if request.POST.get('name'):
            name = request.POST.get('name')
            hall = ConferenceHall.objects.get(name=name)
            if hall:
                url += f'{hall.id}/'
            else:
                message = 'There is no such hall.'
                return render(request, 'search_halls.html', context={'message': message})
        else:
            url += '0/'
        if request.POST.get('capacity'):
            capacity = request.POST.get('capacity')
            url += f'{capacity}/'
        else:
            url += '0/'
        if request.POST.getlist('projector'):
            url += '1'
        else:
            url += '0'
        return redirect(url)


def find_halls(request, hall_id, capacity, projector):
    halls = ConferenceHall.objects.all()
    reservations = Reservation.objects.all()
    if int(hall_id) != 0:
        halls = halls.filter(Q(pk=int(hall_id)))
    if int(capacity) != 0:
        halls = halls.exclude(capacity__lte=int(capacity)-1)
    if int(projector) != 0:
        halls = halls.exclude(projector=False)
    else:
        halls = halls.exclude(projector=True)
    if len(halls) != 0:
        message = 'In accordance to your search conditions'
    else:
        message = "No hall meets your criteria"
    if request.method == 'GET':
        if request.session.get('order_by'):
            if request.session.get('order_by') == 2:
                halls = halls.order_by('-capacity')
            elif request.session.get('order_by') == 1:
                halls = halls.order_by('capacity')
        return render(request, 'show_halls_details.html', context={'halls': halls, 'reservations': reservations, 'message': message})
    else:
        if request.POST.get('sort') == "2":
            halls = halls.order_by('-capacity')
            request.session['order_by'] = 2
        elif request.POST.get('sort') == "1":
            halls = halls.order_by('capacity')
            request.session['order_by'] = 1
        else:
            request.session['order_by'] = 0
        return render(request, 'show_halls_details.html', context={'halls': halls, 'reservations': reservations})


def search_reservation(request):
    url = 'search_res/'
    if request.method == 'GET':
        halls = ConferenceHall.objects.all()
        return render(request, 'search_reservation.html', context={'halls': halls})
    else:
        if request.POST.get('date'):
            date = datetime.strftime(request.POST.get('date'), '%Y-%m-%d')

            if date:
                url += f'{date.date()}/'
            else:
                message = 'This is not valid date. Please try again.'
                return render(request, 'search_reservation.html', context={'message': message})
        else:
            url += '0000-00-00/'
        if request.POST.get('hall_id'):
            hall_id = request.POST.get('hall_id')
            url += f'{int(hall_id)}/'
        else:
            url += '0/'
        if request.POST.get('word') and request.POST.get('word') != '':
            word = request.POST.get('word').lower()
            url += f'{word}'
        else:
            url += '0'
        return redirect(url)


def find_res(request, date, hall_id, word):
    reservations = []
    if hall_id != '0':
        hall = ConferenceHall.objects.get(pk=int(hall_id))
        reservations = Reservation.objects.filter(Q(hall=hall))
    if date != '0000-00-00':
        date = datetime.strptime(date, '%Y-%m-%d')
        if hall_id != '0':
            reservations = reservations.exclude(date__lt=date.date())
        else:
            reservations = Reservation.objects.filter(date__gte=date.date())
    if word != "0":
        if hall_id != '0' or date != '0000-00-00':
            for r in reservations:
                if word not in r.description.casefold():
                    reservations = reservations.exclude(pk=r.id)
        else:
            reservations = Reservation.objects.filter(description__icontains=word)
    if word == '0' and hall_id == '0' and date == '0000-00-00':
        reservations = Reservation.objects.all()
    if len(reservations) != 0:
        message = 'According to your search conditions.'
    else:
        message = 'There is no reservations that meets these criteria.'
    if request.method == 'GET':
        if request.session.get('order_by_r'):
            if request.session.get('order_by_r') == 2:
                reservations = reservations.order_by('-date')
            elif request.session.get('order_by_r') == 1:
                reservations = reservations.order_by('date')
        return render(request, 'show_reservations.html', context={'reservations': reservations, 'message': message})
    else:
        if request.POST.get('sort') == "2":
            reservations = reservations.order_by('-date')
            request.session['order_by_r'] = 2
        elif request.POST.get('sort') == "1":
            reservations = reservations.order_by('date')
            request.session['order_by_r'] = 1
        elif request.POST.get('sort') == "0":
            reservations = reservations.order_by('id')
            request.session['order_by_r'] = 0
        return render(request, 'show_reservations.html', context={'reservations': reservations, 'message': message})




