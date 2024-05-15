import logging

from celery.app import shared_task
from utilities.sms.sms_ir_sms_provider import SmsIrSender


@shared_task(rate_limit='30/s')
def send_user_activation_code_task(receiver, template_id, plain_text):
    logging.info('Sending SMS', extra={'RECEIVER': receiver, 'TEXT': plain_text, })
    SmsIrSender(receiver, template_id, plain_text).send_verify_sms(fail_silently=False)


@shared_task(rate_limit='30/s')
def send_user_reset_password_code_task(receiver, template_id, plain_text):
    logging.info('Sending SMS', extra={'RECEIVER': receiver, 'TEXT': plain_text, })
    SmsIrSender(receiver, template_id, plain_text).send_verify_sms(fail_silently=False)


@shared_task(rate_limit='30/s')
def send_plain_text_sms_task(receiver, plain_text):
    logging.info('Sending SMS', extra={'RECEIVER': receiver, 'TEXT': plain_text, })
    SmsIrSender(receiver, plain_text=plain_text).send_plain_text_sms(fail_silently=False)
