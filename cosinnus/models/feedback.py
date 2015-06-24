# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from cosinnus.conf import settings
from django.core.urlresolvers import reverse
from cosinnus.core.registries.group_models import group_model_registry
from cosinnus.models.group import CosinnusPortal
from cosinnus.utils.urls import get_domain_for_portal


@python_2_unicode_compatible
class CosinnusReportedObject(models.Model):
    """
    A complaint report pointing to a generic object.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    target_object = generic.GenericForeignKey('content_type', 'object_id')
    
    text = models.TextField(_('Complaint Text'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_('Creator'),
        on_delete=models.CASCADE,
        null=True,
        related_name='%(app_label)s_%(class)s_set')
    created = models.DateTimeField(
        verbose_name=_('Created'),
        editable=False,
        default=now,
        auto_now_add=True)
    

    class Meta:
        app_label = 'cosinnus'
        ordering = ('content_type',)
        verbose_name = _('Reported object')
        verbose_name_plural = _('Reported objects')

    def __str__(self):
        return '<Report: %s::%s>' % (self.content_type, self.object_id)

    @property
    def model_name(self):
        """
        The model name of the reported object, e.g.:  `'cosinnus_file.FileEntry'`
        """
        if not hasattr(self, '_model_name'):
            ct = self.content_type
            self._model_name = '%s.%s' % (ct.app_label, ct.model_class().__name__)
        return self._model_name
    
    
    def get_absolute_url(self):
        """ Point at URL of referenced ContentType object """
        if self.content_type.model == 'user':
            # patch for user model get_absolute_url pointing to nowhere
            return get_domain_for_portal(CosinnusPortal.get_current()) + reverse('cosinnus:profile-detail', kwargs={'username': self.target_object.username})
        if self.target_object and hasattr(self.target_object, 'get_absolute_url'):
            return self.target_object.get_absolute_url()
        return None
    
    def get_target_model_name(self):
        """ This will return the correct specific cosinnus group model (instead of base group) if we are targeting a group """
        if self.content_type.model == 'cosinnusgroup':
            group_cls = group_model_registry.get_by_type(self.target_object.type)
            return group_cls.__name__.lower() # lower()?
        else:
            return self.content_type.model
    
    def get_target_edit_url(self):
        return reverse('admin:%s_%s_change' % (self.content_type.app_label, self.get_target_model_name()), args=(self.target_object.id,))
    
    def get_target_delete_url(self):
        return reverse('admin:%s_%s_delete' % (self.content_type.app_label, self.get_target_model_name()), args=(self.target_object.id,))
    
