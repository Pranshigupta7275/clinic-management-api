from datetime import timedelta

from django.contrib.auth import authenticate
from django.db.models import Count
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient, Appointment
from .serializers import PatientSerializer, AppointmentSerializer
from .permissions import IsStaffOrReadOnly
from .responses import custom_response


class HomeView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(custom_response(True, {}, "Welcome to the Clinic API"))


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if not user:
            return Response(
                custom_response(False, None, "Invalid credentials"),
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(custom_response(True, {"token": token.key}, "Login successful"))


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.query_params.get('search')

        if search:
            queryset = queryset.filter(name__icontains=search)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_response(True, serializer.data, "Patients fetched successfully"))


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        patient_id = self.request.query_params.get('patient_id')

        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
            
        return queryset


class StatsView(APIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        total_patients = Patient.objects.count()
        total_appointments = Appointment.objects.count()
        status_counts = Appointment.objects.values('status').annotate(count=Count('status'))

        stats = {
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'status_counts': list(status_counts),
        }
        return Response(custom_response(True, stats, "Stats fetched successfully"))


class UpcomingAppointmentsView(APIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        now = timezone.now()
        next_week = now + timedelta(days=7)

        appointments = Appointment.objects.filter(
            appointment_date__range=[now, next_week]
        ).order_by('appointment_date')

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(custom_response(True, serializer.data, "Upcoming appointments fetched successfully"))