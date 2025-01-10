from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Yard
from .forms import YardForm
# Home view

def home(request):
    if request.user.is_authenticated:
        form = YardForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                yards = form.save(commit=False)
                yards.user = request.user
                yards.save()
                messages.success(request, ("It is done!"))
                return redirect('home')

        yards = Yard.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"yards":yards, "form":form})
        
    else:
        yards = Yard.objects.all().order_by("-created_at") 
        return render(request, 'home.html', {"yards":yards})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        yards = Yard.objects.filter(user_id=pk).order_by("-created_at")
        # Post Form Logic
        if request.method == "POST":
            # get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            # follow or unfollow profile
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

            current_user_profile.save()

        return render(request, 'profile.html', {"profile":profile, "yards":yards})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')