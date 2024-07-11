from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (AmountsCreateAPIView, CourseViewSet,
                             LessonsCreateApiView, LessonsDestroyApiView,
                             LessonsListApiView, LessonsRetrieveApiView,
                             LessonsUpdateApiView, SubscriptionAPIView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")
urlpatterns = [
    path("lessons/", LessonsListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>", LessonsRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonsCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete",
        LessonsDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update", LessonsUpdateApiView.as_view(), name="lessons_update"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
    path("amounts_create/", AmountsCreateAPIView.as_view(), name="amounts-create"),
]
urlpatterns += router.urls
