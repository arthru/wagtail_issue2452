from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import (
    StreamFieldPanel, FieldPanel, InlinePanel, MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.wagtailcore.blocks import (
    CharBlock,
    TextBlock,
    StreamBlock,
    StructBlock,
    ChoiceBlock,
    RichTextBlock,
)
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

from modelcluster.fields import ParentalKey


class OneConceptBlock(StructBlock):
    name = CharBlock()
    details = TextBlock()
    image = ImageChooserBlock()


class ManyConceptBlock(StreamBlock):
    one_concept = OneConceptBlock()


class ConceptBlock(StructBlock):
    title = CharBlock()
    subtitle = CharBlock()
    many_concept = ManyConceptBlock()


class WineGrowerBlock(StructBlock):
    title = CharBlock()
    subtitle = CharBlock()
    display_number = ChoiceBlock(choices=[(str(i), i) for i in range(8)])


class PictureBackgroundBlock(StructBlock):
    title = CharBlock()
    subtitle = CharBlock()
    background = ImageChooserBlock()
    content = TextBlock()


class HomePageBlock(StreamBlock):
    picture_background = PictureBackgroundBlock()
    concept = ConceptBlock()
    winegrower = WineGrowerBlock()


class HomePage(Page):
    body = StreamField(HomePageBlock(), blank=True)
    contact_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

FormPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('form_fields', label="Form fields"),
    FieldPanel('thank_you_text', classname="full"),
    MultiFieldPanel([
        FieldPanel('to_address', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('subject', classname="full"),
    ], "Email")
]


class ContentBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    paragraph = RichTextBlock(icon="pilcrow")


class ContentPage(Page):
    body = StreamField(ContentBlock())


ContentPage.content_panels = Page.content_panels + [StreamFieldPanel('body')]

HomePage.content_panels += [
    StreamFieldPanel('body'),
    PageChooserPanel('contact_page', FormPage),
]
