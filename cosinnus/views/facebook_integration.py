# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseNotAllowed, \
    HttpResponseForbidden, HttpResponseBadRequest, JsonResponse,\
    HttpResponseServerError

import json
import urllib2
import logging
from datetime import datetime, timedelta
import time

from cosinnus.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
import urlparse
import requests
import urllib
from cosinnus.utils.urls import iriToUri
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django import forms

logger = logging.getLogger('cosinnus')

def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

    
def datetime_in_seconds(datetime):
    """ Returns a datetime in (local) time since 1900 GMT """
    return time.mktime(datetime.timetuple())


class FacebookIntegrationUserProfileMixin(object):
    
    def get_facebook_user_id(self):
        """ Returns a user's connected facebook user-id ONLY if their access token is still valid.
            (Otherwise, they have to go through the login loop again anyways). """
        user_id = self.settings.get('fb_userID', None)
        expiry = self.settings.get('fb_expiresAfterUTCSeconds', None)
        if user_id and expiry:
            # check if fb_expiresAfterUTCSeconds is plus one hour is still below the expiry time
            expiry = float(expiry)
            now_in_seconds = float(datetime_in_seconds(datetime.now()))
            if (now_in_seconds + 60*60) < expiry:
                return user_id
        return None
    
    def get_facebook_username(self):
        if self.get_facebook_user_id():
            return self.settings.get('fb_username', None)
        return ''
    
    def get_facebook_avatar_url(self):
        user_id = self.get_facebook_user_id()
        if user_id:
            return 'https://graph.facebook.com/%s/picture?type=square' % user_id
        return ''
    
    def delete_facebook_association(self):
        """ Removes all facebook token/user info from this profile and saves it. """
        if 'fb_userID' in self.settings:
            del self.settings['fb_userID']
        if 'fb_accessToken' in self.settings:
            del self.settings['fb_accessToken']
        if 'fb_expiresAfterUTCSeconds' in self.settings:
            del self.settings['fb_expiresAfterUTCSeconds']
        if 'fb_username' in self.settings:
            del self.settings['fb_username']
        self.save()
    
class FacebookIntegrationViewMixin(object):

    def post_to_facebook(self, userprofile, fb_post_text, urls=[], fb_post_target_id=None):
        """ Posts content to the timeline of a given userprofile's user synchronously.
            This method will never throw an exception.
            @param userprofile: a userprofile model instance that contains the user's fb info
            @param fb_post_text: Body text of the Facebook post
            @param urls: Any URLs contained in the post that shall be attached to the post explicitly (for a preview box, etc)
            @param fb_post_target_id: If None, post to the user's timeline. If given, post to this alternate id of the facebook graph API egdes:
                /{user-id}/feed, /{page-id}/feed, /{event-id}/feed, or /{group-id}/feed (No need to specify which one; they are unique)
            @return: a string if posted successfully (either the post's id or '' if unknown), None if the post failed for any reason
            """
        try:
            # get user id and check for valid token
            user_id = userprofile.get_facebook_user_id()
            if not user_id:
                logger.warning('Could not post to facebook timeline even though it was requested because of missing fb_userID!', extra={
                           'user-email': userprofile.user.email, 'alternate-post-target': fb_post_target_id})
                return None
            access_token = userprofile.settings['fb_accessToken']
            if not access_token:
                logger.warning('Could not post to facebook timeline even though it was requested because of missing fb_accessToken!', extra={
                           'user-email': userprofile.user.email, 'user_fbID': user_id, 'alternate-post-target': fb_post_target_id})
                return None
            
            post_target = fb_post_target_id or user_id
            post_url = 'https://graph.facebook.com/v2.5/%(post_target)s/feed' % ({'post_target': post_target})
            data = {
                'message': fb_post_text.encode('utf-8'),
                'access_token': access_token,
            }
            if urls:
                data.update({
                    'link': urls[0],
                })
                
            post_url = post_url + '?' + urllib.urlencode(data)
            post_url = iriToUri(post_url)
            
            req = requests.post(post_url, data=data, verify=False)
            if not req.status_code == 200:
                logger.warn('Facebook posting to timeline failed, request did not return status=200.', extra={'status':req.status_code, 'content': req._content})
                return None
            
            response = req.json()
            return response.get('id', '')
            
        except Exception, e:
            logger.warning('Unexpected exception when posting to facebook timeline!', extra={
                           'user-email': userprofile.user.email, 'user_fbID': user_id, 'exception': force_text(e), 'alternate-post-target': fb_post_target_id})
        return None

    
class FacebookIntegrationGroupFormMixin(object):
    
    facebook_group_id_field = 'facebook_group_id'
    facebook_page_id_field = 'facebook_page_id'
    
    def clean(self):
        cleaned_data = super(FacebookIntegrationGroupFormMixin, self).clean()
        if not getattr(settings, 'COSINNUS_FACEBOOK_INTEGRATION_ENABLED', False):
            return cleaned_data
        if not self.facebook_group_id_field:
            raise ImproperlyConfigured('The ``facebook_group_id_field`` attribute was not supplied!')
        if not self.facebook_page_id_field:
            raise ImproperlyConfigured('The ``facebook_page_id_field`` attribute was not supplied!')
        
        facebook_group_id = cleaned_data.get(self.facebook_group_id_field)
        facebook_page_id = cleaned_data.get(self.facebook_page_id_field)
        
        if facebook_group_id and facebook_page_id:
            raise forms.ValidationError(_('You can only connect to either a Facebook Group or a Fan-Page, but not both!'))
        
        facebook_id = None
        
        if facebook_group_id and facebook_group_id != getattr(self.instance, self.facebook_group_id_field):
            if not _is_number(facebook_group_id):
                raise forms.ValidationError(_('Please enter a numeric Facebook Group-ID only!'))
            facebook_id = facebook_group_id
        elif facebook_page_id and facebook_page_id != getattr(self.instance, self.facebook_page_id_field):
            if _is_number(facebook_page_id):
                raise forms.ValidationError(_('Please enter a string Fan-Page unique name only (example: myfanpage)!'))
            facebook_id = facebook_page_id
        
        if facebook_id:
            if not getattr(self, 'request', None):
                raise ImproperlyConfigured('FacebookIntegrationGroupFormMixin needs a request to be set! Provide your form with one by overriding its __init__ function and passing a request as form kwarg!')
            # check if user has connected to facebook, we need the access token
            if not self.request.user.cosinnus_profile.get_facebook_user_id():
                raise ImproperlyConfigured('You need to be connected to Facebook to link a Group or Fan-Page!')
            
            # get group info
            access_token = self.request.user.cosinnus_profile.settings['fb_accessToken']
            had_error = False
            try:
                location_url = "https://graph.facebook.com/%(group_id)s?access_token=%(access_token)s" \
                       % {
                          'group_id': facebook_id,
                          'access_token': access_token,
                       }
                response_info = urllib2.urlopen(location_url)
            except Exception, e:
                logger.warn('Error when trying to retrieve FB group info from Facebook:', extra={'exception': force_text(e), 'url': location_url})
                had_error = True
            if not had_error and not response_info.code == 200:
                logger.warn('Error when trying to retrieve FB group info from Facebook (non-200 response):', extra={'response_info': force_text(response_info.__dict__)})
                had_error = True
            if not had_error:
                content_info = json.loads(response_info.read()) # this graph returns a JSON string, not a query response
                if not 'name' in content_info:
                    had_error = True
            
            #  if group could not be accessed in any way throw validation eorr
            if had_error:
                raise forms.ValidationError(_('The Facebook Fan-Page ID or Group ID could not be found on Facebook! Make sure you have entered the correct ID for your Group/Fan-Page!'))
            
            # for Facebook Fan-Pages, we immediately try to get an access token to the fan-page, and deny connecting it
            # if we cannot obtain it (user may not be an admin of the group)
            if facebook_page_id:
                obtain_token_result = obtain_facebook_page_access_token_for_user(request=None, group=self.instance, page_id=facebook_page_id, user=self.request.user)
                if not obtain_token_result:
                    raise forms.ValidationError(_('We could not obtain access to the Fan-Page for your connected Facebook Account. Please check that you entered the correct Fan-Page name, and that you are an admin of that Fan-Page!'))
                
                
def obtain_facebook_page_access_token_for_user(request=None, group=None, page_id=None, user=None):
    """ Tries to obtain a Facebook-Page access token for a user and for a group, and its connected page-id.
        Then saves this page-access token in the userprofile.settings as {'fb_page_%(group_id)d_%(page_id)s': <access-token>} 
        @return: True if the fan-page access token was obtained and saved in the user profile.
                 False if anything went wrong.
        """
        
    if request is not None:
        # TODO: obtain the variables from the request
        group = None
        page_id = None
        user = request.user
    
    if not group or not page_id or not user:
        print ">> returning from obtain token early"
        return False
    
    # using a facebook fan-page access token, using the user access token of an admin of that page (see https://developers.facebook.com/docs/pages/getting-started)
    access_token = user.cosinnus_profile.settings['fb_accessToken']
    had_error = False
    try:
        location_url = "https://graph.facebook.com/%(page_id)s?fields=access_token&access_token=%(access_token)s" \
            % {
               'page_id': page_id,
               'access_token': access_token,
            }
        response_info = urllib2.urlopen(location_url)
    except Exception, e:
        logger.warn('Error when trying to retrieve FB page access-token from Facebook:', extra={'exception': force_text(e), 'url': location_url})
        had_error = True
    if not had_error and not response_info.code == 200:
        logger.warn('Error when trying to retrieve FB page access-token from Facebook (non-200 response):', extra={'response_info': force_text(response_info.__dict__)})
        had_error = True
    if not had_error:
        token_info = json.loads(response_info.read()) # this graph returns a JSON string, not a query response
        if not 'access_token' in token_info:
            had_error = True
            
    if had_error:
        return False
    page_settings_key = 'fb_page_%(group_id)d_%(page_id)s' % {'group_id': group.id, 'page_id': page_id}
    
    user.cosinnus_profile.settings[page_settings_key] = token_info['access_token']
    user.cosinnus_profile.save()
    
    return True


def save_auth_tokens(request):
    """ Saves the given facebook auth tokens for the current user """
    
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated():
        return HttpResponseForbidden('Must be logged in!')
    if not 'authResponse' in request.POST:
        return HttpResponseBadRequest('authResponse data missing!')
    if not settings.COSINNUS_FACEBOOK_INTEGRATION_APP_ID:
        raise ImproperlyConfigured('Missing setting COSINNUS_FACEBOOK_INTEGRATION_APP_ID for facebook integration!')
    if not settings.COSINNUS_FACEBOOK_INTEGRATION_APP_SECRET:
        raise ImproperlyConfigured('Missing setting COSINNUS_FACEBOOK_INTEGRATION_APP_SECRET for facebook integration!')
    
    authResponse = json.loads(request.POST.get('authResponse'))
    user_id = authResponse['userID']
    
    try:
        # The client only gets a short ~2hr access token. We will now exchange that for a long-lived  ~60day token.
        location_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%(app-id)s&client_secret=%(app-secret)s&fb_exchange_token=%(short-lived-token)s" \
               % {
                  'app-id': settings.COSINNUS_FACEBOOK_INTEGRATION_APP_ID,
                  'app-secret': settings.COSINNUS_FACEBOOK_INTEGRATION_APP_SECRET,
                  'short-lived-token':authResponse['accessToken'],
               }
        response = urllib2.urlopen(location_url)
    except Exception, e:
        logger.error('Error when trying to retrieve long-lived-access-token from Facebook:', extra={'exception': force_text(e), 'url': location_url})
        return HttpResponseServerError('Facebook request could not be completed (1).')
    
    if not response.code == 200:
        logger.error('Error when trying to retrieve long-lived-access-token from Facebook (non-200 response):', extra={'response': force_text(response.__dict__)})
        return HttpResponseServerError('Facebook request could not be completed (2).')
    
    # for some reason, the oauth graph node returns a QSL string, and not JSON
    content_auth = dict(urlparse.parse_qsl(response.read()))
    # content should contain 'access_token' (string) and 'expires' (string, in seconds)
    if not 'access_token' in content_auth or not 'expires' in content_auth or not _is_number(content_auth['expires']):
        logger.error('Error when trying to retrieve long-lived-access-token from Facebook (missing data):', extra={'content_auth': content_auth})
        return HttpResponseServerError('Facebook request could not be completed (3).')
    
    access_token = content_auth['access_token']
    
    # get username!
    fb_username = None
    try:
        location_url = "https://graph.facebook.com/%(user_id)s?access_token=%(access_token)s" \
               % {
                  'user_id': user_id,
                  'access_token': access_token,
               }
        response_info = urllib2.urlopen(location_url)
    except Exception, e:
        logger.warn('Error when trying to retrieve user info from Facebook:', extra={'exception': force_text(e), 'url': location_url})
        fb_username = 'error'
        
    if not fb_username and not response_info.code == 200:
        logger.warn('Error when trying to retrieveuser info from Facebook (non-200 response):', extra={'response_info': force_text(response_info.__dict__)})
        fb_username = 'error'
        
    if not fb_username:
        content_info = json.loads(response_info.read()) # this graph returns a JSON string, not a query response
        if 'name' in content_info:
            fb_username = content_info.get('name')
    else:
        fb_username = None
    
    # save long lived token to userprofile
    profile = request.user.cosinnus_profile
    profile.settings['fb_userID'] = user_id
    profile.settings['fb_accessToken'] = access_token
    profile.settings['fb_username'] = fb_username
    # we save the time-point in UTC seconds after which this token must be renewed    
    then = datetime.now() + timedelta(seconds=int(content_auth['expires']))
    profile.settings['fb_expiresAfterUTCSeconds'] = datetime_in_seconds(then)
    profile.save()
    
    return JsonResponse({'status': 'ok', 'username': fb_username, 'user_id': user_id, 'avatar': profile.get_facebook_avatar_url()})


def remove_facebook_association(request):
    """ Saves the given facebook auth tokens for the current user """
    if not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated():
        return HttpResponseForbidden('Must be logged in!')
    
    userprofile = request.user.cosinnus_profile
    fb_user_id = userprofile.get_facebook_user_id()
    if fb_user_id:
        access_token = userprofile.settings['fb_accessToken']
        if not access_token:
            logger.error('Could not delete facebook associatione even though it was requested because of missing fb_accessToken!', extra={
                       'user-email': userprofile.user.email, 'user_fbID': fb_user_id})
            messages.error(request, _('An error occured when trying to disconnect your facebook account! Please contact an administrator!'))
            return redirect(reverse('cosinnus:profile-edit'))
        
        post_url = 'https://graph.facebook.com/v2.5/%(user_id)s/permissions' % ({'user_id': fb_user_id})
        data = {
            'access_token': access_token,
        }
        post_url = post_url + '?' + urllib.urlencode(data)
        post_url = iriToUri(post_url)
        
        req = requests.delete(post_url, data=data, verify=False)
        if not req.status_code == 200:
            logger.error('Facebook deleting association failed, request did not return status=200.', extra={'status':req.status_code, 'content': req._content})
            messages.error(request, _('An error occured when trying to disconnect your facebook account! Please contact an administrator!'))
            return redirect(reverse('cosinnus:profile-edit'))
        
        response = req.json()
        
        if response.get('success', False) == True:
            userprofile.delete_facebook_association()
            messages.success(request, _('Your Facebook account was successfully disconnected from this account.'))
        else:
            logger.error('Facebook deleting association failed, response did not return success=True.', extra={'response': response})
            messages.warning(request, _('An error occured when trying to disconnect your facebook account! Please contact an administrator!'))
    
    return redirect(reverse('cosinnus:profile-edit'))
        

