from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notifications, CommentYard, ReplyToYardComment

@receiver(post_save, sender=CommentYard)
def sent_comment_notification(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user} answered on your Yard"'    
        user = instance.yard.user
        author = instance.user
        link = reverse('yard_show', args=[str(instance.yard.id)])
        notification = Notifications(user=user, author=author, message=message, link=link)
        notification.save()

@receiver(post_save, sender=ReplyToYardComment)
def sent_reply_notification(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user} replied to your comment"'    
        user = instance.comment.user
        author = instance.user
        link = reverse('reply', args=[str(instance.comment.id)])
        notification = Notifications(user=user, author=author, message=message, link=link)
        notification.save()