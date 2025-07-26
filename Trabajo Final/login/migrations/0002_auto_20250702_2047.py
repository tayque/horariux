from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_users_and_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User') 
    UserProfile = apps.get_model('login', 'UserProfile')

    if not User.objects.filter(username='director').exists():
        director_user = User.objects.create(
            username='director',
            email='director@unsa.edu.pe', 
            password=make_password('pruebita'), 
            is_staff=True, 
            is_superuser=True, 
            is_active=True,
        )
        UserProfile.objects.create(
            user=director_user,
            is_director=True,
            is_secretary=False,
        )

    if not User.objects.filter(username='secretaria').exists():
        secretary_user = User.objects.create(
            username='secretary',
            email='secretary@unsa.edu.pe',
            password=make_password('pruebita2'), 
            is_staff=True, 
            is_superuser=True,
            is_active=True,
        )
        UserProfile.objects.create(
            user=secretary_user,
            is_director=False,
            is_secretary=True,
        )

def delete_initial_users_and_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('login', 'UserProfile')

    UserProfile.objects.filter(user__username='director').delete()
    UserProfile.objects.filter(user__username='secretary').delete()

    User.objects.filter(username='director').delete()
    User.objects.filter(username='secretary').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_initial_users_and_profiles, reverse_code=delete_initial_users_and_profiles),
    ]