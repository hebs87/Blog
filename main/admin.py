from django.contrib import admin

from .models import Blog


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    """ A custom BlogAdmin class to enable customising Blog admin view """
    list_display = ('title', 'date_created', 'last_modified', 'is_draft')
    list_filter = ('is_draft',)


admin.site.register(Blog, BlogAdmin)
