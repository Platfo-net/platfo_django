import logging

from django.db import models

from notification.enums import SMSNotificationSender


class SmsNotification(models.Model):
    receiver = models.CharField(max_length=13, verbose_name='receiver number')
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_id = models.CharField(max_length=30, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    plain_text = models.TextField(verbose_name='sms content', blank=True, null=True)

    def send(self):
        from utilities.tasks import (send_user_activation_code_task,
                                     send_user_reset_password_code_task,
                                     send_plain_text_sms_task)

        if not (self.template_name or self.plain_text or self.template_id):
            raise ValueError('Sms must have either template_name or plain_text or template_id')

        try:
            logging.info('Queueing SMS', extra={
                'RECEIVER': self.receiver,
            })
            if self.template_name == SMSNotificationSender.USER_ACTIVATION.value:
                send_user_activation_code_task.apply_async(
                    args=(self.receiver, self.template_id, self.plain_text
                          )
                )
            elif self.template_name == SMSNotificationSender.RESET_PASSWORD.value:
                send_user_reset_password_code_task.apply_async(
                    args=(self.receiver, self.template_id, self.plain_text
                          )
                )
            else:
                send_plain_text_sms_task.apply_async(
                    args=(self.receiver, self.plain_text)
                )
        except Exception:
            logging.exception('Could not run sms task')

    def __str__(self):
        return f'{self.receiver} ({self.datetime})'
