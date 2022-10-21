# Generated by Django 4.1.1 on 2022-10-21 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(blank=True, max_length=100, null=True)),
                ('nid', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('N', 'NA')], max_length=1, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_valid', models.BooleanField(default=False)),
                ('nid_valid', models.BooleanField(default=False)),
                ('email_valid', models.BooleanField(default=False)),
            ],
        ),
    ]
