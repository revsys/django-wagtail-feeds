from django.urls import include, path
from wagtail import urls as wagtail_urls

from wagtail_feeds.feeds import BasicFeed, ExtendedFeed

urlpatterns = [
    path("blog/feed/basic", BasicFeed(), name="basic_feed"),
    path("blog/feed/extended", ExtendedFeed(), name="extended_feed"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    path("", include(wagtail_urls)),
]
