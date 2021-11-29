from django.urls import path
from .views import EventoListView, EventoDetail


urlpatterns = [
    path('list/', EventoListView.as_view(), name='evento_list'),
    path('detail/<int:pk>/', EventoDetail.as_view(), name='evento_detail'),
]