from django.shortcuts import render

from .models import *


def home(request):
    template_to_load    =   'pages/home.html'
    movie_list = Movie.objects.filter()
    print("movie_list")
    for movie in movie_list:
        print("movie "+str(movie))
    context             =   {
        "movie_list" : movie_list,
    }
    return render(request, template_to_load, context = context)

def movie_detail(request, movie_id):
    template_to_load    =   'pages/movie_detail.html'
    movie_info = Movie.objects.get(id = movie_id)
    print("movie_info "+str(movie_info))
    context             =   {
        "movie_info" : movie_info,
    }
    return render(request, template_to_load, context = context)

def book_ticket(request,movie_id):
    template_to_load    =   'pages/book_ticket.html'
    x = []
    screening = Screening.objects.filter(movie_id = movie_id)
    for screens in screening:
        y = {
                'theatre_name' : Theatre.objects.get(id = screens.theatre_id.id),
                'screen' : Screen.objects.get(id = screens.screen_id.id), #screen.id
                'date' : screens.date,
                'time' : screens.start_time,
                'screening_id' : screens.id
            }
        x.append(y)
        print("x = "+str(x))
    context             =   {
        "screening" : screening,
        "screen" : x,
        }
    return render(request, template_to_load, context = context)

def seat_choice(request, screening_id, screen_id):
    template_to_load    =   'pages/seat_choice_ticket.html'
    screen_seat = ScreenSeat.objects.filter(id = screen_id)
    seats_available = ""
    seats_available = ShowSeat.objects.filter(status = "available", screening_id = screening_id)
    print("seats_available "+str(seats_available))
    context             =   { "seats_available" : seats_available}
    return render(request, template_to_load,context = context )
