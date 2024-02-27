from django import forms

from users.models import CustomUser


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

# class UserCreateForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=30)
#     first_name = forms.CharField(label='First name', max_length=30)
#     last_name = forms.CharField(label='Last name', max_length=30)
#     email = forms.EmailField(label='Email')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#
#     def save(self):
#         username = self.cleaned_data['username']
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#         user = User.objects.create_user(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#         )
#         user.set_password(password)
#         user.save()
#
#         return user
