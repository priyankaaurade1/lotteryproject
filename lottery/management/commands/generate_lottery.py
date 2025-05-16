from django.core.management.base import BaseCommand
from django.utils import timezone
from lottery.models import LotteryResult, COLUMN_COLORS
import random

class Command(BaseCommand):
    help = 'Generate 10x10 lottery numbers every 15 minutes'

    def handle(self, *args, **kwargs):
        now = timezone.localtime()
        minute_block = (now.minute // 15) * 15
        rounded_time = now.replace(minute=minute_block, second=0, microsecond=0)

        if LotteryResult.objects.filter(date=now.date(), time_slot=rounded_time.time()).exists():
            self.stdout.write("Result already generated.")
            return

        for i in range(100):
            row, col = divmod(i, 10)
            prefix = f"{i:02d}"
            suffix = f"{random.randint(0, 99):02d}"
            color = COLUMN_COLORS[col % len(COLUMN_COLORS)]
            LotteryResult.objects.create(
                date=now.date(),
                time_slot=rounded_time.time(),
                row=row,
                column=col,
                first_two_digits=prefix,
                last_two_digits=suffix,
                color=color
            )

        self.stdout.write(f"Generated results for {rounded_time.strftime('%I:%M %p')}")
