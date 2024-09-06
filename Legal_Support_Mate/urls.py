from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('talk/<str:category>', views.talk, name='talk'),
    path('sse/<str:category>', views.sse_view, name='sse'),
    path('clear/<category>', views.clear, name='clear'),
]
