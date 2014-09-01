# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import render_to_string
from cosinnus.utils.permissions import get_tagged_object_filter_for_user
from django.shortcuts import render


class BaseRenderer(object):
    
    model = None
    
    @classmethod
    def get_model(cls):
        if not hasattr(cls, 'model'):
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured('Missing model definition for '
                'renderer %s' % cls.__name__)
        return cls.model
    
    @classmethod
    def get_template(cls):
        if not hasattr(cls, 'template'):
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured('Missing template definition for '
                'renderer %s' % cls.__name__)
        return cls.template
    
    @classmethod
    def get_template_single(cls):
        if not hasattr(cls, 'template_single'):
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured('Missing template_single definition for '
                'renderer %s' % cls.__name__)
        return cls.template_single
    
    @classmethod
    def get_template_list(cls):
        if not hasattr(cls, 'template_list'):
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured('Missing template_single definition for '
                'renderer %s' % cls.__name__)
        return cls.template_list

    
    @classmethod
    def render(cls, context, objects=[], **kwargs):
        context.update(kwargs)
        context.update({'objects': objects})
        return render_to_string(cls.get_template(), context)
    
    @classmethod
    def render_single(cls, context, object=None, **kwargs):
        context.update(kwargs)
        context.update({'object': object})
        return render_to_string(cls.get_template_single(), context)

    @classmethod
    def render_list_for_user(cls, user, request, qs_filter={}, limit=30, **kwargs):
        """ Will render a standalone list of items of the renderer's model for
            a user and a request (important if there are forms in the template).
            This function will filter for access permissions for all of the items,
            but any further filtering (group, organization, etc) will have to be
            passed via the qs_filter dict.
        """
        user_filter = get_tagged_object_filter_for_user(user)
        qs = cls.get_model()._default_manager.filter(user_filter, **qs_filter)
        if limit > 0:
            qs = qs[:limit]
        
        context = {}
        context.update(kwargs)
        context.update({'object_list': qs})
        return render(request, cls.get_template_list(), context).content

"""
An example renderer for a specific app could be::

    from cosinnus.utils.renderer import BaseRenderer

    class MyRenderer(BaseRenderer):

        template = "path/to/template.html"

        @classmethod
        def render(cls, context, myobjs):
            return super(MyRenderer, cls).render(context, myobjs=myobjs)
"""
