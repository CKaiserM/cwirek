from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, YardSerializer, ProfileSerializer
from .models import Yard, Profile, User
from .forms import YardForm, SignUpForm, UpdateUserForm, ProfileMiscForm

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

"""
class GroupViewSet(viewsets.ModelViewSet):
    
    API endpoint that allows groups to be viewed or edited.
    
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
"""
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
"""
    YardView()
    return render(request, 'home.html', {})
"""
class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request):
        yards = Yard.objects.all().order_by("-created_at")
        form = YardForm(request.POST or None)
        yard_user = Profile.objects.get(user_id=request.user)
        
        
        return Response({"yards":yards, "form":form, 'yard_user': yard_user})
    
    def post(self, request):
        form = YardForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                yards = form.save(commit=False)
                yards.user = request.user
                yards.save()
                messages.success(request, ("It is done!"))
                return redirect('home')

class PostYardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'yard/post.html'

    def get(self, request):
        yards = Yard.objects.all()
        form = YardForm(request.POST or None)
        return Response({"yards":yards, "form":form})
    
    def post(self, request, pk):
        form = YardForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                yards = form.save(commit=False)
                yards.user = request.user
                yards.save()
                messages.success(request, ("It is done!"))
                return redirect('home')

class YardViewSet(ListCreateAPIView):
    queryset = Yard.objects.all()
    serializer_class = YardSerializer
    #permission_classes = [permissions.IsAuthenticated]

class YardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'yard/yard.html'

    def get(self, request):
        queryset = Yard.objects.all()
        return Response({'yards':queryset})

class ProfileViewSet(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileView(APIView):
    renderer_classes= [TemplateHTMLRenderer]
    template_name = 'profile/profile.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        profile = Profile.objects.get(user_id=pk)
        yards = Yard.objects.filter(user_id=pk).order_by("-created_at")  
        return Response({"profile":profile, "yards":yards})
    
    def post(self, request, pk):
        """
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile_list')
        """
        profile = Profile.objects.get(user_id=pk)
        yards = Yard.objects.filter(user_id=pk).order_by("-created_at")  
        current_user_profile = request.user.profile
        action = request.POST['follow']
        # follow or unfollow profile
        if action == "unfollow":
            current_user_profile.follows.remove(profile)
        elif action == "follow":
            current_user_profile.follows.add(profile)

        current_user_profile.save()
        return Response({"profile":profile, "yards":yards})

   
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile/profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
"""    
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

        return render(request, 'profile/profile.html', {"profile":profile, "yards":yards})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
"""
def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')

def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles":profiles})
        else:
            messages.success(request, ("That is not your profile page"))
            return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'profile/follows.html', {"profiles":profiles})
        else:
            messages.success(request, ("That is not your profile page"))
            return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    

def login_user(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("Wrong password or username"))
            return redirect('login')
    else:
        return render(request, 'profile/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #second_name = form.cleaned_data['second_name']
            #email = form.cleaned_data['email']
            
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered"))
            return redirect('home')
        
    return render(request, 'profile/register.html', {'form':form})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfileMiscForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "profile/update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
     
def yard_like(request, pk):
    if request.user.is_authenticated:  
        yard = get_object_or_404(Yard, id=pk)
        
        # if dislike exists, remove
        if yard.dislikes.filter(id=request.user.id):
            yard.dislikes.remove(request.user)

        if yard.likes.filter(id=request.user.id):
           yard.likes.remove(request.user)
        else:
            yard.likes.add(request.user)  
    else:
        return redirect('home')    
    return redirect(request.META.get("HTTP_REFERER"))

def yard_dislike(request, pk):
    if request.user.is_authenticated:  
        yard = get_object_or_404(Yard, id=pk)

        # if like exists, remove
        if yard.likes.filter(id=request.user.id):
            yard.likes.remove(request.user)  
            
        if yard.dislikes.filter(id=request.user.id):
           yard.dislikes.remove(request.user)
        else:
            yard.dislikes.add(request.user)

    else:
        return redirect('home')    
    return redirect(request.META.get("HTTP_REFERER"))

def yard_show(request, pk):
    yard = get_object_or_404(Yard, id=pk)
    
    if yard:
        return render(request, "yard/show_yard.html", {'yard':yard})
    else:
        messages.success(request, ("This post does not exist"))
        return redirect('home')

    #if request.user.is_authenticated:
def yard_delete(request, pk):
    if request.user.is_authenticated:  
        yard = get_object_or_404(Yard, id=pk)
        #check ownership
        if request.user.username == yard.user.username:
            #delete
            yard.delete()
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("not your yard"))
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("Please log in."))
        return redirect('login')

def yard_edit(request, pk):
    if request.user.is_authenticated:
        yard = get_object_or_404(Yard, id=pk)
        if request.user.username == yard.user.username:  
            
            form = YardForm(request.POST or None, instance=yard)

            #edit post
            if request.method == "POST":
                if form.is_valid():
                    yards = form.save(commit=False)
                    yards.user = request.user
                    yards.save()
                    messages.success(request, ("It is done!"))
                    return redirect('home')
            else:
                return render(request, "yard/edit_yard.html", {'form':form, 'yard':yard})
        else:
            messages.success(request, ("not your yard"))
            return redirect('home')
    else:
        messages.success(request, ("Please log in."))
        return redirect('login')

def yard_search(request):
    if request.method == "POST":
        #grab search phrase
        search = request.POST['search']
        #search the DB
        searched = Yard.objects.filter(body__contains=search)
        return render(request, "search/search_yard.html", {'search':search, 'searched':searched})
    else:
        return render(request, "search/search_yard.html", {})

def user_search(request):
    if request.method == "POST":
        #grab search phrase
        search = request.POST['search']
        #search the DB
        searched = User.objects.filter(username__contains=search)
        return render(request, "search/search_users.html", {'search':search, 'searched':searched})
    else:
        messages.success(request, ("Sorry, nothing found"))
        return render(request, "search/search_users.html", {})
    
def search(request):
    if request.method == "POST":
        #grab search phrase
        search = request.POST['search']
        #search the DB
        found_user = User.objects.filter(username__contains=search)
        found_yard = Yard.objects.filter(body__contains=search)
        return render(request, "search/search.html", {'search':search, 'found_user':found_user, 'found_yard':found_yard})
    else:
        messages.success(request, ("Sorry, nothing found"))
        return render(request, "search/search.html", {})

