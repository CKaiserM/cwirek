# Generated by Django 5.1.4 on 2025-02-01 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yard', '0010_remove_notifications_test_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentyard',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='notifications',
            options={'ordering': ['-date_modified']},
        ),
        migrations.AlterModelOptions(
            name='replytoyardcomment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='yard',
            options={'ordering': ['-created_at']},
        ),
    ]
