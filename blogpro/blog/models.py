from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = AutoSlugField(
        populate_from='title',
        unique=True,
        editable=False,
        always_update=False,
        blank=True,
        verbose_name='Slug标识',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def delete_url(self):
        return reverse(
            'blog:post_delete',
            args=[
                self.slug,
            ]
        )

    def update_url(self):
        return reverse(
            'blog:blog_update',
            args=[
                self.slug,
            ]
        )

    def get_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ]
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_comment'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.commenter.username, self.post)