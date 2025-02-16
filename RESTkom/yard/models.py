from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.urls import reverse

# Create yard (podwórko) model

class Yard(models.Model):
    user = models.ForeignKey(User, related_name="yard", on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="yard_like", blank=True)
    dislikes = models.ManyToManyField(User, related_name="yard_dislike", blank=True)

    yard_image = models.ImageField(null=True, blank=True, upload_to="images/yard/")

#    slug = models.SlugField(unique=True, max_length=50)

    # Keep track of likes and dislikes

    def number_of_likes(self):
        return self.likes.count()
    def number_of_dislikes(self):
        return self.dislikes.count()

    # Create string with user, date and body
    def __str__(self):
        return (f"{self.user} " f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body}...")

    class Meta:
        ordering = ['-created_at']
    
# Comment post model

class CommentYard(models.Model):
    yard = models.ForeignKey(Yard, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment_author", on_delete=models.DO_NOTHING)
    body = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comment_like", blank=True)
    dislikes = models.ManyToManyField(User, related_name="comment_dislike", blank=True)

    # Keep track of likes and dislikes

    def number_of_likes(self):
        return self.likes.count()
    def number_of_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return (f"{self.user} " f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body[:30]}...")
    
    class Meta:
        ordering = ['-created_at']

# Reply to comment model   

class ReplyToYardComment(models.Model):
    comment = models.ForeignKey(CommentYard, related_name="replies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reply_author", on_delete=models.DO_NOTHING, null=True)
    body = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="reply_like", blank=True)
    dislikes = models.ManyToManyField(User, related_name="reply_dislike", blank=True)
    # Keep track of likes and dislikes

    def number_of_likes(self):
        return self.likes.count()
    def number_of_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return (f"{self.user} " f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body[:30]}...")
    
    class Meta:
        ordering = ['-created_at']


# Create a User Profile Model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    date_modified = models.DateTimeField(User, auto_now=True)

    profile_image = models.ImageField(blank=True, upload_to="images/profile/", default="default_profile_pic.png")
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

# Create a notifications model. 

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_user")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_author")
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    date_modified = models.DateTimeField(User, auto_now_add=True)

    class Meta:
        ordering = ['-date_modified']

# Signal Receivers (post_save) for Yard, Comment and Reply. If created, the receivers will save new Notification object with User and Author. 

@receiver(post_save, sender=Yard)
def sent_yard_notification(sender, instance, created, **kwargs):
    followers = instance.user.profile.followed_by.all()
    if followers != 0:
        if created:
            message = f'{instance.user} posted new Yard'    
            author = instance.user
            for follower in followers:
                if follower.user != author:
                    link = reverse('yard_show', args=[str(instance.id)])
                    notification = Notifications(user=follower.user, author=author, message=message, link=link)
                    notification.save()
 

@receiver(post_save, sender=CommentYard)
def sent_comment_notification(sender, instance, created, **kwargs):
    user = instance.yard.user
    author = instance.user
    if created and user != author:
        message = f'{instance.user} answered on your Yard'    
        link = reverse('yard_show', args=[str(instance.yard.id)])
        notification = Notifications(user=user, author=author, message=message, link=link)
        notification.save()

@receiver(post_save, sender=ReplyToYardComment)
def sent_reply_notification(sender, instance, created, **kwargs):
    user = instance.comment.user
    author = instance.user
    if created and user != author:
        message = f'{instance.user} replied to your comment'    
        link = reverse('reply', args=[str(instance.comment.id)])
        notification = Notifications(user=user, author=author, message=message, link=link)
        notification.save()

# end of Notification Receivers   