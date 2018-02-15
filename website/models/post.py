from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(_('post_title'), max_length=100)
    body = models.TextField(_('post_body'))
    tags = TaggableManager(_('post_tags'), help_text=_('post_tags_help_text'))
    create_time = models.DateTimeField(_('post_create_time'), auto_now_add=True)
    update_time = models.DateTimeField(_('post_update_time'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title
