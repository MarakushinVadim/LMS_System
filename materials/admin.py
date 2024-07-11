from django.contrib import admin

from materials.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "name",
        'amount',
        'last_update_date',
    )
