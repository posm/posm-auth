# Generated by Django 2.2.6 on 2019-10-31 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_initial_superuser(apps, schema_editor):
    from django.contrib.auth.models import User
    User.objects.create_user(
        username='admin',
        password='admin123',
        is_superuser=True,
        is_staff=True,
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PosmComponentPermission',
            fields=[
                ('code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('permissions', models.ManyToManyField(to='group.PosmComponentPermission')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.ManyToManyField(to='group.PosmComponentPermission')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

        migrations.RunPython(create_initial_superuser, reverse_code=migrations.RunPython.noop),
    ]
