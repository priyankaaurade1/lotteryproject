from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from datetime import timedelta
from .models import LotteryResult, COLUMN_COLORS
import random

@csrf_exempt
def run_cron_job(request):
    secret_token = request.GET.get('token')
    if secret_token != 'my_secret_token_123':
        return JsonResponse({'status': 'unauthorized'}, status=403)

    now = localtime()
    minute_block = (now.minute // 15) * 15
    rounded_time = now.replace(minute=minute_block, second=0, microsecond=0)

    if LotteryResult.objects.filter(date=now.date(), time_slot=rounded_time.time()).exists():
        return JsonResponse({'status': 'already_exists'})

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

    return JsonResponse({'status': 'generated'})
