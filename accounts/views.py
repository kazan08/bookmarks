from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

from .models import Profile


# def user_login(request):
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            cd = form.cleaned_data
#            user = authenticate(request,
#                                username=cd['username'],
#                                password=cd['password'])
#            if user is not None:
#                if user.is_active:
#                    login(request, user)
#                    return HttpResponse('Вы успешно вошли в систему')
#                else:
#                    return HttpResponse('Неактивный аккаунт')
#            else:
#                return HttpResponse('Неверный логин/пароль')
#    else:
#        form = LoginForm()
#    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохранить объект User
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлён успешно')
        else:
            messages.error(request, 'Ошибка обновления профиля')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                    'accounts/edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard'})
