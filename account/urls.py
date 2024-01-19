from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserLogoutView, UserLogin, UserRegister, user_list

urlpatterns = [
    # api (drf)
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # function-based view(django)
    path('user-login/', UserLogin , name='user-login'),
    path('user-register/', UserRegister , name='user-register'),
    path('', user_list, name='user_list')
]