from django.urls import path

from .views import AccountungView, UserView

urlpatterns = [
    path('accounting/', AccountungView.as_view(), name='index'),
    path('accounting/users/<owner_name>/', UserView.as_view(), name='users'),
]
