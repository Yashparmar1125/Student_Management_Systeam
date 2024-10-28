# your_app/utils.py
from django.utils import timezone
from .models import Holidays

def delete_expired_holidays():
    today = timezone.now().date()
    expired_holidays = Holidays.objects.filter(end_date__lt=today)
    count, _ = expired_holidays.delete()
    return count
