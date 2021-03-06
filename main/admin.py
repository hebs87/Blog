from django.utils import timezone
from django.contrib import admin, messages
from django.db.models import Count

from django_summernote.admin import SummernoteModelAdmin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateTimeRangeFilter
from import_export.admin import ImportExportModelAdmin

from .models import Blog, Comment, Category
from .resources import CommentResource


# Register your models here.
# TabularInline displays field in a row, StackedInline displays the fields as stacked
class CommentInline(admin.TabularInline):
    """ A custom CommentInline to enable crud operations on related Comment records from BlogAdmin """
    model = Comment
    fields = ('comment', 'is_active')
    extra = 0
    # Allows classes modification in Inline
    classes = ('collapse',)


# Inherit from SummernoteModelAdmin, which is a sub class of admin.ModelAdmin
class BlogAdmin(SummernoteModelAdmin):
    """ A custom BlogAdmin class to enable customising Blog admin view """
    list_display = ('title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation', 'no_of_comments')
    list_filter = ('is_draft', ('date_created', DateTimeRangeFilter))
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
    # This can also be filter_vertical
    filter_horizontal = ('categories',)
    summernote_fields = ('body',)
    fieldsets = (
        (
            'Details',
            {
                # Can also add classes and description properties
                'fields': ('title', 'body', 'categories',),
                'description': 'The Title is required'
            }
        ),
        (
            'Status',
            {
                # Can also add classes and description properties
                'fields': ('is_draft',),
                'classes': ('collapse',),
            }
        ),
        (
            'Key Dates',
            {
                # Can also add classes and description properties
                'fields': (('date_created', 'last_modified'),),
                'classes': ('collapse',),
            }
        ),
    )
    readonly_fields = ('date_created', 'last_modified')
    inlines = (CommentInline,)

    actions = ('set_blogs_to_published',)

    def get_queryset(self, request):
        """ Override get_queryset method to also return number of comment per Blog """
        qs = super(BlogAdmin, self).get_queryset(request)
        # annotate() adds value to each record in qs - we want to add number of comments
        # 'comments' is related_name for blog field in Comment model
        qs = qs.annotate(comments_count=Count('comments'))
        return qs

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

    def no_of_comments(self, obj):
        """ A custom column in the list display to show the comments_count (added to Blog record in get_queryset """
        return obj.comments_count
    # Allow ordering by comments field in list view
    no_of_comments.admin_order_field = 'comments_count'

    def days_since_creation(self, obj):
        """ A custom column in the list display to show the days since creation """
        diff = timezone.now() - obj.date_created
        return diff.days
    days_since_creation.short_description = 'Days Active'


class CommentAdmin(ImportExportModelAdmin):
    """ A custom CommentAdmin class to enable customising Comment admin view """
    list_display = ('get_comment', 'blog', 'date_created', 'is_active')
    list_filter = ('is_active', 'date_created', ('blog', RelatedDropdownFilter))
    # Allows editing the field directly from the change list
    list_editable = ('is_active',)
    search_fields = ('comment',)
    list_per_page = 50
    date_hierarchy = 'date_created'
    ordering = ('blog', 'comment', '-date_created')
    fieldsets = (
        (
            'Details',
            {
                # Can also add classes and description properties
                'fields': ('blog', 'comment'),
            }
        ),
        (
            'Status',
            {
                # Can also add classes and description properties
                'fields': ('is_active',),
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
    resource_class = CommentResource
    # list_select_related = ('blog',)
    raw_id_fields = ('blog',)

    actions = ('set_comment_to_inactive',)

    def set_comment_to_inactive(self, request, queryset):
        """ Custom action to set selected Comments' is_active to False - show success or warning message """
        try:
            count = queryset.update(is_active=False)
            # Display a success message to the user
            self.message_user(
                request,
                f'{count} {"Comment has" if count == 1 else "Comments have"} been successfully deactivated'
            )
        except:
            self.message_user(request, f'Unable to publish selected Blog', level=messages.WARNING)
    set_comment_to_inactive.short_description = 'Mark selected Comments as inactive'

    def get_comment(self, obj):
        """ A custom column in the list display to show the truncated comment """
        if len(obj.comment) > 50:
            return f'{obj.comment[:50]}...'

        return obj.comment
    get_comment.short_description = 'Comment'


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
