from django import shortcuts
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_object_actions.utils import DjangoObjectActions
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView


class CustomActionsMixin(DjangoObjectActions):
    change_list_template = 'admin/custom_actions_change_list.html'

    @staticmethod
    def modify_admin_urls(admin_instance, *urls):
        # Order of operands matters
        return list(urls) + super(admin_instance.__class__, admin_instance).get_urls()


class CustomAdminActionView(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, IsAdminUser, )
    parser_classes = (FormParser, MultiPartParser, )
    form_class = None
    template = None
    title = ''
    multipart = False
    model_class = NotImplementedError()
    submit_text = NotImplementedError()

    def perform_action(self, form, request, **kwargs):
        """Method for subclasses to perform the action the form meant to do.

        :param form: Cleaned instance of form from class provided as form_class
        :param request: The received request with valid data
        :return: Should return an instance of Django or DRF response to be returned to the user
        """
        pass

    def _redirect_to_model_admin(self):
        # noinspection PyProtectedMember,PyUnresolvedReferences
        path = 'admin:{}_{}_changelist'.format(self.model_class._meta.app_label,
                                               self.model_class._meta.model_name)
        return HttpResponseRedirect(reverse(path))

    def get(self, request, **kwargs):
        return self.render_admin_template(request, **kwargs)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if not form.is_valid():
            kwargs.update(form=form)
            return self.render_admin_template(request, **kwargs)

        return self.perform_action(form, request, **kwargs)

    def render_admin_template(self, request, template=None, **kwargs):
        context = {
            'form': self.form_class(),
            'title': self.title,
            'submit_text': self.submit_text,
            'opts': self.model_class._meta,
            'multipart': self.multipart,
        }
        context.update(kwargs)
        if template is None:
            template = self.template

        return shortcuts.render(request, template, context)
