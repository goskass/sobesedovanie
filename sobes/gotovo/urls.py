from django.urls import path
from . import views

urlpatterns = [
    path('', views.word_counter, name='word_counter'),
]
