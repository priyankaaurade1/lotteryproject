from django.shortcuts import render
from datetime import datetime, timedelta, time
from .models import LotteryResult
from django.utils.timezone import now

# Define colors for columns
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

    # Create grid for table
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
