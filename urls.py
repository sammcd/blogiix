from django.conf.urls.defaults import *


urlpatterns = patterns('',
	# References to blog
	(r'^blog/$', 'blogiix.views.index'),
    (r'^$', 'blogiix.views.index'),

	# Short URL
	(r'^s/(?P<short_hash>\w+)/$', 'blogiix.views.short_url'),
	
	# Archive view
	(r'^archive$', 'blogiix.views.archive_view'),
	
	# Each part of the long URL
	(r'^blog/(?P<year>\d{4})/$', 'blogiix.views.year_view'),
	(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/$', 'blogiix.views.month_view'),
	(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'blogiix.views.day_view'),
	
	#Legacy URLs
	(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<url_title>[a-zA-Z0-9_|-]+)', 'blogiix.views.post_view'),
	
	#Newer URLS
	(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<url_title>[a-zA-Z0-9_|-]+)', 'blogiix.views.post_view'),
	
	
	# Form Submissions
	(r'^blog/post-comment/(?P<id>\d*)/$', 'blogiix.views.post_comment'),
	
	(r'^feeds/rss', 'blogiix.views.rss_feed'),
)