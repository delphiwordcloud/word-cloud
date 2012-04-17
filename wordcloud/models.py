__author__ = 'michael odland'

from django.db import models
from django.contrib.auth.models import User
import linguist


"""
class Text(models.Model):
    title = models.CharField(max_length=200)
    file  = models.FilePathField()
    def __unicode__(self):
        return u'%s %s' %(self.title, self.file.name)
"""

class Corpus(models.Model):
    title  = models.CharField(max_length=200)
    file   = models.FileField(upload_to='uploaded_text/') #FilePathField(path='/', recursive=True)
    user   = models.ForeignKey(User)
    #text   = models.ForeignKey(Text)
    #todo: when I get to corpus sharing uncomment next line
    #users  = models.ManyToManyField(User)
    def __unicode__(self):
        return u'%s %s' %(self.title, self.user.username)

class Profile(models.Model):
    corpus  = models.ForeignKey(Corpus)
    pairs   = models.TextField(max_length=None)
    context = models.TextField(max_length=None)

class Json(models.Model):
    name   = models.CharField(max_length=64, unique=True)
    data_stream = models.TextField(max_length=None)
    corpus = models.ForeignKey(Corpus)
    def __unicode__(self):
        return u'%s %s' %(self.name, self.corpus.file)

class Settings(models.Model):
    profile   = models.ForeignKey(Profile)
    charCount = models.IntegerField()
    wordCount = models.IntegerField()

class Tag(models.Model):
    name    = models.CharField(max_length=64, unique=True)
    corpora = models.ManyToManyField(Corpus)
    def __unicode__(self):
        return u'%s %s' % self.name

class Cloud(models.Model):
    name  = models.CharField(max_length=200)
    json  = models.ForeignKey(Json)
    user  = models.ForeignKey(User)
    #todo figure out HTML5 canvas to image conversion and uncomment next line
    #image = models.ImageField()
    def __unicode__(self):
        return u'%s %s' %(self.name, self.json.file, self.user.username)