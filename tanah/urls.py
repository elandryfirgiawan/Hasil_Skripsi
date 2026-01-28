from django.urls import path
from .views import form_input

urlpatterns = [
    path('', form_input, name='form'),
]
