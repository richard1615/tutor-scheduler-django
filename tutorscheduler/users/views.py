from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from scheduler.models import Session
from users.models import Teacher
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You can now login"
            )
            return redirect("login")
    else:  # displays empty form initially
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    # user_group = request.user.groups.values_list("name", flat=True).first()
    # this give a QuerySet<'Teacher'>
    context = {
        "user_group": "Teacher" if user.groups.filter(name="teacher") else "Student",
        "user_sessions": Session.objects.filter(student=user),
        "teacher": Teacher.objects.filter(teacher=user).first(),
        "teacher_sessions": Session.objects.filter(weekday="MONDAY"),
    }
    return render(request, "users/profile.html", context)


@login_required
def editprofile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated.")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/editprofile.html", context)

