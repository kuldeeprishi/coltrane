from django.conf.urls.defaults import *
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from coltrane.models import Link

link_info_dict = {
    'model': Link,
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
}

# Views for the Link Model
urlpatterns = patterns('',
    url(r'^$', ArchiveIndexView.as_view(**link_info_dict), name='coltrane_link_archieve_index'),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(make_object_list = True, allow_future = True, **link_info_dict), name='coltrane_link_archieve_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', MonthArchiveView.as_view(**link_info_dict), name='coltrane_link_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', DayArchiveView.as_view(**link_info_dict), name='coltrane_link_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', DateDetailView.as_view(**link_info_dict), name='coltrane_link_detail'),

)