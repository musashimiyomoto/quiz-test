from django.urls import path

from users.views import (LogIn,
                         SignUp,
                         user_logout)

urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
]
