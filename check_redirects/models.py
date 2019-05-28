from django.db import models

# Create your models here.

class Urllist(models.Model):
    site_url = models.URLField()
    team = models.CharField(max_length=60)
    # slack_url = models.URLField()
    target_url = models.URLField(default="")
    enable = models.BooleanField(default=True)
    broken_redirect = models.BooleanField(default=False)
    actual_target = models.URLField(default=None, blank=True, null=True)
    slack_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.site_url

class Responsetime(models.Model):
    response_time = models.FloatField(default=0.00)
