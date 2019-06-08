from django.urls import path
from .views import Requests

app_name = 'the_one'

urlpatterns = [
    path('', Requests.as_view(), name='Requests')
]
