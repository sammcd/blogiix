from django.db import models
from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import ModelForm
from blogiix.config import BlogConfig
import datetime, time

import re # Regular expressions


# Posts Model
class Post(models.Model):
  text = models.TextField()
  title = models.CharField(max_length = 100)
  date_posted = models.DateTimeField(auto_now_add=True)
  views = models.IntegerField(default=0)
  preview = models.BooleanField(default=False)
  def __unicode__(self):
    return self.title
  
    
  @models.permalink
  def get_absolute_url(self):
    
    return ('post_view', (), {
      'year': self.date_posted.year,
      'month': self.month(),
      'day': self.day(),
      'url_title': self.url_title()})
    #return ('blog.views.post_view', [self.date_posted.year, self.month(), self.day(), self.url_title()])
    #return "/blog/%s/%s/%s/%s" % (self.date_posted.year, self.month(), self.day(), self.url_title())
    
  def url_title(self):
    p = re.compile('\s')
    return p.sub('-', self.title)
    
  #Creates a URL from the title of the post
  @staticmethod
  def title_from_url(title):
    p = re.compile('-')
    return p.sub(' ', title)
    
  def string_id(self):
    return "%s" % self.id
    
  # Used by templates to put leading 0 in front of months
  def month(self):
    date = self.date_posted
    if date.month > 9:
      return date.month
    else:
      return '0%i' % date.month
  
  # Used by template to put leading 0 in front of day for urls
  def day(self):
    date = self.date_posted
    if date.day > 9 :
      return date.day
    else:
      return '0%i' % date.day
  
  # Used by templates to display number of comments   
  def num_comments(self):
    comments = Comment.objects.filter(post=self).filter(is_spam=False)
    return comments.count()
    
  # Used for templates to determine proper grammer
  def one_comment(self):
    if ( self.num_comments() == 1 ):
      return True;
    else:
      return False;
  

#Comments Model
class Comment(models.Model):
  post = models.ForeignKey(Post, blank=True)
  text = models.TextField()
  name = models.CharField(max_length = 50)
  email = models.EmailField(blank=True)
  url = models.CharField(max_length = 100, blank=True)
  is_owner = models.BooleanField(blank=True, default=False)
  email_sent = models.BooleanField(blank=True, default=False)
  date_posted = models.DateTimeField(auto_now_add=True)
  is_spam = models.BooleanField(blank=True, default=False)
  
  def __unicode__(self):
    return '%s - %s' % (self.name, self.email)
    
  def relative_time(self):
    # Seconds since post
    difference =  time.time() - time.mktime(self.date_posted.timetuple())
    
    minutes = difference / 60.0
    hours = minutes / 60.0 
    days = hours / 24
    
    if minutes < 60:
      if int(minutes) == 1:
        relative_time = '1 minute ago'
      else:
        relative_time = '%s minutes ago' % int(minutes)
    elif int(hours) < 24:
      if hours == 1:
        relative_time = '1 hour ago'
      else:
        relative_time = '%s hours ago' % int(hours)
    else:
      if int(days) == 1:
        relative_time = '1 day ago'
      else:
        relative_time = '%s days ago' % int(days)


    # Measure in the 
    return relative_time
    
#Tiny URL work
class ShortUrl(models.Model):
  url = models.CharField(max_length = 200)
  
  def short_url(self):
    return '%s/s/%s' % (BlogConfig.url, self.short_hash())
  
  def short_hash(self):
    
    number = "%s" % (self.pk)
    
    fromdigits = "0123456789"
    todigits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"

    # make an integer out of the number
    x=long(0)
    for digit in str(number):
      x = x*len(fromdigits) + fromdigits.index(digit)

    # create the result in base 'len(todigits)'
    res=""
    while x>0:
      digit = x % len(todigits)
      res = todigits[digit] + res
      x /= len(todigits)

    return res

  @staticmethod
  def hash_to_id(number):
    fromdigits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
    todigits = "0123456789"

    # make an integer out of the number
    x=long(0)
    for digit in str(number):
      x = x*len(fromdigits) + fromdigits.index(digit)

    # create the result in base 'len(todigits)'
    res=""
    while x>0:
      digit = x % len(todigits)
      res = todigits[digit] + res
      x /= len(todigits)

    return res

  def __unicode__(self):
    return "%s: %s" % (self.short_hash(), self.url)



#Set up form for validation
class CommentForm(ModelForm):
  class Meta:
    model = Comment