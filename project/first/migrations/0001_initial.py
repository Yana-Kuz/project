# Generated by Django 3.2.8 on 2022-03-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumer_key', models.CharField(max_length=20)),
                ('consumer_secret', models.CharField(max_length=20)),
                ('launch_url', models.CharField(max_length=50)),
                ('lti_message_type', models.CharField(max_length=30)),
                ('lti_version', models.CharField(max_length=10)),
                ('resource_link_id', models.CharField(max_length=20)),
            ],
        ),
    ]
