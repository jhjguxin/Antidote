from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class EntryManager(models.Manager):
    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        taglist = defaults.pop('taglist', {})
        Entry.taglist = taglist
        kwargs.update(defaults)
        super(EntryManager, self).get_or_create(**kwargs)

class Entry(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateField(blank=True, null=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    taglist = []
    objects = EntryManager()

    def save(self, *args, **kwargs):
        super(Entry, self).save()
        for i in self.taglist:
            p, created = Tag.objects.get_or_create(name=i)
            self.tags.add(p)
        super(Entry, self).save()
        self.taglist = []

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
