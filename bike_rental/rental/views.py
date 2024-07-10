from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer, CustomTokenObtainPairSerializerWithUserData
from .models import User, Bike, Rental
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from .tasks import calculate_rental_cost


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializerWithUserData

class AvailableBikesListView(APIView):
    def get(self, request):
        bikes = Bike.objects.filter(is_available=True)
        bikes_data = [{"id": bike.id, "name": bike.name} for bike in bikes]
        return Response(bikes_data)
    

class RentBikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if Rental.objects.filter(user=user, end_time__isnull=True).exists():
            return Response({"detail": "You already have a bike rented."}, status=status.HTTP_400_BAD_REQUEST)

        bike_id = request.data.get('bike_id')
        try:
            bike = Bike.objects.get(id=bike_id, is_available=True)
        except Bike.DoesNotExist:
            return Response({"detail": "Bike is not available."}, status=status.HTTP_400_BAD_REQUEST)

        rental = Rental.objects.create(user=user, bike=bike)
        bike.is_available = False
        bike.save()

        rental_data = {"id": rental.id, "bike": rental.bike.name, "start_time": rental.start_time}
        return Response(rental_data, status=status.HTTP_201_CREATED)

    
class ReturnBikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            rental = Rental.objects.get(user=user, end_time__isnull=True)
        except Rental.DoesNotExist:
            return Response({"detail": "No active rental found."}, status=status.HTTP_400_BAD_REQUEST)

        rental.end_time = timezone.now()
        rental.save()

        calculate_rental_cost.delay(rental.id)
        bike = rental.bike
        bike.is_available = True
        bike.save()

        rental_data = {
            "id": rental.id,
            "bike": rental.bike.name,
            "start_time": rental.start_time,
            "end_time": rental.end_time
        }
        return Response(rental_data, status=status.HTTP_200_OK)


class UserRentalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        rentals = Rental.objects.filter(user=user)
        rentals_data = [
            {"id": rental.id, "bike": rental.bike.name, "start_time": rental.start_time, "end_time": rental.end_time}
            for rental in rentals
        ]
        return Response(rentals_data)

