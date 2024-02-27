from django.urls import path
from users import views as v

app_name = 'users'
urlpatterns = [
    path('login/', v.LoginView.as_view(), name='login'),
    path('register/', v.Register.as_view(), name='register'),
    path('profile/', v.ProfileView.as_view(), name='profile'),
    path('profile/update/', v.UserUpdateView.as_view(), name='update'),
    path('logout/', v.LogoutView.as_view(), name='logout'),
]
