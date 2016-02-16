# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cosinnus.models.group import CosinnusGroup, CosinnusGroupMembership,\
    CosinnusPermanentRedirect, CosinnusPortal, MEMBERSHIP_MEMBER,\
    MEMBERSHIP_PENDING
from cosinnus.utils.dashboard import create_initial_group_widgets
from django.http.response import HttpResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.db.models import Q
from cosinnus.views.profile import delete_userprofile
from cosinnus.utils.group import move_group_content as move_group_content_utils
from cosinnus.models.widget import WidgetConfig
from django.core.cache import cache
from django.conf import settings
from cosinnus.conf import settings as cosinnus_settings
import json
import urllib2


def housekeeping(request):
    """ Do some integrity checks and corrections. 
        Currently doing:
            - Checking all groups and projects for missing widgets versus the default widget
                settings and adding missing widgets
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    groups = CosinnusGroup.objects.all()
    ret = ""
    for group in groups:
        ret += "Checked group %s\n<br/>" % group.slug
        create_initial_group_widgets(None, group)
    return HttpResponse(ret)


def delete_spam_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    ret = ''
    user_csv = ''
    deleted_user_count = 0
    
    spam_users = get_user_model().objects.filter(date_joined__gt='2014-09-10').filter(
        Q(email__contains='.pl') | Q(cosinnus_profile__website__contains='.pl') | Q(email__contains='makre')
    ).distinct()
    
    
    for user in spam_users:
        user_groups = CosinnusGroup.objects.get_for_user(user)
        if len(user_groups) > 1:
            ret += '> Not deleting a user because he is in %d groups <br/>' % len(user_groups)
            continue
        
        breakadmin = False
        for group in user_groups:
            admins = CosinnusGroupMembership.objects.get_admins(group=group)
            if user.pk in admins:
                ret += '> Not deleting a user because he is admin in group %s' % group.slug
                breakadmin = True
                break
        if breakadmin:
            continue
        
        user_csv += '%(id)s,%(email)s,%(first_name)s,%(last_name)s<br/>' % user.__dict__
        deleted_user_count += 1
        if request.GET.get('commit', False) == 'true':
            delete_userprofile(user)
    
    if not request.GET.get('commit', False) == 'true':
        ret = ' **********   THIS IS A FAKE DELETION ONLY! user param ?commit=true to really delete the users! ***********'
    
    ret += '<br/><br/><br/>Deleted %d Users<br/><br/>' % deleted_user_count + user_csv
    return HttpResponse(ret)


def move_group_content(request, fromgroup, togroup):
    """ access to function for moving group content from one group to another """
    if not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    fromgroup = CosinnusGroup.objects.get_cached(slugs=fromgroup)
    togroup = CosinnusGroup.objects.get_cached(slugs=togroup)
    
    logs = move_group_content_utils(fromgroup, togroup)
    return HttpResponse("<br/>".join(logs))
        
        
def recreate_all_group_widgets(request=None, verbose=False):
    """ Resets all CosinnusGroup Dashboard Widget Configurations to their default
        by deleting and recreating them. """
    if request and not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    # delete all widget configs
    WidgetConfig.objects.all().delete()
    
    # create all default widgets for all groups
    groups_ids = []
    all_groups = CosinnusGroup.objects.all()
    for group in all_groups:
        create_initial_group_widgets(None, group)
        groups_ids.append(str(group.id))
        if verbose:
            print ">>> recreated widget config for group id", group.id
    
    return HttpResponse("The following groups were updated:<br/><br/>" + "<br/>".join(groups_ids))


HOUSEKEEPING_CACHE_KEY = 'cosinnus/core/housekeeping/setcache_debug'

def setcache(request, content):
    """ access to function for moving group content from one group to another """
    if not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    content = force_text(content)
    cache.set(HOUSEKEEPING_CACHE_KEY, content)
    return HttpResponse("Set '%s' as debug cache entry." % content)
        
        
def getcache(request):
    """ access to function for moving group content from one group to another """
    if not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    content = cache.get(HOUSEKEEPING_CACHE_KEY)
    return HttpResponse("The debug cache entry contains: '%s'." % content)


def check_and_delete_loop_redirects(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    delete = bool(request.GET.get('delete', False))
    
    bad_redirects = [redirect for redirect in CosinnusPermanentRedirect.objects.all() if not redirect.check_integrity()]
    response_string = 'Bad redirects:<br>' +  \
            '<br>'.join([ \
                'portal: %d, from_slug: %s, from_type: %s' % (redirect.from_portal_id, redirect.from_slug, redirect.from_type) \
             for redirect in bad_redirects])
    if delete:
        for redirect in bad_redirects:
            redirect.delete()
    response_string += '<br><br>' + ('These redirects were deleted.' if delete else 'Delete them by using ?delete=1 as GET!')
    return HttpResponse(response_string)


def add_members_to_forum(request=None):
    if request and not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    str = 'Added these users:<br/><br/>\n'
    
    for portal in CosinnusPortal.objects.all():
        users = get_user_model().objects.filter(id__in=portal.members)
        for group_slug in getattr(settings, 'NEWW_DEFAULT_USER_GROUPS', []):
            try:
                group = CosinnusGroup.objects.get(slug=group_slug, portal_id=portal.id)
                for user in users:
                    memb, created = CosinnusGroupMembership.objects.get_or_create(user=user, group=group, defaults={'status': MEMBERSHIP_MEMBER})
                    if not created:
                        if memb.status == MEMBERSHIP_PENDING:
                            memb.status = MEMBERSHIP_MEMBER
                            memb.save()
                            str += 'Set user %d to not pending anymore in portal %d <br/>\n' % (user.id, portal.id)
                    else:
                        str += 'Added user %d to forum in portal %d<br/>\n' % (user.id, portal.id)
                            
            except CosinnusGroup.DoesNotExist:
                str += 'Could not find forum in portal %d <br/>\n' % portal.id
    
    return HttpResponse(str)

easter_european_country_codes = ['BY', 'BG', 'CZ', 'HU', 'MD', 'PL', 'RO', 'RU', 'SK', 'UA']

def user_statistics(request=None):
    if request and not request.user.is_superuser:
        return HttpResponseForbidden('Not authenticated')
    
    user_locs = get_user_model().objects.filter(cosinnus_profile__media_tag__location_lat__isnull=False)\
        .values_list('id', 'cosinnus_profile__media_tag__location_lat', 'cosinnus_profile__media_tag__location_lon')
    
    results = []
    
    class Found(Exception): pass
    for id, lat, lon in user_locs:
        location_url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f" % (lat, lon)
        location_data = json.load(urllib2.urlopen(location_url))
        try:
            for r in location_data['results']:
                for c in r['address_components']:
                    if 'country' in c['types']:
                        short_name = c['short_name']
                        if short_name in easter_european_country_codes:
                            results.append('%d,%f,%f,%s' % (id, lat, lon, short_name))
                            raise Found
        except Found:
            pass
    #group_locs = CosinnusGroup.objects.filter(locations__gt=0).values_list('id', 'media_tag__location_lat', 'media_tag__location_lon')
    
    #user_locs_str = [str(x) for x in results]
    #group_locs_str = [str(y) for y in group_locs]
    
    return HttpResponse('<br/>'.join(results))# + ' (group)<br/>'.join(group_locs_str))


def delete_portal(portal_slug):
    """ Completely deletes a portal object and all of its groups and all objects assigned to the groups.
        THen deletes (!) any users who are both no member of any group AND no member of any portal. """
    # do NOT delete etherpads on the server!
    settings.COSINNUS_DELETE_ETHERPADS_ON_SERVER_ON_DELETE = False
    CosinnusPortal.objects.get(slug=portal_slug).delete()
    get_user_model().objects.filter(cosinnus_memberships__isnull=True).filter(cosinnus_portal_memberships__isnull=True).delete()

