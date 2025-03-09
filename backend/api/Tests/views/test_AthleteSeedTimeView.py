import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Athlete, TimeRecord, MeetEvent, EventType, SwimMeet
from datetime import timedelta, date
from api.serializers.AthleteSeedTimeSerializer import AthleteSeedTimeSerializer, UpdateAthleteSeedTimeSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class AthleteSeedTimeViewTests(APITestCase):
    fixtures = ['setup_data.json', 'athlete_data.json', 'meetevent_data.json', 'swim_meet.json', 'time_record.json']

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_authenticate(user=self.user)
        self.meet_event = MeetEvent.objects.get(id=1)
        self.url = reverse("seed-times", args=[self.meet_event.id])


    def test_get_athlete_seed_times_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),9)
        print(response.data)

        serializer = AthleteSeedTimeSerializer(data=response.data, many=True)
        self.assertTrue(serializer.is_valid())

        ordered_by_first_name = ['Ana Gomez', 'Anna Anderson', 'Ava Wilson', 'Elena Lopez', 'Ellie Yuan', 'Kyla Smith', 'Laura Sanchez', 'Olivia Davis', 'Sofia Avila']
        self.assertEqual(ordered_by_first_name, [athlete['athlete_full_name'] for athlete in serializer.validated_data] )

    def test_get_event_not_found(self):
        url = reverse("seed-times", args=[999])
        bad_response = self.client.get(url)
        self.assertEqual(bad_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(bad_response.content, b'{"error":"Event not found"}')

        print(self.meet_event.event_type.stroke)

    def test_get_event_type_not_found(self):
        self.meet_event.event_type.delete()
        response = self.client.get(self.url)
        print(response)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_update_seed_time_success(self):
        data = {"id": 1, "date": datetime.datetime.now(), "time": "00:00:99.360000"}
        response = self.client.post(self.url, data, format='json')
        print(response)
        get_response = self.client.get(self.url)
        print(len(get_response.data))
        # a1 = Athlete.objects.get(id=2)
        # data = {'athlete_id': a1.id, 'time': 60}
        # response = self.client.post(self.url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
