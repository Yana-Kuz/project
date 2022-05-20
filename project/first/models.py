from django.db import models

class Tools(models.Model):
    consumer_key = models.CharField(max_length=20)
    consumer_secret = models.CharField(max_length=20)
    launch_url = models.URLField()
    lti_message_type = models.CharField(max_length=30)
    lti_version = models.CharField(max_length=10)
    resource_link_id = models.CharField(max_length=20)
