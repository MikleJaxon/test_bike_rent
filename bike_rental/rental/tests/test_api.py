import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rental.models import User, Bike, Rental
from django.utils import timezone

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def bike(db):
    return Bike.objects.create(name='Test Bike')


@pytest.mark.django_db
def test_rent_bike(auth_client, user, bike):
    url = reverse('rent_bike')
    response = auth_client.post(url, {'bike_id': bike.id})
    assert response.status_code == 201
    rental = Rental.objects.get(user=user, bike=bike)
    assert rental.start_time is not None
    assert rental.end_time is None
    bike.refresh_from_db()
    assert not bike.is_available

@pytest.mark.django_db
def test_return_bike(auth_client, user, bike):
    rental = Rental.objects.create(user=user, bike=bike)
    url = reverse('return_bike')
    response = auth_client.post(url)
    assert response.status_code == 200
    rental.refresh_from_db()
    assert rental.end_time is not None
    bike.refresh_from_db()
    assert bike.is_available

@pytest.mark.django_db
def test_rental_history(auth_client, user, bike):
    rental = Rental.objects.create(user=user, bike=bike)
    rental.end_time = timezone.now()
    rental.save()
    url = reverse('rental_history')
    response = auth_client.get(url)
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 1
    assert history[0]['id'] == rental.id
    assert history[0]['bike'] == bike.name
    assert history[0]['end_time'] is not None
