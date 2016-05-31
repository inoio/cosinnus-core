# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import wagtail_modeltranslation.models
from django.conf import settings

import cosinnus.models.wagtail_blocks

class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('cosinnus', '0007_auto_20160413_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamDashboardDoubleColumnPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_de', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_uk', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('show_register_button', models.BooleanField(default=True, verbose_name='Show Register Button')),
                ('redirect_if_logged_in', models.BooleanField(default=False, help_text='If active, this page will only be visible to non-logged-in users. All others will be redirected to the activities page.', verbose_name='Redirect Logged in Users')),
                ('banner_left', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left banner (top)', blank=True)),
                ('banner_left_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_right', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Right banner (top)', blank=True)),
                ('banner_right_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('header', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Header', blank=True)),
                ('header_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('footer_left', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left footer', blank=True)),
                ('footer_left_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_right', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Right footer', blank=True)),
                ('footer_right_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('content1', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content (left column)', blank=True)),
                ('content1_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content1_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content1_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content1_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content2', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content (right column)', blank=True)),
                ('content2_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
                ('content2_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
                ('content2_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
                ('content2_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
            ],
            options={
                'verbose_name': '2-Column Dashboard Page (Modular)',
            },
            bases=(cosinnus.models.wagtail_models.SplitMultiLangTabsMixin, wagtail_modeltranslation.models.TranslationMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='StreamDashboardSingleColumnPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_de', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_uk', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('show_register_button', models.BooleanField(default=True, verbose_name='Show Register Button')),
                ('redirect_if_logged_in', models.BooleanField(default=False, help_text='If active, this page will only be visible to non-logged-in users. All others will be redirected to the activities page.', verbose_name='Redirect Logged in Users')),
                ('banner_left', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left banner (top)', blank=True)),
                ('banner_left_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_right', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Right banner (top)', blank=True)),
                ('banner_right_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('header', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Header', blank=True)),
                ('header_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('footer_left', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left footer', blank=True)),
                ('footer_left_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_right', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Right footer', blank=True)),
                ('footer_right_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('content1', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content', blank=True)),
                ('content1_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content1_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content1_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content1_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
            ],
            options={
                'verbose_name': '1-Column Dashboard Page (Modular)',
            },
            bases=(cosinnus.models.wagtail_models.SplitMultiLangTabsMixin, wagtail_modeltranslation.models.TranslationMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='StreamDashboardTripleColumnPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_de', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_uk', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('show_register_button', models.BooleanField(default=True, verbose_name='Show Register Button')),
                ('redirect_if_logged_in', models.BooleanField(default=False, help_text='If active, this page will only be visible to non-logged-in users. All others will be redirected to the activities page.', verbose_name='Redirect Logged in Users')),
                ('banner_left', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left banner (top)', blank=True)),
                ('banner_left_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_left_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left banner (top)', blank=True)),
                ('banner_right', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Right banner (top)', blank=True)),
                ('banner_right_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('banner_right_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right banner (top)', blank=True)),
                ('header', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Header', blank=True)),
                ('header_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('header_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Header', blank=True)),
                ('footer_left', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left footer', blank=True)),
                ('footer_left_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_left_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left footer', blank=True)),
                ('footer_right', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Right footer', blank=True)),
                ('footer_right_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('footer_right_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Right footer', blank=True)),
                ('content1', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content (left column)', blank=True)),
                ('content1_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content1_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content1_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content1_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (left column)', blank=True)),
                ('content2', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content (center column)', blank=True)),
                ('content2_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (center column)', blank=True)),
                ('content2_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (center column)', blank=True)),
                ('content2_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (center column)', blank=True)),
                ('content2_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (center column)', blank=True)),
                ('content3', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content (right column)', blank=True)),
                ('content3_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
                ('content3_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
                ('content3_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
                ('content3_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content (right column)', blank=True)),
            ],
            options={
                'verbose_name': '3-Column Dashboard Page (Modular)',
            },
            bases=(cosinnus.models.wagtail_models.SplitMultiLangTabsMixin, wagtail_modeltranslation.models.TranslationMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='StreamSimpleOnePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_de', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_uk', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('content', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content', blank=True)),
                ('content_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
            ],
            options={
                'verbose_name': 'Simple One-Column Page (Modular)',
            },
            bases=(cosinnus.models.wagtail_models.SplitMultiLangTabsMixin, wagtail_modeltranslation.models.TranslationMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='StreamSimpleTwoPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_de', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('title_uk', models.CharField(help_text="The page title as you'd like it to be seen by the public", max_length=255, null=True, verbose_name='Title')),
                ('content', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Content', blank=True)),
                ('content_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('content_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Content', blank=True)),
                ('leftnav', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], verbose_name='Left Sidebar', blank=True)),
                ('leftnav_de', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left Sidebar', blank=True)),
                ('leftnav_en', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left Sidebar', blank=True)),
                ('leftnav_ru', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left Sidebar', blank=True)),
                ('leftnav_uk', wagtail.wagtailcore.fields.StreamField([('paragraph', cosinnus.models.wagtail_blocks.BetterRichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True, verbose_name='Left Sidebar', blank=True)),
            ],
            options={
                'verbose_name': 'Simple Page with Left Navigation (Modular)',
            },
            bases=(cosinnus.models.wagtail_models.SplitMultiLangTabsMixin, wagtail_modeltranslation.models.TranslationMixin, 'wagtailcore.page'),
        ),
    ]
