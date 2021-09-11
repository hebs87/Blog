from django.db import models


# Create your models here.
class Blog(models.Model):

    slug = models.SlugField(max_length=100, blank=False)
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(max_length=3000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)
    categories = models.ManyToManyField('main.Category')

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save method to create slug if it is not present,
        or if editing the record and title has changed
        """
        existing_record = None
        if self.pk:
            existing_record = Blog.objects.get(pk=self.pk)

        if not existing_record or existing_record.title != self.title:
            self.slug = self.generate_slug(self.title)

        super(Blog, self).save(*args, **kwargs)

    @staticmethod
    def generate_slug(title):
        """ Convert title to slug - lowercase title separated by hyphens instead of spaces """
        title_words = title.lower().split(' ')
        return '-'.join(title_words)


class Comment(models.Model):

    # related_name is what we will refer to this model as from the Blog model
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000)
    is_active = models.BooleanField(blank=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('main.Category')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        if len(self.comment) > 50:
            return f'{self.blog} - {self.comment[:50]}...'

        return f'{self.blog} - {self.comment}'


class Category(models.Model):

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        if len(self.name) > 50:
            return f'{self.name[:50]}...'

        return f'{self.name}'
