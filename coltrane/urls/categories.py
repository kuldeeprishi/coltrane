from django.conf.urls.defaults import *
from django.views.generic.list import ListView
from coltrane.models import Category

# Views for Category
urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model = Category), name='coltrane_category_list'),
    url(r'^(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail'),
)

