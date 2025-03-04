from django.contrib import admin

from .models import Course, Group, Lesson, Attendance, Video, EmailConfirmation, Students_of_group

@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "teacher")
    search_fields = ("name", "course__title", "teacher__user__username")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "date")
    search_fields = ("title", "group__name")
    list_filter = ("date",)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "is_present", "grade")
    search_fields = ("student__user__username", "lesson__title")
    list_filter = ("is_present",)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("lesson", "video_file")
    search_fields = ("lesson__title",)

@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")
    search_fields = ("user__email", "token")

@admin.register(Students_of_group)
class Students_of_groupAdmin(admin.ModelAdmin):
    list_display = ("student", "group")


admin.site.site_header = 'RapqonEdu Admin'
admin.site.site_title = 'RapqonEdu Admin Portal'
admin.site.index_title = 'Welcome To RapqonEdu Researcher Portal'