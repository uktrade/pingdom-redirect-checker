from django.db import models

# Create your models here.

PROTOCOL_CHOICE = (
    ('both','BOTH'),
    ('https','HTTPS'),
    ('http','HTTP'),
)

class Urllist(models.Model):
    site_url = models.URLField()
    target_url = models.URLField(default='')
    enable = models.BooleanField(default=True)
    broken_redirect = models.BooleanField(default=False)
    actual_target = models.URLField(default=None, blank=True, null=True)

    def __str__(self):
        return self.site_url

class Responsetime(models.Model):
    response_time = models.FloatField(default=0.00)
