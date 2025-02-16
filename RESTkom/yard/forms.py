from django import forms
from .models import Yard, Profile, CommentYard, ReplyToYardComment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# Profile bio, image and social links form

class ProfileMiscForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}), required=False)
    homepage_link = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Personal homepage'}), required=False)
    facebook_link = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook link'}), required=False)
    instagram_link = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram link'}), required=False)
    linkedin_link = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin link'}), required=False)
    youtube_link = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin link'}), required=False)

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link','youtube_link',)

# Form for posting Yards

class YardForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Enter your message.", "class":"form-control", "id":"postYard",}), label="", max_length=250, )
    yard_image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}), required=False)
    class Meta:
        model = Yard
        field = ['body', 'yard_image']
        exclude = ("user", "likes", "dislikes",)

# Form for commenting on Yard

class CommentYardForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Add your comment...", "class":"form-control",}), label="", max_length=250, )
    class Meta:
        model = CommentYard
        field = ['body']
        exclude = ("user", "likes", "dislikes", "yard")

# Form for Reply to Comment

class ReplyToCommentForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Reply to comment", "class":"form-control",}), label="", max_length=250, )
    class Meta:
        model = ReplyToYardComment
        field = ['body']
        exclude = ("user", "likes", "dislikes", "yard", "comment")

# Sign-Up form

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

# Update user form

class UpdateUserForm(UserChangeForm):

    password = None
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
