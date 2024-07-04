from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lessons, Subscription
from users.models import User


class LessonsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="123qwe")
        self.course = Course.objects.create(
            name="test_course", description="test_course description"
        )
        self.lesson = Lessons.objects.create(
            name="test_lesson",
            description="test_lesson description",
            video_link="www.youtube.com/watch",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lessons_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], self.lesson.name)

    def test_lessons_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "name": "test lesson",
            "description": "test lesson description",
            "video_link": "www.youtube.com",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lessons.objects.all().count(), 2)

    def test_lessons_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "updated_lesson",
            "description": "updated_lesson description",
            "video_link": "www.youtube.com/watch",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lessons.objects.get(pk=self.lesson.pk).name, "updated_lesson")

    def test_lessons_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lessons.objects.all().count(), 0)

    def test_lessons_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_link": self.lesson.video_link,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="123qwe")
        self.course = Course.objects.create(
            name="test_course", description="test_course description"
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk, "owner": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)

    def test_subscription_delete(self):
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk, "owner": self.user.pk}
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
