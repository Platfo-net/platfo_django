from utilities.admin.commons import CommonModelAdmin


class AddForbiddenBaseAdminMixin:
    """Keep these permission mixins before BaseAdmin or its subclasses"""
    def has_add_permission(self, request, obj=None):
        return False


class DeleteForbiddenBaseAdminMixin:
    """Keep these permission mixins before BaseAdmin or its subclasses"""
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class NeitherAddNorDeleteAdmin(AddForbiddenBaseAdminMixin, DeleteForbiddenBaseAdminMixin,
                               CommonModelAdmin):
    """
    Must be declared before other sublasses of `admin.ModelAdmin` in case of
    multiple inheritance.
    """
    pass
