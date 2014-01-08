from django.shortcuts import get_object_or_404, render_to_response
from coltrane.models import Entry, Category
from tagging.models import Tag, TaggedItem
from tagging.utils import get_tag
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _

from django.http import Http404



def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('coltrane/category_detail.html',
                                {'object_list':category.live_entry_set(),
                                'category':category})


