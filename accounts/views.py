from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_email_verification import send_email, verify_view, verify_token
from yaml import serialize, serialize_all


from accounts.forms import RegistrationForm, AccountAuthenticationForm

# Create your views here.


def registration_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    context = {}
    context["email"] = ""
    context["username"] = ""
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            account.is_active = False
            send_email(account)
            return render(
                request, "accounts/check_email_prompt.html", {
                    "account": account}
            )
        else:
            context["registration_form"] = form
    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "accounts/register.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")
    else:
        return HttpResponse("Cannot logout when you aren't logged in")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("index")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("index")

    else:
        form = AccountAuthenticationForm()
    context["login_form"] = form
    return render(request, "accounts/login.html", context)


def resend_email(request):
    if request.POST:
        email = request.POST.get("email")
        raw_password = request.POST.get('password')
        try:
            user = get_user_model().objects.get(email=email)
            original_active_value = user.is_active
            user.is_active = True
            user.save()
            account = authenticate(email=email, password=raw_password)
            account.is_active = original_active_value
            account.save()
        except:
            account = None
        if account:
            if not account.is_active:
                send_email(account)
                return render(
                    request, "accounts/check_email_prompt.html", {
                        "account": account}
                )
            else:
                return HttpResponse("Account already verified")
        else:
            return HttpResponse("Email or password incorrect", status=404)

    return render(
        request,
        "accounts/confirm_template.html",
        {"success": False, "username": "", "invaid_token_display": False},
    )


@verify_view
def confirm(request, token):
    success, user = verify_token(token)
    try:
        username = user.username
    except:
        username = ""
    return render(
        request,
        "accounts/confirm_template.html",
        {"success": success, "username": username, "invaid_token_display": True},
    )

