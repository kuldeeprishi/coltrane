from django.conf.urls import *
#from coltrane.urls import urlpatterns as coltraneurls



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^cms/', include('cms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': 'C:/virtual_env/django_project/cms/templates/tinymce/js/tinymce/'}),
    (r'^search/$', 'search.views.search'),
    url(r'weblog/categories/', include('coltrane.urls.categories')),
    url(r'weblog/links/', include('coltrane.urls.links')),
    url(r'weblog/tags/', include('coltrane.urls.tags')),
    url(r'^weblog/', include('coltrane.urls.entries')),
    url(r'^comment/', include('django.contrib.comments.urls')),

    (r'', include('django.contrib.flatpages.urls')),
)