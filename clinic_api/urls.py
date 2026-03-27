from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from patients.views import (
    HomeView, 
    LoginView, 
    PatientViewSet, 
    AppointmentViewSet, 
    StatsView, 
    UpcomingAppointmentsView
)

# Admin Dashboard Customization
admin.site.site_header = "Clinic API Administration"
admin.site.site_title = "Clinic API Portal"
admin.site.index_title = "Welcome to the Clinic Management Dashboard"

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    
    path('api/', include(router.urls)),
    path('api/stats/', StatsView.as_view(), name='api-stats'),
    
    # FIXED: Matches Task 3.2 requirement exactly
    path('api/appointments/upcoming/', UpcomingAppointmentsView.as_view(), name='upcoming-appointments'),

    path('api/auth/login/', LoginView.as_view(), name='api-login'),
    path('api/auth/token/', obtain_auth_token, name='api-token-auth'),
]