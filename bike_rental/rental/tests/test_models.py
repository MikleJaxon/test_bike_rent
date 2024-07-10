import pytest
from django.utils import timezone
from rental.models import User, Bike, Rental

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.check_password('password123')

@pytest.mark.django_db
def test_create_bike():
    bike = Bike.objects.create(name='Test Bike')
    assert bike.name == 'Test Bike'
    assert bike.is_available

@pytest.mark.django_db
def test_create_rental():
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
    bike = Bike.objects.create(name='Test Bike')
    rental = Rental.objects.create(user=user, bike=bike)
    assert rental.user == user
    assert rental.bike == bike
    assert rental.start_time <= timezone.now()
    assert rental.end_time is None
