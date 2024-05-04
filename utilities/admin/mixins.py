from django.contrib.admin import widgets
from django.core.paginator import Paginator
from django.db import OperationalError, connection, models, transaction
from django.utils.functional import cached_property

from utilities.admin.link import ForeignKeyLinkWidget


class LongIntegerMixin:
    formfield_overrides = {models.IntegerField: {'widget': widgets.AdminBigIntegerFieldWidget()}, }


class LargeQuerysetPaginator(Paginator):
    @cached_property
    def count(self):
        try:
            with transaction.atomic(), connection.cursor() as cursor:
                cursor.execute('SET LOCAL statement_timeout TO 5;')
                return super().count
        except OperationalError:
            pass

        if not self.object_list.query.where:
            try:
                with transaction.atomic(), connection.cursor() as cursor:
                    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s",
                                   [self.object_list.query.model._meta.db_table])
                    estimate = int(cursor.fetchone()[0])
                    return estimate
            except Exception:
                pass
        return super().count


class LargeQuerysetMixin:
    show_full_result_count = False
    paginator = LargeQuerysetPaginator


class LinkMixin:
    link_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def get_form(self, request, obj=None, **kwargs):
        self.object = obj
        return super().get_form(request, obj, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.object = obj
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if self.link_fields and self.object is not None and db_field.name in self.link_fields:
            kwargs['widget'] = ForeignKeyLinkWidget(db_field.remote_field, self.admin_site,
                                                    using=kwargs.get('using'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


