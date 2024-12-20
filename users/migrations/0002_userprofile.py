# Generated by Django 5.1.1 on 2024-09-16 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('account_number', models.CharField(max_length=20)),
                ('account_name', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('referral_code', models.CharField(blank=True, max_length=7, null=True)),
                ('referral_points', models.IntegerField(default=0)),
            ],
        ),
    ]
