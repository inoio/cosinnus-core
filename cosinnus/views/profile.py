# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from cosinnus.forms.profile import UserProfileForm
from cosinnus.models.profile import get_user_profile_model
from cosinnus.views.mixins.avatar import AvatarFormMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponseRedirect
from cosinnus.models.tagged import BaseTagObject
from cosinnus.models.group import CosinnusGroup, CosinnusGroupMembership
from cosinnus.models.widget import WidgetConfig
from django.contrib.auth import logout


def delete_userprofile(user):
    """ Deactivate and anonymize a user's profile """
    
    profile = user.cosinnus_profile
    
    # delete user widgets
    widgets = WidgetConfig.objects.filter(user_id__exact=user.pk)
    for widget in widgets:
        widget.delete()
    
    # leave all groups
    for membership in CosinnusGroupMembership.objects.filter(user=user):
        membership.delete()
    
    # delete user media_tag
    if profile.media_tag:
        profile.media_tag.delete()
    
    # delete user profile
    if profile.avatar:
        profile.avatar.delete(False)
    profile.delete()
    
    # set user to inactive and anonymize all data
    user.first_name = "deleted"
    user.last_name = "user"
    user.username = user.id
    user.email = user.id
    user.is_active = False
    user.save()


class UserProfileObjectMixin(SingleObjectMixin):
    model = get_user_profile_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        """ Return the userprofile for the current logged in user if no kwarg slug is given,
            or the userprofile for the username slug given """
        
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        
        # return the current user's userprofile if no slug is given
        if not pk and not slug:
            return self.model._default_manager.get_for_user(self.request.user)
        
        if queryset is None:
            queryset = self.get_queryset()
        if pk is not None:
            queryset = queryset.filter(user__pk=pk)
        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{'user__' + slug_field: slug})
        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        
        return obj


class UserProfileDetailView(UserProfileObjectMixin, DetailView):
    template_name = 'cosinnus/user/userprofile_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileDetailView, self).dispatch(
            request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super(UserProfileDetailView, self).get_queryset()
        qs = qs.exclude(user__is_active=False)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        profile = context['object']
        context.update({
            'optional_fields': profile.get_optional_fields(),
            'profile': profile,
            'this_user': profile.user,
        })
        return context

detail_view = UserProfileDetailView.as_view()


class UserProfileUpdateView(AvatarFormMixin, UserProfileObjectMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'cosinnus/user/userprofile_form.html'
    message_success = _('Your profile was edited successfully.')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileObjectMixin, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('cosinnus:profile-detail')
    
    def form_valid(self, form):
        # security catch to disallow "nobody" privacy values of users
        if not self.object.media_tag.visibility in [BaseTagObject.VISIBILITY_ALL, BaseTagObject.VISIBILITY_GROUP]:
            self.object.media_tag.visibility = BaseTagObject.VISIBILITY_ALL
        
        ret = super(UserProfileUpdateView, self).form_valid(form)
        messages.success(self.request, self.message_success)
        return ret

update_view = UserProfileUpdateView.as_view()


class UserProfileDeleteView(AvatarFormMixin, UserProfileObjectMixin, UpdateView):
    #form_class = UserProfileForm
    template_name = 'cosinnus/user/userprofile_delete.html'
    message_success = _('Your profile was deleted successfully. We\'re sorry you are no longer with us.')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileDeleteView, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('login')
    
    def _validate_user_delete_safe(self, user):
        is_safe = user.is_authenticated()
        
        for group in CosinnusGroup.objects.get_for_user(user):
            admins = CosinnusGroupMembership.objects.get_admins(group=group)
            if user.pk in admins:
                messages.error(self.request, _('You are the only administrator left for group "%s". Please appoint a different administrator or delete the group first.' % group.name))
                is_safe = False
        
        return is_safe
    
    def get(self, request, *args, **kwargs):
        self._validate_user_delete_safe(self.request.user)
        return super(UserProfileDeleteView, self).post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self._validate_user_delete_safe(request.user):
            return HttpResponseRedirect(reverse('cosinnus:profile-delete'))
        delete_userprofile(request.user)
        
        # log user out
        logout(request)
        
        messages.success(self.request, self.message_success)
        return HttpResponseRedirect(self.get_success_url())
    

delete_view = UserProfileDeleteView.as_view()
