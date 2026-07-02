from django.db import models


class SecurityEvent(models.Model):
    event_type = models.CharField(max_length=120)
    severity = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.severity} - {self.event_type}"



