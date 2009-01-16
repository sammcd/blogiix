# Create your views here.
from blogiix.models import Post, Comment, CommentForm, ShortUrl
from blogiix.config import BlogConfig
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from blogiix.akismet import Akismet

############################################################################
# Displaying Blog Posts
############################################################################

def index(request):
	allPosts = Post.objects.order_by('-date_posted')
	post = Post.objects.filter(preview=False).order_by('-date_posted')[0]
	
	return post_view(request, post.date_posted.year,post.month(),post.day(),post.url_title())
	
def post_view(request, year, month, day, url_title):
	title_from_url = Post.title_from_url(url_title)
	post = Post.objects.filter(date_posted__year=year).filter(date_posted__month=int(month)).filter(date_posted__day=int(day)).filter(title = title_from_url)[0]
	comments = Comment.objects.filter(post__id=post.pk).filter(is_spam=False).order_by('date_posted')
	post.views = post.views + 1
	post.save()
	form = CommentForm()
	return render_to_response('blog/post_view.html', {'post' : post, 
		'url_title' : url_title,
		'comments': comments,
		'form': form}, 
		RequestContext(request))

	
def year_view(request, year):
	posts = Post.objects.filter(date_posted__year=year).filter(preview=False).order_by('-date_posted')
	return render_to_response('blog/overview.html', {'posts': posts, 
		'sub_heading': 'Year View - %s' % (year)}, 
		RequestContext(request))
		
def month_view(request, year, month):
	posts = Post.objects.filter(date_posted__year=year).filter(preview=False).filter(date_posted__month=month).order_by('-date_posted')
	return render_to_response('blog/overview.html', {'posts': posts,
		'sub_heading': 'Month View - %s.%s' % (year, month)},
		RequestContext(request))
		
def day_view(request, year, month, day):
	posts = Post.objects.filter(date_posted__year=year).filter(preview=False).filter(date_posted__month=month).filter(date_posted__day=day).order_by('-date_posted')
	return render_to_response('blog/overview.html', {'posts': posts,
		'sub_heading': 'Day View - %s.%s.%s' % (year, month, day)},
		RequestContext(request))	
		
def archive_view(request):
	
	posts = Post.objects.filter(preview=False).order_by('-date_posted')
	year_array = [];
	
	# Loop through each post making a note of all the different years?
	current_year = posts[0].date_posted.year
	next_cut = 0
	count = 0
	for i in range(0,len(posts)):
		if posts[i].date_posted.year != current_year:
			year_array.append( {'year': current_year, 'posts' : posts[next_cut:i] } )
			current_year = posts[i].date_posted.year
		 	next_cut = count + 1
		
	year_array.append( {'year': current_year, 'posts' : posts[next_cut:] } )
			
	return render_to_response('blog/archive_view.html', { 'years': year_array, 'posts':posts}, RequestContext(request))		

############################################################################
# Displaying Comments
############################################################################	
def post_comment(request, id):
	post = get_object_or_404(Post, pk=id)
	cin = request.POST
	request_meta = request.META
	valid = False
	spam = 0
	
	
	#Check if the form is valid
	form = CommentForm(request.POST)
	if not form.is_valid():
		return render_to_response('blog/comment_invalid.html', {'post': post, 'form': form }, RequestContext(request))
	
	# Now that comment is valid, check if it is spam
	api = Akismet(key=BlogConfig.akismet_key, blog_url=BlogConfig.url, agent=None)
	if api.verify_key():
		# API Key is valid
		valid = True
		
		# Create Data object
		# TODO: Add perma link
		data = {}
		data['user_ip'] = request_meta['REMOTE_ADDR']
		data['user_agent'] = request_meta['HTTP_USER_AGENT']
		data['comment_type'] = 'comment'
		data['comment_author'] = cin['name']
		data['comment_author_email'] = cin['email']
		data['comment_author_url'] = cin['url']
		
		
		if 'HTTP_REFERER' in request_meta:
			data['referrer'] = request_meta['HTTP_REFERER']
		
		if api.comment_check(cin['text'], data):
			# True means spam
			spam = 1
	
	c = Comment(post=post, text=cin['text'], name=cin['name'], email=cin['email'], url=cin['url'], is_spam=spam)
	c.save()

	
	return render_to_response('blog/comment_submitted.html', 
		{'post': post, 'spam': spam, 'valid': valid, 'test': BlogConfig.url}, 
		RequestContext(request))

############################################################################
# OTHER Short Urls, RSS
############################################################################
def short_url(request, short_hash):
	post_id = ShortUrl.hash_to_id(short_hash)
	short_url_record = get_object_or_404(ShortUrl, pk=post_id)
	return HttpResponsePermanentRedirect(short_url_record.url)


def rss_feed(request):
	link = BlogConfig.url
	posts = Post.objects.all().filter(preview=False).order_by('-date_posted')
	return render_to_response('blog/feeds/rss.html', {'posts': posts, 'link': link})