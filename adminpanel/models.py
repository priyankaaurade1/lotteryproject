from django.db import models
from django.utils import timezone
from datetime import timedelta

COLUMN_COLORS = [
    '#FFD700', '#DDA0DD', '#90EE90', '#FFB6C1', '#CD5C5C',
    '#F5DEB3', '#ADD8E6', '#FFC0CB', '#87CEEB', '#FFA07A'
]

class LotteryResult(models.Model):
    date = models.DateField()
    time_slot = models.TimeField()
    row = models.IntegerField()
    column = models.IntegerField()
    first_two_digits = models.CharField(max_length=2)
    last_two_digits = models.CharField(max_length=2)
    color = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)

    def full_number(self):
        return f"{self.first_two_digits}{self.last_two_digits}"

    def is_editable(self):
        # Editable for 14 minutes after creation
        return timezone.now() < self.created_at + timedelta(minutes=14)

    class Meta:
        unique_together = ('date', 'time_slot', 'row', 'column')
    

