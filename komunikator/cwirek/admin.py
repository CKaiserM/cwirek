from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Yard
#unregister groups
admin.site.unregister(Group)

# Combine profile info and user
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend user model

class UserAdmin(admin.ModelAdmin):
    model = User
    #display only username
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister initial User
admin.site.unregister(User)

# Register user and profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

# Register messages (Yard)
admin.site.register(Yard)
