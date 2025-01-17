from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create yard (podwórko) model

class Yard(models.Model):
    user = models.ForeignKey(User, related_name="yard", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="yard_like", blank=True)
    dislikes = models.ManyToManyField(User, related_name="yard_dislike", blank=True)

    # Keep track of likes and dislikes

    def number_of_likes(self):
        return self.likes.count()
    def number_of_dislikes(self):
        return self.dislikes.count()

    # Create string with user, date and body
    def __str__(self):
        return (f"{self.user} " f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body}...")
    
# Comment post model

class CommentYard(models.Model):
    yard = models.ForeignKey(Yard, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING, null=True)
    body = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    #comment = models.ManyToManyField(User, related_name="yard_comment", blank=True)
    
    def number_of_comments(self):
        return self.comments.count()

    def __str__(self):
        return (f"{self.user} " f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body[:30]}...")

# Create a User Profile Model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    date_modified = models.DateTimeField(User, auto_now=True)

    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=1500)
    homepage_link = models.CharField(null=True, blank=True, max_length=100)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)
    linkedin_link = models.CharField(null=True, blank=True, max_length=100)
    youtube_link = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username

# Create profile when new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #follow myself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)
