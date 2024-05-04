from django_celery_beat.models import PeriodicTask
from django_lifecycle import AFTER_SAVE, BEFORE_DELETE, hook


class CeleryTaskMixin:
    @staticmethod
    def _get_celery_task_identifier() -> str:
        raise NotImplementedError()

    def _get_celery_task_description(self) -> str:
        raise NotImplementedError()

    def _get_celery_task_kwargs(self) -> str:
        raise NotImplementedError()

    def _get_periodic_task_defaults(self) -> dict:
        raise NotImplementedError()

    def _create_celery_task_enabled(self):
        return not getattr(self, 'is_archived', False)

    @hook(AFTER_SAVE)
    def _create_celery_task(self):
        if self._create_celery_task_enabled():
            PeriodicTask.objects.update_or_create(name=self._get_celery_task_description(),
                                                  task=self._get_celery_task_identifier(),
                                                  kwargs=self._get_celery_task_kwargs(),
                                                  defaults=self._get_periodic_task_defaults())

    @hook(BEFORE_DELETE)
    def _remove_celery_task(self):
        PeriodicTask.objects.filter(name=self._get_celery_task_description(),
                                    task=self._get_celery_task_identifier(),
                                    kwargs=self._get_celery_task_kwargs()).delete()
