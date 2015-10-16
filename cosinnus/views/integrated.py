# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import logging
logger = logging.getLogger('cosinnus')

from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from cosinnus.core.decorators.views import staff_required, superuser_required,\
    redirect_to_not_logged_in, redirect_to_403
from cosinnus.forms.user import UserCreationForm, UserChangeForm
from cosinnus.views.mixins.ajax import patch_body_json_data
from cosinnus.utils.http import JSONResponse
from django.contrib import messages
from cosinnus.models.profile import get_user_profile_model
from cosinnus.models.tagged import BaseTagObject
from cosinnus.models.group import CosinnusPortal
from cosinnus.core.mail import MailThread, get_common_mail_context,\
    send_mail_or_fail_threaded
from django.template.loader import render_to_string
from django.http.response import HttpResponseNotAllowed, Http404,\
    HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

USER_MODEL = get_user_model()

IntegratedHasher = PBKDF2PasswordHasher()
salt = 'cos01'

CREATE_INTEGRATED_USER_SESSION_CACHE_KEY = 'cosinnus/integrated/created_session_keys/%s'


def _get_integrated_user_validated(username, password):
    """ Does a 'login' for an integrated user based on a username and a double hashed passowrd """
    try:
        user = USER_MODEL.objects.get(username=username, is_active=True)
        # pseudo password check, removed for now
        #if _get_user_pseudo_password(user) == request.POST.get('password'):
        #if user.password == request.POST.get('password'): #md5 check, no pseudo check
        if IntegratedHasher.verify(user.password, password):
            user.backend = 'cosinnus.backends.IntegratedPortalAuthBackend'
        else:
            user = None
    except USER_MODEL.DoesNotExist:
        user=None
    return user


@sensitive_post_parameters()
@csrf_exempt
@never_cache
def login_integrated(request, authentication_form=AuthenticationForm):
    """
        Logs the user in with a CSRF exemption! This is used for integrated portal mode,
        when we allow subdomain-cross-site requests!
    """
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            return HttpResponseBadRequest('Missing POST parameters!')
        
        user = _get_integrated_user_validated(username, password)
        
        if user:
            auth_login(request, user)
            return redirect(request.POST.get('next', '/'))
        else:
            return HttpResponseNotAllowed('POST', content='Sorry, we could not connect your user account! Please contact an administrator!')
    else:
        raise Http404


@csrf_exempt
def logout_integrated(request):
    """
    Logs an integrated user out by setting a force-logout flag on him.
    """
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            return HttpResponseBadRequest('Missing POST parameters!')
        
        user = _get_integrated_user_validated(username, password)
        request.user = user
        
        # set the user to be logged out on next request
        user.cosinnus_profile.settings['force_logout_next_request'] = True
        user.cosinnus_profile.save()
        
        return JSONResponse({})
        
    else:
        raise Http404
    


@csrf_exempt
@never_cache
def create_user_integrated(request):
    if request.method == "POST":
        # spam protection
        # TODO: FIXME: not working right now, because of different session keys for each ajax cross-site POST :/
        session_key = request.session._get_or_create_session_key()
        if cache.get(CREATE_INTEGRATED_USER_SESSION_CACHE_KEY % session_key):
            return HttpResponseBadRequest('You have been doing this too often. Slow down!')
        
        user_email = request.POST.get('user_email', None)
        # this is actually the hashed password of the remote user
        user_password = request.POST.get('user_password', None)
        if not user_email or not user_password:
            return HttpResponseBadRequest('Missing POST parameters!')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # handshake on the integrating server, url from settings, NEVER FROM REQUEST!
        handshake_url = getattr(settings, 'COSINNUS_INTEGRATED_PORTAL_HANDSHAKE_URL', None)
        if not handshake_url:
            raise ImproperlyConfigured('Cannot create integrated user: COSINNUS_INTEGRATED_PORTAL_HANDSHAKE_URL is not configured in settings!')
        
        data = {
            'user_email': user_email,
        }
        req = requests.post(handshake_url, data=data)
        if not req.status_code == 200:
            logger.error('Failed to send handshake! Have you configured the correct COSINNUS_INTEGRATED_PORTAL_HANDSHAKE_URL?',
                         extra={'returned_request': req, 'handshake_url': handshake_url})
            return HttpResponseBadRequest('Could not create integrated user: Handshake could not be established! Code: %d' % req.status_code)
        response = req.json()
        if not response['status'] == 'ok':
            return HttpResponseBadRequest('Could not create integrated user: Handshake failed!')
        
        # handshake succeeded, either create new user or connect to existing one
        
        try:
            user = USER_MODEL.objects.get(email=user_email)
            # user already exists for this email
            # since we trust both servers, we connect the existing user account
        except USER_MODEL.DoesNotExist:
            user = None
        
        # create new user if not existed
        if user is None:
            password = 'will_be_replaced'
            data = {
                'username': user_email,
                'email': user_email,
                'password1': password,
                'password2': password,
                'first_name': first_name,
                'last_name': last_name,
            }
            # use Cosinnus' UserCreationForm to apply all usual user-creation-related effects
            form = UserCreationForm(data)
            if form.is_valid():
                user = form.save()
            else:
                return JSONResponse(data={'status': 'fail', 'reason': force_text(form.errors)})
            get_user_profile_model()._default_manager.get_for_user(user)
            
            # set the new user's password's hash to that of the connected user.
            user.password = user_password
            user.save()
        
        # retransmit a hashed version of the hashed password.
        # yes, we double hash the original password. because then the first password hash 
        # is only exposed once, during user creation, and never again after that.
        # all that is exposed to the client afterwards is a double hash, making this a bit cleaner.
        remote_password = IntegratedHasher.encode(user.password, salt)
        
        # set session key into cache
        cache.set(CREATE_INTEGRATED_USER_SESSION_CACHE_KEY % session_key, 'True', settings.COSINNUS_INTEGRATED_CREATE_USER_CACHE_TIMEOUT)
        
        return JSONResponse(data={'status': 'ok', 'remote_username': user.username, 'remote_password': remote_password})
        
    else:
        raise Http404



