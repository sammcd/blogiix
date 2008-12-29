from blogiix.models import Post
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def blog_processors(request):
	recent_posts = Post.objects.filter(preview=False).order_by('-date_posted')[:5]
	popular_posts = Post.objects.order_by('-views')[:3]
	#code_css =  HtmlFormatter(style='native').get_style_defs('.highlight') Use for creating pygments theme
	return {'recent_posts': recent_posts, 
		'popular_posts': popular_posts}
		
