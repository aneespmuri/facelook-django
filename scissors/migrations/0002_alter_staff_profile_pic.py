# Generated by Django 5.2.1 on 2025-06-17 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scissors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='staff_profiles/'),
        ),
    ]
