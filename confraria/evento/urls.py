from django.urls import path
from .views import EventoListView, EventoDetail, receber_doacao


urlpatterns = [
    path('list/', EventoListView.as_view(), name='evento_list'),
    path('detail/<int:pk>/', EventoDetail.as_view(), name='evento_detail'),
    path(
        'receber_doacao/evento/<int:evento_pk>/pessoa/<int:pessoa_pk>/',
        receber_doacao, name='receber_doacao'
    ),
]
