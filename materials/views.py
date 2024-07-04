from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lessons, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (CoursesDetailSerializer, CourseSerializer,
                                   LessonsSerializer, SubscriptionSerializer)
from users.permissions import IsModerators, IsOwner


class CourseViewSet(ModelViewSet):
    """Эндпоинт для модели курсов"""

    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Функция для действия retrieve"""
        if self.action == "retrieve":
            return CoursesDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """Функция для действия create"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Функция для проверки доступа"""
        if self.action == "create":
            self.permission_classes = (~IsModerators,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerators | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerators | IsOwner,)
        return super().get_permissions()


class LessonsCreateApiView(CreateAPIView):
    """Эндпоинт для создания урока"""

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
    """Эндпоинт для просмотра уроков"""

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    pagination_class = CustomPagination


class LessonsRetrieveApiView(RetrieveAPIView):
    """Эндпоинт для получения 1-го урока"""

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerators | IsOwner,
    )


class LessonsUpdateApiView(UpdateAPIView):
    """Эндпоинт для обновления урока"""

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerators | IsOwner,
    )


class LessonsDestroyApiView(DestroyAPIView):
    """Эндпоинт для удаления урока"""

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerators)


class SubscriptionAPIView(APIView):
    """Эндпоинт для добавления/удаления подписки на курс"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(
            owner=user, course=course_item
        )
        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return Response({"message": message})
