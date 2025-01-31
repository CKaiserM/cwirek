from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Yard, CommentYard, ReplyToYardComment, Notifications
#unregister groups
admin.site.unregister(Group)

# Combine profile info and user
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend user model

class UserAdmin(admin.ModelAdmin):
    model = User
    #display only username
    fields = ["username", "email"]
    inlines = [ProfileInline]

# Unregister initial User
admin.site.unregister(User)

# Register user and profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

# Register messages (Yard)
admin.site.register(Yard)

# Register yard comments
admin.site.register(CommentYard)

# Register Reply to yard comments
admin.site.register(ReplyToYardComment)
admin.site.register(Notifications)