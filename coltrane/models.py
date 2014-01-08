import datetime
from django.conf import settings

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from tagging.fields import TagField


class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text = 'Suggested value will be generated automatically from title. Must be unique.')  # short text for user in url
    description = models.TextField(help_text='Provide a short description of your category.')

    class Meta:
        ordering = ['title']
        verbose_name_plural = ("Categories")

    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '%s' % self.slug

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
            (LIVE_STATUS, 'Live'),
            (DRAFT_STATUS, 'Draft'),
            (HIDDEN_STATUS, 'Hidden'),
            )
    # Core fields
    title = models.CharField(max_length=250, help_text="Maximum 250 characters.")
    excerpt = models.TextField(blank=True, help_text="A short summary of the entry. (Optional)") # optional, brief description
    body = models.TextField()
    pub_date = models.DateTimeField(default = datetime.datetime.now)

    # Fields to store generated html
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # Metadata
    author = models.ForeignKey(User)
    enable_commments = models.BooleanField(default = True)
    featured = models.BooleanField(default = False)
    slug = models.SlugField(unique_for_date='pub_date', help_text="Suggested value will be automatically generated from \
                                                                    title. Must be unique")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text="Only entries with live \
                                                                                    status will be publically displayed.")

    # Categorization
    categories = models.ManyToManyField(Category)
    tags = TagField(help_text="Separate tags with spaces.")

    live = LiveEntryManager()    
    objects = models.Manager()




    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)


    class Meta:
        verbose_name_plural = ("Entries")
        ordering = ["-pub_date"]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (), {'year': self.pub_date.strftime("%Y"),
                                                'month': self.pub_date.strftime("%b").lower(),
                                                'day':self.pub_date.strftime("%d"),
                                                'slug': self.slug})


class Link(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False,blank=True)
    url = models.URLField(unique=True)

    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    tags = TagField()

    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to delicious', default=True)

    via_name = models.CharField('Via', max_length=250, blank=True, help_text='The name of person whose site you spotted the link on. Optional')
    via_url = models.URLField('Via URL', blank=True, help_text='The URL of site where you spotted the link. Optional')

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.id and self.post_elsewhere:
            import pydelicious
            from django.utils.encoding import smart_str
            pydelicious.add(settings.DELICIOUS_USER,
                            settings.DELICIOUS_PASSWORD,
                            smart_str(self.url),
                            smart_str(self.title),
                            smart_str(self.tags))
        if self.description:
            self.description_html = markdown(self.description)
        super(Link, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_link_detail', (), {'year':self.pub_date.strftime('%Y'),
                                            'month':self.pub_date.strftime('%b').lower(),
                                            'day':self.pub_date.strftime('%d'),
                                            'slug':self.slug})
