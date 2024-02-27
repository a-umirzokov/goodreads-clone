from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UserUpdateForm


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('books:home')
        else:
            return render(request, 'users/login.html', {'form': login_form})


class Register(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
                   'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(
            data=request.POST,
            files=request.FILES
        )
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out')
        return redirect('books:home')


class UserUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        update_form = UserUpdateForm(instance=user)
        context = {
            'form': update_form
        }
        return render(request, 'users/update.html', context)

    def post(self, request):
        user = request.user
        update_form = UserUpdateForm(
            data=request.POST,
            instance=user,
            files=request.FILES
        )
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('users:profile')
        else:
            context = {
                'form': update_form
            }
            return render(request, 'users/update.html', context)
