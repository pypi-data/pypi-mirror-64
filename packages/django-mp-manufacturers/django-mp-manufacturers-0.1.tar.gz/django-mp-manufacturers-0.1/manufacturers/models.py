
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Manufacturer(models.Model):

    name = models.CharField(
        _('Manufacturer name'),
        max_length=255,
        unique=True,
        db_index=True)

    logo = models.ImageField(
        _('Logo'),
        max_length=255,
        blank=True,
        null=True,
        upload_to='manufacturers')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


class ManufacturerField(models.ForeignKey):

    def __init__(
            self,
            to=Manufacturer,
            on_delete=models.SET_NULL,
            verbose_name=_('Manufacturer'),
            blank=True,
            null=True,
            *args, **kwargs):
        super().__init__(
            to=to,
            on_delete=on_delete,
            verbose_name=verbose_name,
            blank=blank,
            null=null,
            *args, **kwargs)
