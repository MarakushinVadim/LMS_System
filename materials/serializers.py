from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lessons


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = "__all__"


class CoursesDetailSerializer(ModelSerializer):
    lesson_count_in_this_course = SerializerMethodField()
    information_all_lessons = LessonsSerializer(many=True, source="lessons_set.all")

    def get_lesson_count_in_this_course(self, course):
        return Lessons.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "preview",
            "description",
            "lesson_count_in_this_course",
            "information_all_lessons",
        ]
