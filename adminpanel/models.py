from django.db import models

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

    def full_number(self):
        return f"{self.first_two_digits}{self.last_two_digits}"

    class Meta:
        unique_together = ('date', 'time_slot', 'row', 'column')
