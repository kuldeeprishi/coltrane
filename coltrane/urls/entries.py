from django.conf.urls.defaults import *
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from coltrane.models import Entry


entry_info_dict = {
    'model': Entry,
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}

# Views for Entry Model
urlpatterns = patterns('',
    url(r'^$', ArchiveIndexView.as_view(**entry_info_dict), name='coltrane_entry_archive_index'),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(make_object_list = True, allow_future = True, **entry_info_dict), name='coltrane_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', MonthArchiveView.as_view(**entry_info_dict), name='coltrane_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', DayArchiveView.as_view(**entry_info_dict), name='coltrane_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', DateDetailView.as_view(**entry_info_dict), name='coltrane_entry_detail'),
)