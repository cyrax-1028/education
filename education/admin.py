from django.contrib import admin

from .models import Course

@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}



admin.site.site_header = 'RapqonEdu Admin'
admin.site.site_title = 'RapqonEdu Admin Portal'
admin.site.index_title = 'Welcome To RapqonEdu Researcher Portal'