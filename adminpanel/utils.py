import random
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import LotteryResult, COLUMN_COLORS

def generate_results_for_slot():
    current_time = now()
    slot_time = (current_time + timedelta(minutes=15)).replace(second=0, microsecond=0)
    today = slot_time.date()

    hour, minute = slot_time.hour, slot_time.minute
    if hour < 9 or (hour == 21 and minute > 30) or hour > 21:
        return

    for row in range(10):
        for col in range(10):
            first_two = f"{row * 10 + col:02}"
            last_two = f"{random.randint(0, 99):02}"
            LotteryResult.objects.update_or_create(
                date=today,
                time_slot=slot_time.time(),
                row=row,
                column=col,
                defaults={
                    'first_two_digits': first_two,
                    'last_two_digits': last_two,
                    'color': COLUMN_COLORS[col],
                }
            )
