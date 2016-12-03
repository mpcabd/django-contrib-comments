from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _
from django.conf import settings

SITE_DOMAIN = getattr(settings, 'SITE_DOMAIN', 'example.com')
SITE_NAME = getattr(settings, 'SITE_NAME', 'example.com')

import django_comments


class LatestCommentFeed(Feed):
    """Feed of latest comments on the current site."""

    def __call__(self, request, *args, **kwargs):
        return super(LatestCommentFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return _("%(site_name)s comments") % dict(site_name=SITE_NAME)

    def link(self):
        return "http://%s/" % SITE_DOMAIN

    def description(self):
        return _("Latest comments on %(site_name)s") % dict(site_name=SITE_NAME)

    def items(self):
        qs = django_comments.get_model().objects.filter(
            is_public=True,
            is_removed=False,
        )
        return qs.order_by('-submit_date')[:40]

    def item_pubdate(self, item):
        return item.submit_date
