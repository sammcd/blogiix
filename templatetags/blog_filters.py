from django import template
from django.template.defaultfilters import stringfilter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re

register = template.Library()

@register.filter
@stringfilter
def code_convert(value):
	

	p = re.compile('<codecolor>')
	parted_tuple = p.split(value)
	
	
	if len(parted_tuple)  > 1:
	
		before_tag = parted_tuple[0]
		after_tag = parted_tuple[1]
		last_string = ''
		count = 1
		
		while ( after_tag != '') :
			#Convert value between <codecolor> tags
			q = re.compile('</codecolor>')
			in_tuple = q.split(after_tag)
			between_tags = in_tuple[0]
			between_tags = highlight(between_tags, PythonLexer(), HtmlFormatter())
			converted_value = '%s%s' % (before_tag, between_tags)
			
			#Prime for next trip through the loop
			last_string = in_tuple[1]
			last_split = p.split(in_tuple[1])
			count = count + 1

			if count < len(parted_tuple) :
				before_tag = '%s%s' % (converted_value, last_string)
				after_tag = parted_tuple[count]
			else:
				after_tag = ''
	
		converted_value = '%s%s' % (converted_value, last_string)
		return converted_value
	
	else:
		return value


@register.filter(name='newline_to_p')
@stringfilter
def newline_to_p(value):
	p = re.compile('\n')
	parRep = '<p>' + p.sub('</p><p>',value)
	return parRep + "</p>"
	

	
