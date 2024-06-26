from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lessons
from materials.serializers import CourseSerializer, LessonsSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonsCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsListApiView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsRetrieveApiView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsUpdateApiView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyApiView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
