from django.shortcuts import render,redirect
from .models import LotteryResult
from django.utils.timezone import now
import random
from datetime import datetime, timedelta, time
from django.http import JsonResponse

# Define colors for columns``
COLUMN_COLORS = ['#FFD700', '#DDA0DD', '#90EE90', '#FFB6C1', '#CD5C5C',
                 '#F5DEB3', '#ADD8E6', '#FFC0CB', '#87CEEB', '#FFA07A']

def get_time_slots():
    start = time(9, 0)
    end = time(21, 30)
    slots = []
    current = datetime.combine(datetime.today(), start)

    while current.time() <= end:
        slots.append(current.time().strftime('%H:%M'))
        current = current + timedelta(minutes=15)
    return slots

def past_results(request):
    selected_date = request.GET.get('date', now().date().isoformat())
    selected_slot = request.GET.get('time_slot', '09:00')

    records = LotteryResult.objects.filter(date=selected_date, time_slot=selected_slot).order_by('row', 'column')

    grid = [[None for _ in range(10)] for _ in range(10)]
    for result in records:
        full_number = f"{result.first_two_digits}{result.last_two_digits}"
        grid[result.row][result.column] = {
            'number': full_number,
            'color': result.color
        }
    context = {
        'numbers_grid': grid,
        'date': selected_date,
        'time_slot': selected_slot,
        'all_slots': get_time_slots(),
    }
    return render(request, 'past_results.html', context)

def get_next_time_slot():
    now = datetime.now()
    minute = ((now.minute // 15) + 1) * 15
    if minute == 60:
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        return next_hour.time()
    return time(now.hour, minute)

def auto_generate_lottery_results(request):
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

    return JsonResponse({"status": "success", "time_slot": str(time_slot)})

def edit_lottery_results(request):
    today = datetime.now().date()
    next_slot = get_next_time_slot()

    if request.method == "POST":
        results = LotteryResult.objects.filter(date=today, time_slot=next_slot)
        for result in results:
            key = f"last_two_{result.row}_{result.column}"
            if key in request.POST:
                result.last_two_digits = request.POST[key]
                result.save()
        return redirect('edit_lottery_results')

    grid = [[None]*10 for _ in range(10)]
    results = LotteryResult.objects.filter(date=today, time_slot=next_slot)
    for res in results:
        grid[res.row][res.column] = res
    print("Editing slot:", next_slot)
    print("Results count:", results.count())

    return render(request, 'edit_results.html', {
        'grid': grid,
        'date': today.strftime('%d-%m-%Y'),
        'time_slot': next_slot.strftime('%H:%M'),
    })