from django.http import HttpResponse #email
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticate_user
from warehouse.models import Customer

from django.contrib.auth.decorators import login_required
#change password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

#email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.
@unauthenticate_user
def RegisterUser(request):
    form = RegistrationForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email already used', extra_tags='reg')
                return redirect('register')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('account/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')

    context = {'form': form}
    return render(request, 'account/signup_page.html', context)

@unauthenticate_user
def LoginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or Password is incorrect', extra_tags='login')

    context = {}
    return render(request, 'account/login_page.html', context)

def Logout(request):
    logout(request)
    return redirect('login')


#change password
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!', extra_tags='change_pass')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags='change_pass')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'account/change_password.html', context)


#eamil
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        username = user.username
        email = user.email

        group = Group.objects.get(name='customer')
        user.groups.add(group)
        customer = Customer.objects.create(user=user, name=username, email=email)

        messages.success(request, 'Account is created for  ' + username, extra_tags='login')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')