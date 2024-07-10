from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, AvailableBikesListView , RentBikeView, ReturnBikeView, UserRentalHistoryView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Bike Rental API",
      default_version='v1',
      description="API for renting bikes",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@bike-rental.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[],
)

urlpatterns = [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bikes/available/', AvailableBikesListView.as_view(), name='available_bikes'),
    path('rent/', RentBikeView.as_view(), name='rent_bike'),
    path('return/', ReturnBikeView.as_view(), name='return_bike'),
    path('history/', UserRentalHistoryView.as_view(), name='rental_history'),

]

urlpatterns += router.urls
