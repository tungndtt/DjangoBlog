from django.shortcuts import render, redirect
from .form import RegisterForm, UserUpdateForm, ProfileUpdateForm, ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import send_mail


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', context={'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        print(request.POST)
        print(request.FILES)
        if userForm.is_valid():
            userForm.save()
        if profileForm.is_valid():
            print('saved new profile pic!')
            profileForm.save()
        return redirect('Profile')
    else:
        userForm = UserUpdateForm()
        profileForm = ProfileUpdateForm()
        return render(request, 'user/profile.html', context={'userForm': userForm, 'profileForm': profileForm})


@login_required
def viewProfile(request, **kwargs):
    username = list(kwargs.values())[0]
    user = User.objects.filter(username=username).first()
    return render(request, 'user/viewProfile.html', context={'user': user})


def sendMail(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email=email)
        msg = 'Hi {},\n ' \
              'this url links to password reset confirmation:\n ' \
              'http://localhost:8000/reset-password/reset/{}/{}/' \
            .format(user.username, user.pk, user.password)
        send_mail(subject='Reset password', message=msg, from_email='tungndtt224@gmail.com',
                  recipient_list=[email], fail_silently=False)
        return render(request, 'user/request_sent.html')
    else:
        return render(request, 'user/reset_password.html')


def resetPassword(request, **kwargs):
    if request.method == 'POST':
        user = User.objects.get(pk=kwargs['pk'], password=kwargs['hash_password'])
        reset = ResetPasswordForm(request.POST, instance=user)
        if reset.is_valid():
            reset.save()
            return redirect('Login')
    reset = ResetPasswordForm()
    return render(request, 'user/reset_password_confirmation.html', context={'reset': reset})
