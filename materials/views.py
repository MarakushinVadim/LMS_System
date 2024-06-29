from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lessons
from materials.serializers import (CoursesDetailSerializer, CourseSerializer,
                                   LessonsSerializer)
from users.permissions import IsModerators, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CoursesDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerators,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerators | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerators | IsOwner,)
        return super().get_permissions()


class LessonsCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModerators,
    )

    def perform_create(self, serializer):
        lessons = serializer.save()
        lessons.owner = self.request.user
        lessons.save()


class LessonsListApiView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsRetrieveApiView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerators | IsOwner,
    )


class LessonsUpdateApiView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerators | IsOwner,
    )


class LessonsDestroyApiView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerators)
