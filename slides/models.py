from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from my_database.validators import validate_id
from sheets.models import Sheet
from sheets.utils import create_id
from slides.choices import AccessChoices, ComponentTypes

USER_MODEL = get_user_model()


class Slide(models.Model):
    """A slide can be considered as a page that 
    holds a set of blocks which contain either data
    from the overall slide or specific data unique to
    the block"""

    user = models.ForeignKey(USER_MODEL, models.CASCADE)
    # TODO: Determine whether a slide should have one data
    # single data source or multiple data sources. In which
    # case fields like search_columns cannot be on one single
    # Slide model
    # FIXME: Not sure what the purpose of this field is.
    # Just create one foreign key to a given sheet as
    # opposed to using a ManyToManyField
    sheets = models.ManyToManyField(Sheet, blank=True)
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    slide_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_id]
    )
    blocks = models.ManyToManyField('Block', blank=True)
    # TODO: Foreign key to sheets
    slide_data_source = models.CharField(
        help_text=_('Top level slide data source'),
        max_length=100,
        blank=True,
        null=True
    )
    access = models.CharField(
        max_length=100,
        default=AccessChoices.PUBLIC,
        choices=AccessChoices.choices
    )
    columns_visibility = None
    # share_url = models.URLField(blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Slide: {self.slide_id}'


class Block(models.Model):
    """A block represents a section that
    holds data. It can hold either page/slide 
    level data or  block level data. A block
    is automatically linked to a page or a slide"""

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    block_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_id]
    )
    component = models.CharField(
        max_length=100,
        default=ComponentTypes.TABLE_BLOCK,
        choices=ComponentTypes.choices
    )
    record_creation_columns = models.JSONField(
        help_text=_(
            "Columns to consider when the user "
            "attemps to create a new record"
        ),
        blank=True,
        null=True
    )
    record_update_columns = models.JSONField(
        help_text=_(
            "Columns to consider when the user attemps "
            "to update a new record"
        ),
        blank=True,
        null=True
    )
    visible_columns = models.JSONField(
        help_text=_("Columns to be visible at the block level"),
        blank=True,
        null=True
    )
    # FIXME: This should be a foreign key to
    # Sheet -> DataSource
    block_data_source = models.URLField(
        blank=True,
        null=True,
        help_text=_('Link this specific block to a specific data source')
    )
    search_columns = models.JSONField(
        help_text=_(
            "The columns to use when the user "
            "attemps to search for data"
        ),
        blank=True,
        null=True
    )
    user_filters = models.JSONField(
        help_text=_("The filters the user is allowed to use"),
        blank=True,
        null=True
    )
    conditions = models.JSONField(
        help_text=_("Internal block configuration"),
        blank=True,
        null=True
    )
    allow_record_creation = models.BooleanField(
        help_text=_("Whether the block should accept record creation"),
        default=True
    )
    allow_record_update = models.BooleanField(
        help_text=_("Whether the block should accept record update"),
        default=True
    )
    allow_record_search = models.BooleanField(
        help_text=_("Whether the block should accept record search"),
        default=True
    )
    active = models.BooleanField(default=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Block: {self.block_id}'

    @property
    def data_source(self):
        """We can have both page level and block 
        level data source. When both a present,
        consider the block level first and then
        the slide data source in second"""
        if self.block_data_source is None:
            return self.slide_set.latest('created_on').slide_data_source
        return self.block_data_source


@receiver(pre_save, sender=Slide)
def create_slide_id(instance, **kwargs):
    if instance.slide_id is None:
        instance.slide_id = create_id('sl')


@receiver(pre_save, sender=Block)
def create_block_id(instance, **kwargs):
    if instance.block_id is None:
        instance.block_id = create_id('bl')
