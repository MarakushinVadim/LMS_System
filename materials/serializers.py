from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lessons
from materials.validators import validate_url


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonsSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_url])

    class Meta:
        model = Lessons
        fields = "__all__"


class CoursesDetailSerializer(serializers.ModelSerializer):
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


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id',)
