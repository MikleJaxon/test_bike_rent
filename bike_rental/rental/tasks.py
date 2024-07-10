from celery import shared_task
from django.utils import timezone
from .models import Rental

@shared_task
def calculate_rental_cost(rental_id):
    try:
        rental = Rental.objects.get(id=rental_id)
        if rental.end_time:
            duration = rental.end_time - rental.start_time
            hours = duration.total_seconds() // 3600
            cost = hours * 1000
            rental.cost = cost
            rental.save()
    except Rental.DoesNotExist:
        pass
