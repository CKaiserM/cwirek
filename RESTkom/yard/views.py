from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

import after_response

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, YardSerializer, ProfileSerializer
from .models import Yard, Profile, User, CommentYard, ReplyToYardComment, Notifications
from .forms import YardForm, SignUpForm, UpdateUserForm, ProfileMiscForm, CommentYardForm, ReplyToCommentForm

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request):
        yards = Yard.objects.all().order_by("-created_at")
        if request.user.is_authenticated:
            form = YardForm(request.POST or None, request.FILES or None)
            commentform = CommentYardForm(request.POST or None)
            replyToCommentForm = ReplyToCommentForm(request.POST or None)
            yard_user = request.user
            unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
            return Response({"yards":yards, "form":form, 'yard_user': yard_user, 'commentform':commentform, "replyToCommentForm":replyToCommentForm, 'unread_notifications': unread_notifications})
        else:
            return Response({"yards":yards})
    
    def post(self, request):
        if request.user.is_authenticated:
            form = YardForm(request.POST or None, request.FILES or None)
            if request.method == "POST":
                if form.is_valid():
                    yards = form.save(commit=False)
                    yards.user = request.user
                    yards.save()
                    messages.success(request, ("It is done!"))
                    return redirect('home')
        else:
            messages.success(request, ("Please log in"))
            return redirect('login')

class PostYardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'yard/post.html'

    def get(self, request):
        yards = Yard.objects.all()
        form = YardForm(request.POST or None, request.FILES or None)
        return Response({"yards":yards, "form":form})
    
    def post(self, request, pk):
        form = YardForm(request.POST or None, request.FILES or None)
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
        yards = Yard.objects.all()
        unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
        return Response({'yards':yards, 'unread_notifications':unread_notifications})
    
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
                
                form = YardForm(request.POST or None, request.FILES or None, instance=yard)

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
        unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
        yards = Yard.objects.filter(user_id=pk).order_by("-created_at")
        form = YardForm(request.POST or None, request.FILES or None)
        commentform = CommentYardForm(request.POST or None)
        replyToCommentForm = ReplyToCommentForm(request.POST or None)          
        return Response({"profile":profile, "yards":yards, "form":form, 'commentform':commentform, "replyToCommentForm":replyToCommentForm, 'unread_notifications':unread_notifications})
    
    def post(self, request, pk):
        profile = Profile.objects.get(user_id=pk)
        yards = Yard.objects.filter(user_id=pk).order_by("-created_at")  
        current_user_profile = request.user.profile

        form = YardForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                yards = form.save(commit=False)
                yards.user = request.user
                yards.save()
                messages.success(request, ("It is done!"))
                return redirect(request.META.get("HTTP_REFERER"))

        action = request.POST['follow']
        # follow or unfollow profile
        if action == "unfollow":
            current_user_profile.follows.remove(profile)
        elif action == "follow":
            current_user_profile.follows.add(profile)

        current_user_profile.save()
        return Response({"profile":profile, "yards":yards})
    
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

class ProfileListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/profile_list.html'

    def get(self, request):
        if request.user.is_authenticated:
            profiles = Profile.objects.exclude(user=request.user)
            return Response({"profiles":profiles})
        else:
            messages.success(request, ("You must be logged in to view this page..."))
            return redirect('home')           

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'profile/reset_password.html'
    email_template_name = 'profile/password_reset_email.html'
    subject_template_name = 'profile/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

    success_url = reverse_lazy('profile')

# Comment class

class PostCommentView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    model = CommentYard
    template_name = 'yard/comment.html'
    fields = '__all__'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if request.user.is_authenticated:
            commentform = CommentYardForm(request.POST or None)
            commentYard = CommentYard.objects.all().order_by("-created_at")
            unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
            return Response({'commentYard': commentYard, "commentform":commentform, 'unread_notifications':unread_notifications})

    def post(self, request, pk):
        if request.user.is_authenticated:
            commentform = CommentYardForm(request.POST or None)
            yard = get_object_or_404(Yard, pk=pk)
            if request.method == "POST":
                if commentform.is_valid():
                    comment = commentform.save(commit=False)
                    comment.yard = yard
                    comment.user = request.user
                    comment.save()
                    messages.success(request, ("It is done!"))
                    return redirect('home')

    def comment_like(request, pk):
        if request.user.is_authenticated:  
            comment = get_object_or_404(CommentYard, id=pk)
            
            # if dislike exists, remove
            if comment.dislikes.filter(id=request.user.id):
                comment.dislikes.remove(request.user)

            if comment.likes.filter(id=request.user.id):
                comment.likes.remove(request.user)
            else:
                comment.likes.add(request.user)  
        else:
            return redirect('home')    
        return redirect(request.META.get("HTTP_REFERER"))

    def comment_dislike(request, pk):
        if request.user.is_authenticated:  
            comment = get_object_or_404(CommentYard, id=pk)

            # if like exists, remove
            if comment.likes.filter(id=request.user.id):
                comment.likes.remove(request.user)  
                
            if comment.dislikes.filter(id=request.user.id):
                comment.dislikes.remove(request.user)
            else:
                comment.dislikes.add(request.user)

        else:
            return redirect('home')    
        return redirect(request.META.get("HTTP_REFERER"))

    def comment_show(request, pk):
        comment = get_object_or_404(CommentYard, id=pk)
        
        if comment:
            return render(request, "yard/show_yard.html", {'comment':comment})
        else:
            messages.success(request, ("This post does not exist"))
            return redirect('home')

        #if request.user.is_authenticated:
    
    def comment_delete(request, pk):
        if request.user.is_authenticated:  
            comment = get_object_or_404(CommentYard, id=pk)
            #check ownership
            if request.user.username == comment.user.username:
                #delete
                comment.delete()
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                messages.success(request, ("not your comment"))
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("Please log in."))
            return redirect('login')

    def comment_edit(request, pk, pc):
        if request.user.is_authenticated:
            comment = get_object_or_404(CommentYard, id=pc)
            if request.user.username == comment.user.username:  
                
                commentform = YardForm(request.POST or None, request.FILES or None, instance=comment)
                yard = get_object_or_404(Yard, pk=pk)
                #edit comment
                if request.method == "POST":
                    if commentform.is_valid():
                        comments = commentform.save(commit=False)
                        comments.user = request.user
                        comments.yard = yard
                        comments.save()
                        messages.success(request, ("It is done!"))
                        return redirect('home')
                else:
                    return render(request, "yard/edit_comment.html", {'commentform':commentform, 'comment':comment})
            else:
                messages.success(request, ("not your comment"))
                return redirect('home')
        else:
            messages.success(request, ("Please log in."))
            return redirect('login')

# Reply to comment class

class PostReplyView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    model = ReplyToYardComment
    template_name = 'yard/reply.html'
    fields = '__all__'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        replyToCommentForm = ReplyToCommentForm(request.POST or None)
        replyToComment = ReplyToYardComment.objects.all().order_by("-created_at")
        unread_notifications = Notifications.objects.filter(user=request.user, read=False).count()
        return Response({'replyToComment': replyToComment, "replyToCommentForm":replyToCommentForm, 'unread_notifications':unread_notifications})

    def post(self, request, pk):
        replyToCommentForm = ReplyToCommentForm(request.POST or None)
        comment = get_object_or_404(CommentYard, pk=pk)
        if request.method == "POST":
            if replyToCommentForm.is_valid():
                reply = replyToCommentForm.save(commit=False)
                reply.comment = comment
                reply.user = request.user
                reply.save()
                messages.success(request, ("Reply added"))
                return redirect('home')

    def reply_like(request, pk):
        if request.user.is_authenticated:  
            reply = get_object_or_404(ReplyToYardComment, id=pk)
            
            # if dislike exists, remove
            if reply.dislikes.filter(id=request.user.id):
                reply.dislikes.remove(request.user)

            if reply.likes.filter(id=request.user.id):
                reply.likes.remove(request.user)
            else:
                reply.likes.add(request.user)  
        else:
            return redirect('home')    
        return redirect(request.META.get("HTTP_REFERER"))

    def reply_dislike(request, pk):
        if request.user.is_authenticated:  
            reply = get_object_or_404(ReplyToYardComment, id=pk)

            # if like exists, remove
            if reply.likes.filter(id=request.user.id):
                reply.likes.remove(request.user)  
                
            if reply.dislikes.filter(id=request.user.id):
                reply.dislikes.remove(request.user)
            else:
                reply.dislikes.add(request.user)

        else:
            return redirect('home')    
        return redirect(request.META.get("HTTP_REFERER"))

    def reply_show(request, pk):
        reply = get_object_or_404(ReplyToYardComment, id=pk)
        
        if reply:
            return render(request, "yard/show_yard.html", {'reply':reply})
        else:
            messages.success(request, ("This post does not exist"))
            return redirect('home')

        #if request.user.is_authenticated:
    
    def reply_delete(request, pk):
        if request.user.is_authenticated:  
            reply = get_object_or_404(ReplyToYardComment, id=pk)
            #check ownership
            if request.user.username == reply.user.username:
                #delete
                reply.delete()
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                messages.success(request, ("not your yard"))
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("Please log in."))
            return redirect('login')

    def reply_edit(request, pk, pc):
        if request.user.is_authenticated:
            reply = get_object_or_404(ReplyToYardComment, id=pc)
            if request.user.username == reply.user.username:  
                
                replyForm = ReplyToCommentForm(request.POST or None, instance=reply)
                comment = get_object_or_404(CommentYard, pk=pk)
                #edit comment
                if request.method == "POST":
                    if replyForm.is_valid():
                        replies = replyForm.save(commit=False)
                        replies.user = request.user
                        replies.yard = comment
                        replies.save()
                        messages.success(request, ("It is done!"))
                        return redirect('home')
                else:
                    return render(request, "yard/edit_reply.html", {'replyForm':replyForm, 'reply':reply})
            else:
                messages.success(request, ("not your comment"))
                return redirect('home')
        else:
            messages.success(request, ("Please log in."))
            return redirect('login')
# Follow class

class FollowView(APIView):

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
                return render(request, 'profile/followers.html', {"profiles":profiles})
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

class SearchView(APIView):   

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
        print(request.method)
        print(request.POST['search'])
        if request.method == "POST":
            #grab search phrase
            search = request.POST['search']
            #search the DB
            found_user = User.objects.filter(username__contains=search)
            found_yard = Yard.objects.filter(body__contains=search)
            found_comment = CommentYard.objects.filter(body__contains=search)
            found_reply = ReplyToYardComment.objects.filter(body__contains=search)
            return render(request, "search/search.html", {'search':search, 'found_user':found_user, 'found_yard':found_yard, 'found_comment':found_comment, 'found_reply':found_reply})
        else:
            messages.success(request, ("Sorry, nothing found"))
            return render(request, "search/search.html", {})

@after_response.enable
def notifications_read(request):
    notifications = Notifications.objects.filter(user=request.user)
    for object in notifications:
        object.read = True
        object.save()

class NotificationsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    model = Notifications
    template_name = 'notifications/notifications.html'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notifications.objects.filter(user=request.user).order_by('-date_modified')
        notifications_read.after_response(request)
        return Response({'notifications': notifications})
    
    
    

           




