from django.contrib import admin

from .models import Blog


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    """ A custom BlogAdmin class to enable customising Blog admin view """
    list_display = ('title', 'date_created', 'last_modified', 'is_draft')
    list_filter = ('is_draft',)
    search_fields = ('title',)
    # One way to order - this does it for all users
    # ordering = ('title', '-date_created')

    def get_ordering(self, request):
        """ Override get_ordering method to customise ordering based on user type """
        if request.user.is_superuser:
            return 'title', '-date_created'

        return 'title'


admin.site.register(Blog, BlogAdmin)
