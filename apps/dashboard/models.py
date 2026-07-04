from django.db import models

class SecurityEvent(models.Model):
    # Standard choice boundaries to ensure unified lookups
    SEVERITY_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk / Tactical Threat'),
    ]

    event_type = models.CharField(max_length=120)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='LOW')
    description = models.TextField(blank=True)
    rssi = models.IntegerField(null=True, blank=True, help_text="Signal strength indicator in dBm")
    source = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Crucial field for the active operational pipeline triage queue
    is_triaged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.event_type} - {self.source if self.source else 'Unknown Source'}"



