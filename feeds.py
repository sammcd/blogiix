#! /usr/bin/env python
# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from django.contrib.syndication.feeds import Feed 
from blogiix.models import Post 
class AllPosts(Feed):
    __module__ = __name__
    title = "Sam McDonald's Blog"
    link = '/asdf'
    description = 'Updates on posts to sammcd.com'

    def items(self):
        return Post.objects.order_by('date_posted')
