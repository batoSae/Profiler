from django.contrib import admin
from .models import User, Comment
from django.contrib.contenttypes.admin import GenericTabularInline

admin.site.site_header = "ProfilerApp Admin Area"
admin.site.site_title = "ProfilerApp Admin"
admin.site.index_title = "Welcome"

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class UserAdmin(admin.ModelAdmin):
    list_display = ['image_tag','user_fname','user_lname','user_email','user_position']
    search_fields = ['user_fname','user_lname','user_email','user_position']
    inlines = [CommentInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'user_id', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(active=True)

admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
# Register your models here.

