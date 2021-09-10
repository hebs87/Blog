from django.db import models


# Create your models here.
class Blog(models.Model):

    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(max_length=3000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title
