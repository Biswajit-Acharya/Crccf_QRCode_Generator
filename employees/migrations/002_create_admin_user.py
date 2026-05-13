import os
from django.db import migrations


def create_admin_user(apps, schema_editor):
    User = apps.get_model("auth", "User")

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@gmail.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin12345")

    user, created = User.objects.get_or_create(username=username)

    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("employees", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]