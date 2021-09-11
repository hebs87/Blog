from django.contrib import admin, messages

from .models import Blog


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    """ A custom BlogAdmin class to enable customising Blog admin view """
    list_display = ('title', 'date_created', 'last_modified', 'is_draft')
    list_filter = ('is_draft', 'date_created')
    search_fields = ('title',)
    exclude = ('slug',)
    list_per_page = 50
    date_hierarchy = 'date_created'
    # How to generate field automatically based on another field
    # prepopulated_fields = {
    #     'slug': ('title',)
    # }
    # One way to order - this does it for all users
    # ordering = ('title', '-date_created')

    # fields = ('title', 'body', 'is_draft', ('date_created', 'last_modified'))
    fieldsets = (
        (
            'Details',
            {
                # Can also add classes and description properties
                'fields': ('title', 'body'),
                'description': 'The Title is required'
            }
        ),
        (
            'Status',
            {
                # Can also add classes and description properties
                'fields': ('is_draft',),
            }
        ),
        (
            'Key Dates',
            {
                # Can also add classes and description properties
                'fields': (('date_created', 'last_modified'),),
            }
        ),
    )
    readonly_fields = ('date_created', 'last_modified')

    actions = ('set_blogs_to_published',)

    def get_ordering(self, request):
        """ Override get_ordering method to customise ordering based on user type """
        if request.user.is_superuser:
            return 'title', '-date_created'

        return 'title'

    def set_blogs_to_published(self, request, queryset):
        """ Custom action to set selected Blogs' is_draft to False - show success or warning message """
        try:
            count = queryset.update(is_draft=False)
            # Display a success message to the user
            self.message_user(
                request,
                f'{count} {"Blog has" if count == 1 else "Blogs have"} been successfully published'
            )
        except:
            self.message_user(request, f'Unable to publish selected Blog', level=messages.WARNING)
    set_blogs_to_published.short_description = 'Mark selected Blogs as published'


admin.site.register(Blog, BlogAdmin)
