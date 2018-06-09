from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from website import models
from website.views.page import Page


class Posts(Page, ListView):
    template_name = 'posts.html'
    model = models.Event

    allow_empty = True
    ordering = '-start_time'
    paginate_by = 20
    paginate_orphans = 30

    show_headline = False

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag', None)
        keyword = self.request.GET.get('search', None)
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        elif tag:
            queryset = queryset.filter(tags__name__in=(tag,))
        else:
            queryset = queryset.all()

        if self.show_headline:
            headline = self.get_headline()
            if headline:
                queryset = queryset.exclude(id__in=(headline.id,))
        return queryset

    def get_context_data(self, *args, **kwargs):
        current_tag = self.request.GET.get('tag', None)
        keyword = self.request.GET.get('search', None)

        nav_items = []
        nav_items.append({
            'name': '全部活動',
            'link': reverse('home'),
            'active': not current_tag and not keyword
        })
        for tag in models.HomeTab.objects.order_by('order').all():
            nav_items.append({
                'name': tag.name,
                'link': '%s?tag=%s' % (reverse('posts'), tag.name),
                'active': current_tag == tag.name
            })

        context_data = super().get_context_data(*args, **kwargs)
        context_data['search'] = {
            'target': reverse('posts'),
            'placeholder': '搜尋活動'
        }
        context_data['keyword'] = keyword
        context_data['headline'] = self.get_headline()
        context_data['login_modal'] = self.get_login_modal()
        context_data['meta_title'] = '李江却台語文教基金會'
        context_data['nav_items'] = nav_items
        context_data['show_headline'] = self.show_headline
        return context_data

    def get_headline(self):
        now = timezone.now()
        try:
            headline = (
                models.Headline.objects
                .filter(start_time__lte=now, end_time__gte=now)
                .latest('start_time')
            )
            return headline
        except ObjectDoesNotExist:
            return None
