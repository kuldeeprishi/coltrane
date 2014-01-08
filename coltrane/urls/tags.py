from django.conf.urls.defaults import *
from tagging.models import Tag
from tagging.views import TaggedObjectListView, ListView
from coltrane.models import Entry, Link

# Views for Tag
urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model = Tag), name='coltrane_tag_list'),
    url(r'^entries/(?P<tag>[-\w]+)/$', TaggedObjectListView.as_view(queryset = Entry.live.all(), template_name = 'coltrane/entries_by_tag.html') ),
    url(r'^links/(?P<tag>[-\w]+)/$', TaggedObjectListView.as_view(model = Link, template_name = 'coltrane/links_by_tag.html') ),
)