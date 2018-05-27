from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.post import Post

class Headline(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('post'))
    start_time = models.DateTimeField(_('headline_start_time'))
    end_time = models.DateTimeField(_('headline_end_time'))

    class Meta:
        verbose_name = _('headline')
        verbose_name_plural = _('headlines')


    def __str__(self):
        return self.post.title
