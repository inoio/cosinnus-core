# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django import forms

from wagtail.wagtailcore.fields import RichTextField, RichTextArea
from wagtail.wagtailcore.rich_text import DbWhitelister

from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks.field_block import RichTextBlock, RawHTMLBlock,\
    URLBlock
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks.struct_block import StructBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from cosinnus.models.group_extra import CosinnusProject
from random import shuffle

    

class BetterDbWhitelister(DbWhitelister):
    """ Prevents <div> tags from being replaced by <p> """
    
    @classmethod
    def clean_tag_node(cls, doc, tag):
        if not 'data-embedtype' in tag.attrs and tag.name == 'div':
            super(DbWhitelister, cls).clean_tag_node(doc, tag) # this gets around having the 'div' tag replaced
        else:
            super(BetterDbWhitelister, cls).clean_tag_node(doc, tag)
            

class BetterRichTextArea(RichTextArea):
    """ Enables using a custom DbWhitelister """
    
    def value_from_datadict(self, data, files, name):
        original_value = super(RichTextArea, self).value_from_datadict(data, files, name)
        if original_value is None:
            return None
        return BetterDbWhitelister.clean(original_value)


class BetterRichTextField(RichTextField):
    """ Enables using a custom DbWhitelister """
    
    def formfield(self, **kwargs):
        defaults = {'widget': BetterRichTextArea}
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults) # super on RichTextField, not self.__class__!


class BetterRichTextBlock(RichTextBlock):
    """ Enables using a custom DbWhitelister """
    
    @cached_property
    def field(self):
        return forms.CharField(widget=BetterRichTextArea, **self.field_options)

    
    
class CreateProjectButtonBlock(StructBlock):
    
    class Meta:
        label = _('Create-Project or Group Button')
        icon = 'group'
        template = 'cosinnus/wagtail/widgets/create_project_button.html'
        
    type = blocks.ChoiceBlock(choices=[
        ('project', 'Project'),
        ('group', 'Group'),
    ], required=True, label='Type', default='project')


    def get_context(self, value):
        context = super(CreateProjectButtonBlock, self).get_context(value)
        context['type'] = value.get('type')
        return context
    

class LinkBlock(StructBlock):
    url = blocks.URLBlock(label='URL')
    text = blocks.CharBlock()

    class Meta:
        icon = 'anchor'
        template = 'cosinnus/wagtail/widgets/link.html'

    def get_context(self, value):
        context = super(LinkBlock, self).get_context(value)
        context['href'] = value.get('url')
        context['text'] = value.get('text')
        context['class'] = value.get('cls')
        return context
    

""" Default configuration of available blocks for out StreamField, because DRY """
STREAMFIELD_BLOCKS_NOFRAMES = [
    ('paragraph', BetterRichTextBlock(icon='form')),
    ('image', ImageChooserBlock(icon='image')),
    ('create_project_button', CreateProjectButtonBlock()),    
    ('media', EmbedBlock(icon="media")),
    ('html', RawHTMLBlock(icon="code")),
    ('link', LinkBlock(icon="link")),
]
    

class DoubleFrameBlock(StructBlock):
    
    columns = blocks.ChoiceBlock(label=_('Proportions'), choices=[
        ('6-6', _('1/2 + 1/2')),
        ('8-4', _('2/3 + 1/3')),
        ('4-8', _('1/3 + 2/3')),
    ], required=True, default='6-6', icon='fa fa-columns')
    
    left = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    right = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    
    class Meta:
        icon = 'fa fa-columns'
        template = 'cosinnus/wagtail/widgets/double_frame.html'
    
    def get_context(self, value):
        context = super(DoubleFrameBlock, self).get_context(value)
        context['left'] = value.get('left')
        context['right'] = value.get('right')
        context['columns'] = value.get('columns')
        return context

class TripleFrameBlock(StructBlock):
    
    columns = blocks.ChoiceBlock(label=_('Proportions'), choices=[
        ('4-4-4', _('1/3 + 1/3 + 1/3')),
        ('6-3-3', _('1/2 + 1/4 + 1/4')),
        ('3-6-3', _('1/4 + 1/2 + 1/4')),
        ('3-3-6', _('1/4 + 1/4 + 1/2')),
    ], required=True, default='4-4-4', icon='fa fa-columns')
    
    left = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    middle = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    right = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    
    class Meta:
        icon = 'fa fa-columns'
        template = 'cosinnus/wagtail/widgets/triple_frame.html'
    
    def get_context(self, value):
        context = super(TripleFrameBlock, self).get_context(value)
        context['left'] = value.get('left')
        context['middle'] = value.get('middle')
        context['right'] = value.get('right')
        context['columns'] = value.get('columns')
        return context
    
class QuadFrameBlock(StructBlock):
    
    left = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    middle_left = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    middle_right = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')
    right = blocks.StreamBlock(STREAMFIELD_BLOCKS_NOFRAMES, icon='cogs')

    class Meta:
        icon = 'fa fa-columns'
        template = 'cosinnus/wagtail/widgets/quad_frame.html'
    
    def get_context(self, value):
        context = super(QuadFrameBlock, self).get_context(value)
        context['left'] = value.get('left')
        context['middle_left'] = value.get('middle_left')
        context['middle_right'] = value.get('middle_right')
        context['right'] = value.get('right')
        return context

 
STREAMFIELD_BLOCKS = STREAMFIELD_BLOCKS_NOFRAMES + [   
    ('layout_2x1', DoubleFrameBlock(icon="form")),
    ('layout_3x1', TripleFrameBlock(icon="form")),
    ('layout_4x1', QuadFrameBlock(icon="form")),
]



class GlobalNotesWidgetBlock(blocks.ChoiceBlock):
    
    choices=[
        ('250', _('Medium News Widget')),
        ('500', _('Large News Widget')),
    ]
    default = '250'
    
    class Meta:
        icon = 'form'
        template = 'cosinnus/wagtail/widgets/global_notes.html'
    
    def get_context(self, value):
        context = super(GlobalNotesWidgetBlock, self).get_context(value)
        context['height'] = value
        return context


class RandomProjectsWidgetBlock(blocks.ChoiceBlock):
    
    choices=[
        ('4', _('4 Random Projects Widget')),
        ('8', _('8 Random Projects Widget')),
    ]
    default = '4'
    
    class Meta:
        icon = 'group'
        template = 'cosinnus/wagtail/widgets/random_projects.html'
    
    def get_random_projects(self, count=4):
        all_pks = CosinnusProject.objects.get_pks().keys()
        shuffle(all_pks)
        pks = all_pks[:count]
        projects = CosinnusProject.objects.get_cached(pks=pks)
        return projects
    
    def get_context(self, value):
        context = super(RandomProjectsWidgetBlock, self).get_context(value)
        context['projects'] = self.get_random_projects(int(value))
        return context


STREAMFIELD_BLOCKS_WIDGETS = [
    ('news', GlobalNotesWidgetBlock()),  
    ('random_projects', RandomProjectsWidgetBlock()),  
]


# old wagtail block set. for page types we want to phase out
STREAMFIELD_OLD_BLOCKS = [
    ('paragraph', BetterRichTextBlock(icon='form')),
    ('image', ImageChooserBlock(icon='image')),
    ('create_project_button', CreateProjectButtonBlock())
]
    