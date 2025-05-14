from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.timezone import now
from .models import LotteryResult, COLUMN_COLORS

@admin.register(LotteryResult)
class LotteryResultAdmin(admin.ModelAdmin):
    change_list_template = 'past_results.html'
    list_display = ['date', 'time_slot', 'full_number']

    def add_view(self, request, form_url='', extra_context=None):
        today = now().date()
        current_time = now().time()
        numbers = []

        for row in range(10):
            row_data = []
            for col in range(10):
                first = f"{row * 10 + col:02}"
                last = ""
                row_data.append({
                    'row': row,
                    'col': col,
                    'first': first,
                    'color': COLUMN_COLORS[col],
                    'input_name': f"cell_{row}_{col}",
                })
            numbers.append(row_data)

        if request.method == 'POST':
            for row in range(10):
                for col in range(10):
                    last_two = request.POST.get(f'cell_{row}_{col}', '').zfill(2)
                    LotteryResult.objects.create(
                        date=today,
                        time_slot=current_time,
                        row=row,
                        column=col,
                        first_two_digits=f"{row * 10 + col:02}",
                        last_two_digits=last_two,
                        color=COLUMN_COLORS[col]
                    )
            self.message_user(request, "Results saved successfully.")
            return TemplateResponse(request, "lotteryresult_success.html", {})

        context = {
            **self.admin_site.each_context(request),
            'numbers_grid': numbers,
        }
        return TemplateResponse(request, "edit_table.html", context)
