from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join/', views.join_fund, name='join'),
    path('participants/', views.participants, name='participants'),
    path('bidding/', views.bidding, name='bidding'),
    path('start-round/', views.start_round, name='start_round'),
    path('end-round/', views.end_round, name='end_round'),
]
