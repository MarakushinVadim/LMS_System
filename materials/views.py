import datetime

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from LMS_System import settings
from materials.tasks import check_courses
from materials.models import Amounts, Course, Lessons, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (AmountsSerializer, CoursesDetailSerializer,
                                   CourseSerializer, LessonsSerializer,
                                   SubscriptionSerializer)
from materials.services import (create_stripe_price, create_stripe_product,
                                create_stripe_session)
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

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.last_update_date = datetime.datetime.now()
        instance.save()
        check_courses.delay(instance.pk)
        return instance

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
        course_amount = self.request.data.get("course_amount")
        course_item = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(
            owner=user, course=course_item, amount=course_amount
        )
        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:

            message = "Подписка добавлена"

        return Response({"message": message})


class AmountsCreateAPIView(CreateAPIView):
    """
    Эндпоинт для создания платежа
    необходимо корректно заполнить поля
    обязательные поля - user, amount, product
    user - ожидается ввод pk юзера,
    amount - ожидается значение в int,
    product - ожидается ввод pk курса
    """

    serializer_class = AmountsSerializer
    queryset = Amounts.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment.product)
        price = create_stripe_price(amount=payment.amount)
        session_id, session_url = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = session_url
        payment.save()
