from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('talk/<category>', views.talk, name='talk'),
]
