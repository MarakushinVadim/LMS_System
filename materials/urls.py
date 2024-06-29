from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonsCreateApiView,
                             LessonsDestroyApiView, LessonsListApiView,
                             LessonsRetrieveApiView, LessonsUpdateApiView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)
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
]
urlpatterns += router.urls
