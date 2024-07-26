# Generated by Django 5.0.6 on 2024-07-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('manufacturer', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Fighting', 'Fighting'), ('story', 'story'), ('RPG', 'RPG'), ('Battle royal', 'Battle royal'), ('first person', 'first person')], max_length=200)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='image')),
            ],
        ),
    ]