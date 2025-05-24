from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, time
import random
from adminpanel.models import LotteryResult
from adminpanel.views import COLUMN_COLORS  

def get_next_time_slot():
    now = datetime.now()
    minute = ((now.minute // 15) + 1) * 15
    if minute == 60:
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        return next_hour.time()
    return time(now.hour, minute)

class Command(BaseCommand):
    help = 'Automatically generate lottery results for the next time slot.'

    def handle(self, *args, **kwargs):
        today = datetime.now().date()
        time_slot = get_next_time_slot()

        for i in range(100):
            row = i // 10
            column = i % 10
            first_two = f"{i:02}"

            LotteryResult.objects.get_or_create(
                date=today,
                time_slot=time_slot,
                row=row,
                column=column,
                first_two_digits=first_two,
                defaults={
                    'last_two_digits': f"{random.randint(0, 99):02}",
                    'color': COLUMN_COLORS[column]
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated results for {time_slot}'))
