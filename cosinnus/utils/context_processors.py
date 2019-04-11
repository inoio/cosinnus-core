# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse, resolve, Resolver404
from django.utils.formats import get_format
from django.utils.translation import get_language

from cosinnus.conf import settings as SETTINGS
from cosinnus.core.registries import app_registry
from cosinnus.models.serializers.profile import UserSimpleSerializer
from postman.models import Message
import json
from cosinnus.core.registries.group_models import group_model_registry
from cosinnus.models.group import CosinnusPortal
from cosinnus.forms.user import TermsOfServiceFormFields
from dateutil import parser

import logging
logger = logging.getLogger('cosinnus')


def settings(request):
    return {
        'SETTINGS': SETTINGS,
    }


def cosinnus(request):
    """
    Exposes a set of global variables to the template rendering context:

    ``COSINNUS_BASE_URL``
        The index URL where cosinnus is being registered.

    ``COSINNUS_CURRENT_APP``
        If the current request points to a cosinnus (app) view, the name the
        app has been registered with (e.g. ``"todo"`` for "cosinnus_todo"). If
        not it is an empty string ``''``.

    ``COSINNUS_DATE_FORMAT``

    ``COSINNUS_DATETIME_FORMAT``
    
    ``COSINNUS_TIME_FORMAT``
    
    ``COSINNUS_DJANGO_DATETIME_FORMAT``
    
    ``COSINNUS_DJANGO_DATE_FORMAT``
    
    ``COSINNUS_DJANGO_DATE_SHORT_FORMAT``
    
    ``COSINNUS_COSINNUS_DJANGO_DATE_SHORT_CLEAR_FORMAT``
    
    ``COSINNUS_DJANGO_TIME_FORMAT``
    
    ``COSINNUS_USER``
        If ``request.user`` is logged in, its a serialized version of
        :class:`~cosinnus.models.serializers.profile.UserSimpleSerializer`. If
        not authenticated it is ``False``. Both serialized to JSON.
    """
    base_url = CosinnusPortal.get_current().get_domain() 
    base_url += '' if base_url[-1] == '/' else '/'

    user = request.user
    if user.is_authenticated:
        user_json = json.dumps(UserSimpleSerializer(user).data)
        unread_count = Message.objects.inbox_unread_count(user)
        from cosinnus_stream.models import Stream
        stream_unseen_count = Stream.objects.my_stream_unread_count(user)
    else:
        user_json = json.dumps(False)
        unread_count = 0
        stream_unseen_count = 0

    current_app_name = ''
    try:
        current_app = resolve(request.path.strip()).app_name.replace(':', '_')
        current_app_name = app_registry.get_name(current_app)
    except KeyError:
        pass  # current_app is not a cosinnus app
    except Resolver404:
        pass
    
    return {
        'COSINNUS_BASE_URL': base_url,
        'COSINNUS_CURRENT_APP': current_app_name,
        'COSINNUS_DATE_FORMAT': get_format('COSINNUS_DATETIMEPICKER_DATE_FORMAT'),
        'COSINNUS_DATETIME_FORMAT': get_format('COSINNUS_DATETIMEPICKER_DATETIME_FORMAT'),
        'COSINNUS_TIME_FORMAT': get_format('COSINNUS_DATETIMEPICKER_TIME_FORMAT'),
        'COSINNUS_DJANGO_DATETIME_FORMAT': get_format('COSINNUS_DJANGO_DATETIME_FORMAT'),
        'COSINNUS_DJANGO_DATE_FORMAT': get_format('COSINNUS_DJANGO_DATE_FORMAT'),
        'COSINNUS_DJANGO_DATE_SHORT_FORMAT': get_format('COSINNUS_DJANGO_DATE_SHORT_FORMAT'),
        'COSINNUS_DJANGO_DATE_SHORT_CLEAR_FORMAT': get_format('COSINNUS_DJANGO_DATE_SHORT_CLEAR_FORMAT'),
        'COSINNUS_DJANGO_TIME_FORMAT': get_format('COSINNUS_DJANGO_TIME_FORMAT'),
        'COSINNUS_USER': user_json,
        'COSINNUS_UNREAD_MESSAGE_COUNT': unread_count,
        'COSINNUS_STREAM_UNSEEN_COUNT': stream_unseen_count,
        'COSINNUS_CURRENT_LANGUAGE': get_language(),
        'COSINNUS_CURRENT_PORTAL': CosinnusPortal.get_current(),
    }


def tos_check(request):
    """ Checks if the portal's ToS version is higher than those that the user
        has accepted, and if so, renders the `updated_tos_form` into the context.
        Currently, `extra_body_header.html` (from `base.html`) checks if the form
        is present and renders a modal popup with it. """
        
    portal = CosinnusPortal.get_current()
    user = request.user
    if user.is_authenticated:
        try:
            tos_accepted_date = user.cosinnus_profile.settings.get('tos_accepted_date', None)
            # if a portal's tos_date has never moved beyond the default, we don't check the tos_accepted_date, 
            # to maintain backwards compatibility with users who have only the `settings.tos_accepted` boolean
            if portal.tos_date.year > 2000 and (tos_accepted_date is None or parser.parse(tos_accepted_date) < portal.tos_date):
                updated_tos_form = TermsOfServiceFormFields(initial={
                    'newsletter_opt_in': user.cosinnus_profile.settings.get('newsletter_opt_in', False)
                })
                return {
                    'updated_tos_form': updated_tos_form, 
                }
        except Exception as e:
            logger.error('Error in `context_processory.tos_check`: %s' % e, extra={'exception': e})
    
    return {}
