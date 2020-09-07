from django.urls import path
from . import views

urlpatterns = [
    path('DoneList/', views.DoneList),
    path('IngList/', views.IngList),
    path('ShowList/', views.ShowList),
    path('Accept/', views.Accept),
    path('WithDraw/', views.WithDraw),
    path('Submit/', views.Submit),
    path('Start/', views.Start),
]