from django.urls import path
from .views import Requests, ProductDeleteView

app_name = 'the_one'

urlpatterns = [
    path('', Requests.as_view(), name='Requests'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='ProductDelete')
]
