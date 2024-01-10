from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserLogin, UserRegister

urlpatterns = [
    # api (drf)
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),

    # function-based view(django)
    path('user-login/', UserLogin , name='user-login'),
    path('user-register/', UserRegister , name='user-register'),
]