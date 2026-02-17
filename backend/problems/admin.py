from django.contrib import admin
from .models import Problem, TestCase, Topic, Tag


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 3
    fields = ['input_data', 'expected_output', 'is_public', 'order']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'difficulty', 'points',
                    'acceptance_rate', 'total_submissions', 'is_active']
    list_filter  = ['difficulty', 'is_active', 'is_premium']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline]
    filter_horizontal = ['topics', 'tags']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']