from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import time
from adminpanel.models import LotteryResult, COLUMN_COLORS

class Command(BaseCommand):
    help = 'Auto-generate a 10x10 lottery table every 15 minutes'

    def handle(self, *args, **kwargs):
        current_time = now()
        current_slot = current_time.replace(second=0, microsecond=0, minute=(current_time.minute // 15) * 15).time()
        today = current_time.date()

        # Check if the slot is within 9:00 AM - 9:30 PM
        if not time(9, 0) <= current_slot <= time(21, 30):
            self.stdout.write("⏳ Outside the scheduled slot. Skipping.")
            return

        # Prevent duplicate table generation
        if LotteryResult.objects.filter(date=today, time_slot=current_slot).exists():
            self.stdout.write(f"Table for {today} {current_slot} already exists.")
            return

        for row in range(10):
            for col in range(10):
                LotteryResult.objects.create(
                    date=today,
                    time_slot=current_slot,
                    row=row,
                    column=col,
                    first_two_digits=f"{row * 10 + col:02}",
                    last_two_digits="",  # Leave last 2 digits blank for editing later
                    color=COLUMN_COLORS[col]
                )

        self.stdout.write(self.style.SUCCESS(f"Table generated for {today} {current_slot}"))
