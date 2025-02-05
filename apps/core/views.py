from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order
from apps.expenses.models import AdExpense


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get period from request, default to 'day'
        period = self.request.GET.get('period', 'day')

        # Calculate date range
        today = timezone.now().date()
        if period == 'day':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        else:  # year
            start_date = today - timedelta(days=365)

        # Get orders data
        orders = Order.objects.filter(
            order_date__date__gte=start_date,
            order_date__date__lte=today
        )

        # Calculate metrics
        total_sales = orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Get expenses
        expenses = AdExpense.objects.filter(
            date__gte=start_date,
            date__lte=today
        )
        total_expenses = expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculate profit
        profit = total_sales - total_expenses

        # Calculate ROI
        roi = (profit / total_expenses * 100) if total_expenses > 0 else 0

        # Calculate margin
        margin = (profit / total_sales * 100) if total_sales > 0 else 0

        context.update({
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'profit': profit,
            'roi': roi,
            'margin': margin,
            'period': period,
        })

        return context