from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notifications, CommentYard
from django.dispatch import Signal

note = Signal()

@receiver(post_save, sender=CommentYard)
def sent_comment_notification(sender, instance, created, **kwargs):
    print("signal")
    if created:
        message = f'{instance.user} answered on your Yard"'    
        user = instance.yard.user
        link = reverse('yard_detail', args=[str(instance.yard.id)])
        notification = Notifications(user=user, message=message, link=link)
        notification.save()