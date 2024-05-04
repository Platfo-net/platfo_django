from functools import partial, wraps

from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db.models import Model
from django.forms.widgets import HiddenInput
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def _render_link(app_label, model_name, instance_id, text):
    path = reverse('admin:{}_{}_change'.format(app_label, model_name, ), args=[instance_id], )
    return mark_safe('<a class="fk-link" href="{url}">{label}</a>'.format(url=path, label=text))


def create_link_for_object(obj_for_link, func=None):
    if obj_for_link is None:
        return '-'
    func_name = '' if func is None else func.__name__
    if not isinstance(obj_for_link, Model):
        raise TypeError('Admin method {method} should output a valid instance of one of '
                        'registered django model. '
                        'Found: {result}'.format(result=obj_for_link, method=func_name))
    return _render_link(obj_for_link._meta.app_label, obj_for_link._meta.model_name,
                        obj_for_link.id, '{}'.format(obj_for_link))


def create_link_for_id(obj_id, namespace):
    if obj_id is None:
        return '-'
    link = reverse(namespace, args=(obj_id, ))
    return format_html('<a href="{}">{}</a>', link, obj_id)


def as_link(func=None, *, namespace=None):
    if func is None:
        return partial(as_link, namespace=namespace)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if namespace:
                obj_id = func(*args, **kwargs)
                return create_link_for_id(obj_id, namespace)
            else:
                obj_for_link = func(*args, **kwargs)
                return create_link_for_object(obj_for_link, func)
        except NoReverseMatch:
            return func(*args, **kwargs)

    return wrapper


class ForeignKeyLinkWidget(ForeignKeyRawIdWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['readonly'] = 'readonly'
        output = super().render(name, value, attrs)
        try:
            link = _render_link(self.rel.model._meta.app_label, self.rel.model._meta.model_name,
                                value,
                                self.label_and_url_for_value(value)[0])
        except NoReverseMatch:
            return output
        return self.render_hidden_input(name, value, attrs) + link

    def render_hidden_input(self, name, value, attrs=None):
        text_in = HiddenInput().render(name, value, attrs)
        return mark_safe('<div>{input}</div>'.format(input=text_in))
