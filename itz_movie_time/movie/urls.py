from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import book_ticket, home, movie_detail, seat_choice

urlpatterns = [
    path('', home, name ='home'),
    path('movie-detail/<movie_id>', movie_detail, name ='movie_detail'),
    path('book-ticket/<movie_id>', book_ticket, name ='book_ticket'),
    path('seat-choice/<screening_id>/<screen_id>', seat_choice, name ='seat_choice'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
