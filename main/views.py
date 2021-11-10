from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Content, UserProfile
from django.http import HttpResponse
from .forms import ContentForm, LoginForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required

from django.conf import settings

# Login materials
from django.contrib.auth import login, authenticate, logout


def index_page(request):
    qs = Content.objects.all().order_by("-last_updated")
    diction = {
        "posts": qs
    }
    return render(request, "main/index.html", context=diction)


@login_required
def content_creation(request):
    print(request.user)  # Current User that is logged in
    form = ContentForm()
    if request.method == "POST":
        form = ContentForm(data=request.POST)
        form.instance.user = request.user  # We are explicitely setting user of the form to current user

        if form.is_valid():
            obj = form.save()
            print("Saved")
            return redirect("content_detail", id=obj.id)

        messages.error(request, "Invalid data provided")
        print("Invalid data")

    context = {
        "form": form,
    }

    return render(request, "main/content_create.html", context)


@login_required
def content_update(request, pk):
    obj = Content.objects.get(pk=pk)

   # Give a permission denied when other user try to update content

    form = ContentForm(instance=obj)

    if request.method == "POST":
        form = ContentForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            print("Saved")
            return HttpResponse("<h1>Congrats</h1>")  # task to redirect to detail

        messages.error(request, "Invalid data provided")
        print("Invalid data")

    context = {
        "form": form,
    }
    return render(request, "main/content_create.html", context)


@login_required
def content_delete(request, number):
    try:
        obj = Content.objects.get(id=number)
    except ObjectDoesNotExist:
        return HttpResponse(f"Content with this Id ({number}) is not found To delete")

    # Give a permission denied when other user try to delete content


    if request.method == "POST":
        obj.delete()
        # messages.success(request, "Content has been deleted")
        return redirect("index_page")

    context = {
        "post_obj": obj
    }

    return render(request, "main/content_delete.html", context)



def content_detail(request, id):
    try:
        obj = Content.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(f"Content with this Id ({id}) is not found")

    context = {
        "post_obj": obj
    }

    return render(request, "main/content_detail.html", context)



def login_user(request):
    user = request.user  # Current user that is active in this session
    if user.is_authenticated:
        raise PermissionDenied("User is Authenticated")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_obj = authenticate(username=username, password=password)  # returns user object
            login(request, user_obj)
            print("User has been logged in ", user_obj)
            next = request.GET.get("next")
            print(next)
            if next:
                return redirect(next)
            return redirect("/")

    context = {
        "form": form
    }

    return render(request, "user/login.html", context)


@login_required
def logout_user(request):
    logout(request)
    print("Logged out")
    return redirect(settings.LOGIN_URL)

