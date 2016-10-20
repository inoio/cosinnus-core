# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader, Context

from haystack import indexes
from haystack.exceptions import SearchFieldError

from cosinnus.utils.import_utils import import_from_settings
from cosinnus.models.group import CosinnusGroup


def prepare_user(obj):
    if obj is None:
        return ''
    return obj.get_full_name() or obj.username


def prepare_users(users):
    if not users:
        return []
    return map(prepare_user, users)


class DefaultTagObjectIndex(indexes.SearchIndex):
    mt_location_place = indexes.CharField(model_attr='media_tag__location_place', null=True)
    mt_people_name = indexes.CharField(model_attr='media_tag__people_name', null=True)
    mt_public = indexes.BooleanField(model_attr='media_tag__public', null=True)


class TagObjectIndex(indexes.SearchIndex):
    mt_location = indexes.CharField(model_attr='media_tag__location', null=True)
    mt_location_lat = indexes.FloatField(model_attr='media_tag__location_lat', null=True)
    mt_location_lon = indexes.FloatField(model_attr='media_tag__location_lon', null=True)
    mt_place = indexes.CharField(model_attr='media_tag__place', null=True)
    mt_valid_start = indexes.DateTimeField(model_attr='media_tag__valid_start', null=True)
    mt_valid_end = indexes.DateTimeField(model_attr='media_tag__valid_end', null=True)
    mt_approach = indexes.CharField(model_attr='media_tag__approach', null=True)
    mt_topics = indexes.MultiValueField(model_attr='media_tag__topics', null=True)
    mt_persons = indexes.MultiValueField(null=True)
    mt_likes = indexes.IntegerField(model_attr='media_tag__likes', null=True)
    mt_visibility = indexes.IntegerField(model_attr='media_tag__visibility', null=True)

    def prepare_mt_persons(self, obj):
        if obj.media_tag:
            return prepare_users(obj.media_tag.persons.all())


def get_tag_object_index():
    """
    Return the cosinnus tag object search index that is defined in
    :data:`settings.COSINNUS_TAG_OBJECT_SEARCH_INDEX`
    """
    from django.core.exceptions import ImproperlyConfigured
    from cosinnus.conf import settings
    
    # if the setting points at the TagObjectIndex defined here, link it directly,
    # otherwise we will get circular import problems
    if getattr(settings, 'COSINNUS_TAG_OBJECT_SEARCH_INDEX', None) == '%s.TagObjectIndex' % __name__:
        index_class = TagObjectIndex
    else:
        index_class = import_from_settings('COSINNUS_TAG_OBJECT_SEARCH_INDEX')
    
    
    if not issubclass(index_class, indexes.SearchIndex):
        raise ImproperlyConfigured("COSINNUS_TAG_OBJECT_SEARCH_INDEX refers to "
                                   "index '%s' that does not exist or is not a "
                                   "valid haystack SearchIndex." %
            settings.COSINNUS_TAG_OBJECT_SEARCH_INDEX)
    return index_class


TagObjectSearchIndex = get_tag_object_index()


class TemplateResolveMixin(object):

    def prepare_template(self, obj):
        """
        Does the same as :func:`haystack.fields.CharField.prepare_template`,
        except it replaces all occurrences of ``{app_label}``, ``{model_name}``
        and ``{field_name}`` with the respective values on the given path(s).
        """
        if self.instance_name is None and self.template_name is None:
            raise SearchFieldError("This field requires either its "
                                   "instance_name variable to be populated or "
                                   "an explicit template_name in order to "
                                   "load the correct template.")

        if self.template_name is not None:
            template_names = self.template_name
            if not isinstance(template_names, (list, tuple)):
                template_names = [template_names]
        else:
            template_names = ['search/indexes/{app_label}/{model_name}_{field_name}.txt']

        resolve_data = {
            'app_label': obj._meta.app_label,
            'model_name': obj._meta.model_name,
            'field_name': self.instance_name,
        }
        resolved_template_names = [tn.format(**resolve_data) for tn in template_names]
        t = loader.select_template(resolved_template_names)
        return t.render(Context({'object': obj}))



class TemplateResolveCharField(TemplateResolveMixin, indexes.CharField):
    pass

class TemplateResolveEdgeNgramField(TemplateResolveMixin, indexes.EdgeNgramField):
    pass


class BaseTaggableObjectIndex(TagObjectSearchIndex):
    text = TemplateResolveEdgeNgramField(document=True, use_template=True)
    rendered = TemplateResolveCharField(use_template=True, indexed=False)
    
    title = indexes.EdgeNgramField(model_attr='title', boost=1.25)
    slug = indexes.CharField(model_attr='slug', indexed=False)
    creator = indexes.EdgeNgramField(model_attr='creator', null=True)
    created = indexes.DateTimeField(model_attr='created')

    get_absolute_url = indexes.CharField(model_attr='get_absolute_url', indexed=False)

    group = indexes.IntegerField(model_attr='group_id', indexed=False)
    group_name = indexes.CharField(model_attr='group__name')
    group_slug = indexes.CharField(model_attr='group__slug', indexed=False)
    group_public = indexes.BooleanField(model_attr='group__public')
    group_members = indexes.MultiValueField(model_attr='group__members')

    def index_queryset(self, using=None):
        model_cls = self.get_model()
        app_name = model_cls.__module__.split('.')[0] # eg 'cosinnus_etherpad'
        excluded_groups_for_app = [group.id for group in CosinnusGroup.objects.with_deactivated_app(app_name)]
        # TODO: check if this works properly
        qs = model_cls.objects.exclude(group__id__in=excluded_groups_for_app)
        # don't index inactive group's items
        qs = qs.filter(group__is_active=True)
        return qs.select_related('media_tag').all()

    def prepare_creator(self, obj):
        return prepare_user(obj.creator)
    
    
class BaseHierarchicalTaggableObjectIndex(BaseTaggableObjectIndex):
    
    def index_queryset(self, using=None):
        qs = super(BaseHierarchicalTaggableObjectIndex, self).index_queryset(using=using)
        return qs.filter(is_container=False)
