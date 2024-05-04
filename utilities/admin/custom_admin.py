from functools import partial

from django.forms import MediaDefiningClass
from django.urls import NoReverseMatch

from utilities.datetime_utils.date_factory import get_string_jalali


class CustomModelAdminMetaclass(MediaDefiningClass):
    """
    ModelAdmin classes using this Meta will have these features:

    1) any date/datetime field can be shown jalali by appending their name with '_jalali'
        for example 'created_at' can be shown jalali by 'created_at_jalali'
        please note that using this in 'fields' wont show jalali widget, just plain text.

    these features work in 'list_display', 'readonly_fields', 'fields'
    """
    @staticmethod
    def jalali(instance, field):
        target = getattr(instance, field)
        return get_string_jalali(target)

    def __new__(mcs, name, bases, attrs):

        new_class = super(CustomModelAdminMetaclass, mcs).__new__(mcs, name, bases, attrs)

        def _add_method(name):
            # FIXME: The fields verbose_name instead of raw_name
            if name is None:
                return
            if name.endswith('_jalali'):
                try:
                    raw_name = name[:-7]
                    method = partial(mcs.jalali, field=raw_name)
                    method.__name__ = raw_name
                    method.allow_tags = True
                    method.admin_order_field = raw_name
                    setattr(new_class, name, method)
                except NoReverseMatch:
                    pass

            if name.endswith('_intcomma'):
                try:
                    raw_name = name[:-9]
                    method = partial(lambda instance, field: f"{getattr(instance, field):,}",
                                     field=raw_name)
                    method.__name__ = raw_name
                    method.allow_tags = True
                    method.admin_order_field = raw_name
                    setattr(new_class, name, method)
                except NoReverseMatch:
                    pass

        if hasattr(new_class, "list_display") and new_class.list_display is not None:
            for name in new_class.list_display:
                _add_method(name)
        if new_class.readonly_fields is not None:
            for name in new_class.readonly_fields:
                _add_method(name)
        if new_class.fields is not None:
            for name in new_class.fields:
                _add_method(name)

        return new_class
