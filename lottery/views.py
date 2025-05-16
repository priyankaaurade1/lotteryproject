from django.shortcuts import render
from adminpanel.models import LotteryResult,COLUMN_COLORS
from datetime import datetime, timedelta
import random
from .utils import generate_lottery_grid

def show_lottery_table(request):
    grid = generate_lottery_grid()
    return render(request, 'index.html', {'grid': grid})

def generate_lottery_results(request):
    today = datetime.now().date()

    time_slots = [
        "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45",
        "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45",
        "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45",
        "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45",
        "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30", "18:45",
        "19:00", "19:15", "19:30", "19:45", "20:00", "20:15", "20:30", "20:45",
        "21:00", "21:15", "21:30"
    ]

    results = []
    for slot in time_slots:

        hour, minute = map(int, slot.split(':'))
        time_obj = datetime.strptime(slot, "%H:%M").time()

        for i in range(100):
            row = i // 10
            column = i % 10
            first_two = f"{i:02}"

            lottery_result, created = LotteryResult.objects.get_or_create(
                date=today,
                time_slot=time_obj,
                row=row,
                column=column,
                first_two_digits=first_two,
                defaults={
                    'last_two_digits': f"{random.randint(0, 99):02}",
                    'color': COLUMN_COLORS[column]
                }
            )
            results.append(lottery_result)

    return render(request, 'index.html', {'results': results})

from django.http import JsonResponse
from django.core.management import call_command

def trigger_lottery(request, token):
    if token != 'your-secret-token':
        return JsonResponse({'error': 'unauthorized'}, status=403)

    call_command('generate_lottery')
    return JsonResponse({'message': 'Lottery generated'})

