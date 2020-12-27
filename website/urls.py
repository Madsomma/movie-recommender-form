from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('choice', views.choice, name='choice'),
    path('recommendation', views.recommendation, name='recommendation'),
    path('end', views.end, name='end')
]
