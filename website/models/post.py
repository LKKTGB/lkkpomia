from bs4 import BeautifulSoup
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(_('post_title'), max_length=100)
    body = HTMLField(_('post_body'))
    tags = TaggableManager(_('post_tags'), help_text=_('post_tags_help_text'))
    create_time = models.DateTimeField(_('post_create_time'), auto_now_add=True)
    update_time = models.DateTimeField(_('post_update_time'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'title__icontains',)

    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        soup = BeautifulSoup(self.body, 'html.parser')
        tags = soup.findAll('img')
        return tags[0]['src'] if tags else None

    @property
    def summary(self):
        soup = BeautifulSoup(self.body, 'html.parser')
        for br in soup.find_all("br"):
            br.replace_with("\n")
        ps = [t for t in soup.findAll('p') if t.text.strip()]
        return ps[0].text if ps else None
