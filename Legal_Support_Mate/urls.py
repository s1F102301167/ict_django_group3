from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('talk/<category>', views.talk, name='talk'),
    path('clear/<category>', views.clear, name='clear'),
    path('stream/<category>', views.stream, name='stream'),
]
