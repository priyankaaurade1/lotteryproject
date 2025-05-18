from django.shortcuts import render
from adminpanel.models import LotteryResult,COLUMN_COLORS
from datetime import datetime, timedelta
import random
from .utils import generate_lottery_grid

def show_lottery_table(request):
    today = datetime.now().date()
    formatted_date = today.strftime("%d-%m-%Y")
    time_slots = [
        "09:00 AM", "09:15 AM", "09:30 AM", "09:45 AM", "10:00 AM", "10:15 AM", "10:30 AM", "10:45 AM",
        "11:00 AM", "11:15 AM", "11:30 AM", "11:45 AM", "12:00 PM", "12:15 PM", "12:30 PM", "12:45 PM",
        "01:00 PM", "01:15 PM", "01:30 PM", "01:45 PM", "02:00 PM", "02:15 PM", "02:30 PM", "02:45 PM",
        "03:00 PM", "03:15 PM", "03:30 PM", "03:45 PM", "04:00 PM", "04:15 PM", "04:30 PM", "04:45 PM",
        "05:00 PM", "05:15 PM", "05:30 PM", "05:45 PM", "06:00 PM", "06:15 PM", "06:30 PM", "06:45 PM",
        "07:00 PM", "07:15 PM", "07:30 PM", "07:45 PM", "08:00 PM", "08:15 PM", "08:30 PM", "08:45 PM",
        "09:00 PM", "09:15 PM", "09:30 PM"
    ]
    grid = generate_lottery_grid()
    slot_label = get_last_time_slot()
    return render(request, 'index.html', {
        'grid': grid,
        'selected_date': today.strftime("%Y-%m-%d"),
        'time_slots': time_slots,
        'current_slot_label': slot_label,
        'formatted_date':formatted_date
    })

def get_last_time_slot():
    now = datetime.now()
    minute = (now.minute // 15) * 15
    last_slot = now.replace(minute=minute, second=0, microsecond=0)
    return last_slot.strftime("%I:%M %p").lstrip("0")  

def generate_lottery_results(request):
    today = datetime.now().date()

    time_slots = [
        "09:00 AM", "09:15 AM", "09:30 AM", "09:45 AM", "10:00 AM", "10:15 AM", "10:30 AM", "10:45 AM",
        "11:00 AM", "11:15 AM", "11:30 AM", "11:45 AM", "12:00 PM", "12:15 PM", "12:30 PM", "12:45 PM",
        "01:00 PM", "01:15 PM", "01:30 PM", "01:45 PM", "02:00 PM", "02:15 PM", "02:30 PM", "02:45 PM",
        "03:00 PM", "03:15 PM", "03:30 PM", "03:45 PM", "04:00 PM", "04:15 PM", "04:30 PM", "04:45 PM",
        "05:00 PM", "05:15 PM", "05:30 PM", "05:45 PM", "06:00 PM", "06:15 PM", "06:30 PM", "06:45 PM",
        "07:00 PM", "07:15 PM", "07:30 PM", "07:45 PM", "08:00 PM", "08:15 PM", "08:30 PM", "08:45 PM",
        "09:00 PM", "09:15 PM", "09:30 PM"
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

