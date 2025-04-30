import pathlib
from typing import TypeVar

from datasources.utils import create_file_name
from datasources.validators import validate_id
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from dataset_backend.utils import create_id

D = TypeVar('D', 'DataSource')


class Webhook(models.Model):
    """A webhook is an endpoint via which
    data can be updated or added in a sheet"""

    sheet = models.ForeignKey(
        'datasources.DataSource',
        on_delete=models.CASCADE,
        blank=True
    )
    webhook_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_id]
    )
    usage = models.PositiveIntegerField(
        default=0
    )
    last_usage = models.DateTimeField(
        default=now
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_on']
        constraints = [
            models.UniqueConstraint(
                fields=['webhook_id', 'sheet'],
                name='unique_webhook_id'
            )
        ]

    def __str__(self):
        return f'Webhook: {self.webhook_id}'


class DataSource(models.Model):
    """A data source is a connection to a local
    csv file or a Google Sheet spreadsheet. A data
    source can be created either by uploading a csv file,
    by creating a csv file via an API endpoint or
    by linking to a Google spreadsheet"""

    user = models.ForeignKey(
        get_user_model(),
        models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    data_source_id = models.CharField(
        verbose_name='Data source ID',
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_id]
    )
    google_sheet_url = models.URLField(
        unique=True,
        help_text=_("The Google sheet's url"),
        blank=True,
        null=True
    )
    csv_file = models.FileField(
        verbose_name='CSV file',
        help_text=_("The csv file to use to create a new sheet"),
        upload_to=create_file_name,
        validators=[],
        blank=True,
        null=True
    )
    endpoint_url = models.URLField(
        help_text=_(
            "The endpoint to use to create a new "
            "local csv file source or a Google sheet"
        ),
        blank=True,
        null=True
    )
    endpoint_data_key = models.CharField(
        max_length=100,
        help_text=_(
            "The key under which the actual "
            "data is stored ex. results in "
            "{'count': 14, 'results: []'}"),
        blank=True,
        null=True
    )
    columns = models.JSONField(
        help_text=_("The data type for each column"),
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'DataSource: {self.data_source_id}'

    @property
    def csv_based(self):
        """Returns whether the data source
        was created by uploading a csv file"""
        return self.endpoint_url is None

    @property
    def is_endpoint(self):
        return self.endpoint_url != None

    @cached_property
    def column_names(self):
        """Return the column names as strings"""
        if self.columns is None:
            return []
        return [item['name'] for item in self.columns]


@receiver(pre_save, sender=DataSource)
def create_data_source_id(instance, **kwargs):
    if instance.data_source_id is None:
        instance.data_source_id = create_id('ds')


@receiver(pre_save, sender=Webhook)
def create_webhook_id(instance, **kwargs):
    if instance.webhook_id is None:
        instance.webhook_id = create_id('wk')


@receiver(post_delete, sender=DataSource)
def delete_csv_file_on_delete(instance, **kwargs):
    """Deletes a csv file that was previously uploaded
    by a user once the instance is deleted"""
    if instance.csv_file is not None:
        try:
            path = pathlib.Path(instance.csv_file.path)
        except:
            return
        if path.exists() and path.is_file():
            parent = path.parent.absolute()
            files = parent.glob('**/*.csv')
            for file in files:
                file.unlink()
            parent.rmdir()


@receiver(pre_save, sender=DataSource)
def change_csv_file_on_delete(instance, **kwargs):
    """Checks if a file is the same as the current
    one saved in the database and deletes the old file
    to replace it by the new uploaded one if needed"""
    if instance.pk:
        try:
            data_source = DataSource.objects.get(user__id=instance.pk)
        except:
            return

        if data_source and data_source.csv_file == instance.csv_file:
            try:
                path = data_source.csv_file.path
            except:
                return

            path = pathlib.Path(path)
            if path.exists() and path.is_file():
                path.unlink()


@receiver(post_save, sender=DataSource)
def clean_csv_data(instance, **kwargs):
    # Work the CSV file based on the elemnents
    # that the user has provided to us
    # csv_instance = CSVData(instance)
    # print(csv_instance)
    pass
