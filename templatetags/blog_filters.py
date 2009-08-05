from django import template
from django.template.defaultfilters import stringfilter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re                   

import urllib, hashlib

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
 
@register.filter(name='relative_time')
def relative_time(timestamp):
	
	return timestamp

@register.filter(name='encode_email')
@stringfilter
def encode_email(email):
  new_string = ''
  last_letter = email[-1]
  for char in email:
    # Mix both html-ascii and actual characters
    if char == last_letter:  
      new_string = new_string + last_letter
    else:
      new_string = new_string + '&#' + str(ord(char)) + ';'       
  return new_string

                            
@register.filter(name='gravatar')
def gravatar(email):
	# Size of gravitar
	size = 45

	# construct the url
	gravatar_url = "http://www.gravatar.com/avatar/"
	gravatar_url += hashlib.md5(email).hexdigest()
	gravatar_url += '?d=identicon'
	return gravatar_url

@register.filter(name='newline_to_p')
@stringfilter
def newline_to_p(value):
	p = re.compile('\n')
	parRep = '<p>' + p.sub('</p><p>',value)
	return parRep + "</p>"
	

	
