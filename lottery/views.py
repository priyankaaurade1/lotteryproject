from django.shortcuts import render
from adminpanel.models import LotteryResult,COLUMN_COLORS
from datetime import datetime, timedelta
import random

def show_lottery_table(request):
    today = datetime.now().date()
    formatted_date = today.strftime("%d-%m-%Y")
    time_slots = [
        "09:00:00", "09:15:00", "09:30:00", "09:45:00", "10:00:00", "10:15:00", "10:30:00", "10:45:00",
        "11:00:00", "11:15:00", "11:30:00", "11:45:00", "12:00:00", "12:15:00", "12:30:00", "12:45:00",
        "13:00:00", "13:15:00", "13:30:00", "13:45:00", "14:00:00", "14:15:00", "14:30:00", "14:45:00",
        "15:00:00", "15:15:00", "15:30:00", "15:45:00", "16:00:00", "16:15:00", "16:30:00", "16:45:00",
        "17:00:00", "17:15:00", "17:30:00", "17:45:00", "18:00:00", "18:15:00", "18:30:00", "18:45:00",
        "19:00:00", "19:15:00", "19:30:00", "19:45:00", "20:00:00", "20:15:00", "20:30:00", "20:45:00",
        "21:00:00", "21:15:00", "21:30:00"
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

# def generate_lottery_grid():
#     today = datetime.now().date()
#     current_slot = get_last_time_slot()

#     grid = [[None]*10 for _ in range(10)]
#     results = LotteryResult.objects.filter(date=today, time_slot=current_slot)

#     for res in results:
#         grid[res.row][res.column] = res.last_two_digits 

#     return grid

import random

def generate_lottery_grid():
    grid = []
    for i in range(100): 
        prefix = f"{i:02d}"  
        suffix = f"{random.randint(0, 99):02d}"  
        full_number = prefix + suffix  
        grid.append(full_number)
    return [grid[i:i+10] for i in range(0, 100, 10)]

def get_last_time_slot():
    now = datetime.now()
    minute = (now.minute // 15) * 15
    last_slot = now.replace(minute=minute, second=0, microsecond=0)
    # print("Fetching results for slot:", current_slot)
    # print("Results count:", results.count())
    return last_slot.time()  

def generate_lottery_results(request):
    today = datetime.now().date()

    time_slots = [
        "09:00:00", "09:15:00", "09:30:00", "09:45:00", "10:00:00", "10:15:00", "10:30:00", "10:45:00",
        "11:00:00", "11:15:00", "11:30:00", "11:45:00", "12:00:00", "12:15:00", "12:30:00", "12:45:00",
        "13:00:00", "13:15:00", "13:30:00", "13:45:00", "14:00:00", "14:15:00", "14:30:00", "14:45:00",
        "15:00:00", "15:15:00", "15:30:00", "15:45:00", "16:00:00", "16:15:00", "16:30:00", "16:45:00",
        "17:00:00", "17:15:00", "17:30:00", "17:45:00", "18:00:00", "18:15:00", "18:30:00", "18:45:00",
        "19:00:00", "19:15:00", "19:30:00", "19:45:00", "20:00:00", "20:15:00", "20:30:00", "20:45:00",
        "21:00:00", "21:15:00", "21:30:00"
    ]

    results = []
    for slot in time_slots:
        time_obj = datetime.strptime(slot, "%H:%M:%S").time()

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

