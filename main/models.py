from django.db import models


# Create your models here.
class Blog(models.Model):

    slug = models.SlugField(max_length=100, blank=False)
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

    def save(self, *args, **kwargs):
        """ Override save method to create slug if it is not present """
        if not self.slug:
            # Convert title to lower case, split words and join with a hyphen
            title_words = self.title.lower().split(' ')
            self.slug = '-'.join(title_words)

        super(Blog, self).save(*args, **kwargs)
