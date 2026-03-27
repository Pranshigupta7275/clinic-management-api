from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta

from .models import Patient, Appointment


class StatsAndUpcomingAppointmentsTests(APITestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            name='Alice',
            age=30,
            gender='Female',
            contact_number='1234567890',
            blood_group='O+'
        )

        # one pending appointment in range, one confirmed out of range
        Appointment.objects.create(
            patient=self.patient,
            doctor_name='Dr. Smith',
            appointment_date=timezone.now() + timedelta(days=2),
            reason='Checkup',
            status='Pending'
        )

        Appointment.objects.create(
            patient=self.patient,
            doctor_name='Dr. Brown',
            appointment_date=timezone.now() + timedelta(days=10),
            reason='Follow-up',
            status='Confirmed'
        )

    def test_stats_endpoint(self):
        url = reverse('stats')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_patients'], 1)
        self.assertEqual(response.data['total_appointments'], 2)

        # should include both counts
        status_counts = {item['status']: item['count'] for item in response.data['status_counts']}
        self.assertEqual(status_counts.get('Pending'), 1)
        self.assertEqual(status_counts.get('Confirmed'), 1)

    def test_upcoming_appointments_endpoint(self):
        url = reverse('upcoming-appointments')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['doctor_name'], 'Dr. Smith')

