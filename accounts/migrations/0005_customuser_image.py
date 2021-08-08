# Generated by Django 3.2.5 on 2021-08-08 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='images'),
        ),
    ]
